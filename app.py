import os
import base64
import requests
import time
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)
# --- ADD DIAGNOSTIC LOGGING ---
logging.basicConfig(level=logging.INFO)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB upload limit

# --- Gemini API Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent?key={GEMINI_API_KEY}"

# --- System Prompt for the AI Model ---
SYSTEM_PROMPT = """You are a specialized AI photo editor for virtual try-ons. Your instructions are strict and must be followed precisely.
      
**Inputs & Roles:**
- **Image 1 (User Photo):** This is the target canvas. The person, their face, hair, body, pose, and the background in this image are the SINGLE SOURCE OF TRUTH for the human subject. They MUST be preserved perfectly.
- **Image 2 (Outfit Photo):** This image is for clothing reference ONLY. You MUST completely DISCARD and IGNORE any person, model, face, body, or mannequin present in this image. 

**Execution Steps:**
1.  Analyze the User Photo (Image 1) to understand the person's exact pose and body shape.
2.  Analyze the Outfit Photo (Image 2) to understand the garment. Extract ONLY the visual information about the clothing: its shape, texture, design, color, and how it drapes. Again, IGNORE the model wearing it.
3.  Perform the try-on: Realistically fit the extracted garment onto the person from the User Photo. The clothing must conform to their pose, creating natural folds and shadows that match the lighting in the User Photo. This is a REPLACEMENT of their original clothing, not a style transfer.
4.  Produce the final image.

**Output:** A single, clean, photorealistic image of the person from the User Photo now wearing the new outfit. No text, no artifacts, no borders."""


def file_to_base64(file_storage):
    """Converts a Flask FileStorage object to a Base64 encoded string."""
    try:
        return base64.b64encode(file_storage.read()).decode('utf-8')
    except Exception as e:
        app.logger.error(f"Error converting file to Base64: {e}")
        return None

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    """Handles image uploads and calls the Gemini API."""
    # --- DIAGNOSTIC LOGGING ---
    app.logger.info("--- Received a new /generate request ---")
    app.logger.info(f"Contents of request.files: {request.files}")

    # --- CORRECTED CODE: Using the right names from the HTML form ---
    if 'personPhoto' not in request.files or not request.files['personPhoto'].filename:
        app.logger.error("'personPhoto' not found in request.files or has no filename.")
        return jsonify({"error": "Person photo is required."}), 400
    
    if 'outfitPhoto' not in request.files or not request.files['outfitPhoto'].filename:
        app.logger.error("'outfitPhoto' not found in request.files or has no filename.")
        return jsonify({"error": "Outfit photo is required."}), 400

    # Convert images to Base64
    person_image = request.files['personPhoto']
    outfit_image = request.files['outfitPhoto']
    
    # We need to seek back to the beginning of the file stream before reading
    person_image.seek(0)
    outfit_image.seek(0)
    
    person_base64 = file_to_base64(person_image)
    outfit_base64 = file_to_base64(outfit_image)
    
    if not person_base64 or not outfit_base64:
        return jsonify({"error": "Could not process one or both images."}), 500

    image_parts = [
        {"inlineData": {"mimeType": person_image.mimetype, "data": person_base64}},
        {"inlineData": {"mimeType": outfit_image.mimetype, "data": outfit_base64}}
    ]
    
    # Prepare payload for Gemini API
    payload = {
        "contents": [{"parts": [{"text": SYSTEM_PROMPT}] + image_parts}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }

    # --- API Call with Exponential Backoff ---
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            response = requests.post(GEMINI_API_URL, json=payload, headers={'Content-Type': 'application/json'})
            response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

            result = response.json()
            
            parts = result.get('candidates', [{}])[0].get('content', {}).get('parts', [])
            image_data = next((p['inlineData']['data'] for p in parts if 'inlineData' in p), None)
            
            if image_data:
                image_url = f"data:image/png;base64,{image_data}"
                return jsonify({"image": image_url}) # Changed key to "image" to match JS
            else:
                error_message = result.get('promptFeedback', {}).get('blockReason', {}).get('message', 'No image data returned from API. The content may have been blocked.')
                return jsonify({"error": error_message}), 500

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429 or err.response.status_code >= 500:
                if attempt < max_attempts - 1:
                    wait_time = (2 ** attempt) + (time.time() % 1)
                    app.logger.warning(f"API rate limit or server error. Retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                else:
                    return jsonify({"error": "The service is currently busy. Please try again later."}), 503
            else:
                app.logger.error(f"HTTP Error: {err.response.status_code} - {err.response.text}")
                return jsonify({"error": f"An API error occurred: {err.response.reason}"}), 500
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Request failed: {e}")
            return jsonify({"error": "Failed to connect to the image generation service."}), 500
        except Exception as e:
            app.logger.error(f"An unexpected error occurred: {e}")
            return jsonify({"error": "An unexpected server error occurred."}), 500
    
    return jsonify({"error": "Failed to generate image after multiple attempts."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

