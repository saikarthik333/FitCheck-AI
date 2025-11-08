# FitCheck AI ✨

An AI-powered virtual try-on application that lets you see yourself in any outfit instantly. Built with Python, Flask, and the Google Gemini API.

## 🚀 Live Demo

You can try the live application here:
[**https://fitcheck-ai-w1me.onrender.com/**](https://fitcheck-ai-w1me.onrender.com/)

## 💡 The Problem

Online clothes shopping has one big problem: "Will this actually look good on me?" This project was born from a personal frustration I've had for years. FitCheck AI is a tool I built to fix this, helping you visualize your fit *before* you buy, just in time for festive shopping.

## ✨ Features

  * **AI-Powered Virtual Try-On:** Upload a photo of yourself and a photo of an outfit to generate a new image of you wearing it.
  * **Intuitive UI:** A clean, modern, and responsive frontend that works on both desktop and mobile.
  * **Drag-and-Drop:** Easy-to-use drag-and-drop file uploads for a smooth user experience.
  * **User-Guided AI:** Built with a sophisticated system prompt to guide the AI, ensuring the user's face and pose are preserved while the outfit is realistically applied.
  * **Instant Feedback:** A simple feedback mechanism to help users and improve the experience.

## 🛠️ Tech Stack

  * **Backend:** Python, Flask, Gunicorn (for production)
  * **Frontend:** HTML5, CSS3, Vanilla JavaScript (for interactivity)
  * **AI:** Google Gemini API (`gemini-2.5-flash-image-preview`)
  * **Deployment:** Render (PaaS), Git, GitHub
  * **Core Libraries:** `requests` (for API calls), `python-dotenv` (for environment variables)

## 🔧 Getting Started: Running Locally

Follow these instructions to get a copy of the project running on your local machine for development and testing.

### 1\. Prerequisites

  * [Python 3.10+](https://www.python.org/downloads/)
  * [Git](https://www.google.com/search?q=https://git-scm.com/downloads)
  * A Google Cloud Platform (GCP) account with the **Generative Language API** enabled and billing active.

### 2\. Clone the Repository

```bash
git clone https://github.com/saikarthik333/FitCheck-AI.git
cd FitCheck-AI
```

### 3\. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4\. Install Dependencies

Install all the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5\. Configure Environment Variables

This is a crucial step for storing your secret API key.

1.  Create a file named `.env` in the root of the project directory (the same folder as `app.py`).
2.  Add your Google Gemini API key to this file:

<!-- end list -->

```text
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 6\. Run the Application

Start the Flask development server.

```bash
flask run --port 5001
```

Open your browser and navigate to `http://127.0.0.1:5001` to see the application running.

## 👤 Author

**Motapothula Sai Karthik**

  * **LinkedIn:** [saikarthik333](https://www.linkedin.com/in/saikarthik333/)
  * **GitHub:** [saikarthik333](https://github.com/saikarthik333)

## 📄 License

This project is licensed under the MIT License.
