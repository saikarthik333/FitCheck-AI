document.addEventListener('DOMContentLoaded', () => {
    // --- Get all the elements we need from the page ---
    const form = document.getElementById('tryon-form');
    const resultImage = document.getElementById('result-image');
    const resultPlaceholder = document.getElementById('result-placeholder');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorDisplay = document.getElementById('error-display');
    const generateBtn = document.getElementById('generate-btn');
    const btnText = document.getElementById('btn-text');
    const postGenerationActions = document.getElementById('post-generation-actions');
    const feedbackThanks = document.getElementById('feedback-thanks');
    const feedbackButtons = document.querySelectorAll('.feedback-btn');

    // --- State variables to hold the selected files ---
    // This is a more robust way to manage files than relying on the input fields directly.
    let personFile = null;
    let outfitFile = null;

    /**
     * Sets up an entire upload area (both click and drag-and-drop)
     * @param {'person' | 'outfit'} areaType - The type of file we are handling.
     * @param {string} inputId - The ID of the file input element.
     * @param {string} dropZoneId - The ID of the div that acts as the drop zone.
     * @param {string} previewContainerId - The ID of the container for the image preview.
     * @param {string} instructionsId - The ID of the text instructions element.
     */
    function setupUploadArea(areaType, inputId, dropZoneId, previewContainerId, instructionsId) {
        const input = document.getElementById(inputId);
        const dropZone = document.getElementById(dropZoneId);
        const previewContainer = document.getElementById(previewContainerId);
        const instructions = document.getElementById(instructionsId);

        // --- Core function to handle a file once it's received ---
        const handleFile = (file) => {
            if (!file || !file.type.startsWith('image/')) {
                return; // Ignore non-image files
            }
            
            // Store the file in the correct state variable
            if (areaType === 'person') {
                personFile = file;
            } else if (areaType === 'outfit') {
                outfitFile = file;
            }

            // Display the preview
            const reader = new FileReader();
            reader.onload = (event) => {
                previewContainer.innerHTML = `<img src="${event.target.result}" alt="Preview" class="preview-image">`;
                previewContainer.style.display = 'block';
                instructions.style.display = 'none';
            };
            reader.readAsDataURL(file);
        };

        // --- Event Listeners ---

        // Handle file selection via the native file picker (when a user clicks)
        input.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });

        // Handle drag-and-drop
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault(); // This is necessary to allow a drop
            dropZone.classList.add('drag-over');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            if (e.dataTransfer.files.length > 0) {
                handleFile(e.dataTransfer.files[0]);
            }
        });
    }

    // Initialize both upload areas
    setupUploadArea('person', 'person-photo-input', 'person-drop-zone', 'person-preview-container', 'person-instructions');
    setupUploadArea('outfit', 'outfit-photo-input', 'outfit-drop-zone', 'outfit-preview-container', 'outfit-instructions');


    // --- Form Submission ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Check our state variables instead of the input fields
        if (!personFile || !outfitFile) {
            showError('Please select both your photo and an outfit photo.');
            return;
        }

        setLoading(true);
        
        // Manually build the FormData object from our state variables. This is the most reliable method.
        const formData = new FormData();
        formData.append('personPhoto', personFile);
        formData.append('outfitPhoto', outfitFile);

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.error || `Server responded with status: ${response.status}`;
                throw new Error(errorMessage);
            }

            const data = await response.json();
            resultImage.src = data.image;
            resultImage.style.display = 'block';
            resultPlaceholder.style.display = 'none';
            postGenerationActions.style.display = 'block';

        } catch (error) {
            console.error('Error:', error);
            showError(error.message);
            resultImage.style.display = 'none';
            resultPlaceholder.style.display = 'block';
        } finally {
            setLoading(false);
        }
    });

    // --- Feedback Buttons ---
    feedbackButtons.forEach(button => {
        button.addEventListener('click', () => {
            feedbackThanks.style.display = 'block';
            feedbackButtons.forEach(btn => btn.disabled = true);
        });
    });


    // --- UI Helper Functions ---
    function setLoading(isLoading) {
        if (isLoading) {
            generateBtn.disabled = true;
            btnText.textContent = 'Generating...';
            loadingSpinner.style.display = 'flex';
            resultImage.style.display = 'none';
            resultPlaceholder.style.display = 'none';
            errorDisplay.style.display = 'none';
            postGenerationActions.style.display = 'none';
            feedbackThanks.style.display = 'none';
            feedbackButtons.forEach(btn => btn.disabled = false);
        } else {
            generateBtn.disabled = false;
            btnText.textContent = 'Check My Fit';
            loadingSpinner.style.display = 'none';
        }
    }

    function showError(message) {
        errorDisplay.innerHTML = message;
        errorDisplay.style.display = 'block';
    }
});

