document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const imagePreview = document.getElementById('image-preview');
    const previewContainer = document.getElementById('preview-container');
    const uploadContent = document.querySelector('.upload-content');
    const analyzeBtn = document.getElementById('analyze-btn');
    const removeBtn = document.getElementById('remove-btn');
    const resultsSection = document.getElementById('results');
    const loadingSection = document.getElementById('loading');

    let currentFile = null;

    // Drag & Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    dropZone.addEventListener('click', (e) => {
        if (e.target !== removeBtn) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUpload();
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file (JPG, PNG).');
            return;
        }
        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            uploadContent.classList.add('hidden');
            previewContainer.classList.remove('hidden');
            analyzeBtn.disabled = false;
            // Clear previous results
            resultsSection.classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }

    function resetUpload() {
        currentFile = null;
        fileInput.value = '';
        imagePreview.src = '';
        uploadContent.classList.remove('hidden');
        previewContainer.classList.add('hidden');
        analyzeBtn.disabled = true;
        resultsSection.classList.add('hidden');
    }

    analyzeBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        // Show loading
        loadingSection.classList.remove('hidden');
        analyzeBtn.disabled = true;
        resultsSection.classList.add('hidden');

        const formData = new FormData();
        formData.append('image', currentFile);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                alert('Analysis failed: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during analysis.');
        } finally {
            loadingSection.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    function displayResults(data) {
        resultsSection.classList.remove('hidden');

        // Gemini Agent Results
        const gemini = data.ai_detection;
        const geminiVerdict = document.getElementById('gemini-verdict');
        const geminiScore = document.getElementById('gemini-score');
        const geminiBar = document.getElementById('gemini-confidence');

        geminiVerdict.textContent = gemini.is_ai_generated ? 'YES' : 'NO';
        geminiVerdict.className = `value badge ${gemini.is_ai_generated ? 'negative' : 'positive'}`;

        geminiScore.textContent = `${gemini.confidence_score}%`;
        geminiBar.style.width = `${gemini.confidence_score}%`;

        document.getElementById('gemini-reasoning').textContent = gemini.reasoning;

        // Web Checker Agent Results
        const checker = data.misuse_check;
        const checkerVerdict = document.getElementById('checker-verdict');
        const checkerRisk = document.getElementById('checker-risk');

        checkerVerdict.textContent = checker.misuse_detected ? 'DETECTED' : 'CLEAR';
        checkerVerdict.className = `value badge ${checker.misuse_detected ? 'negative' : 'positive'}`;

        checkerRisk.textContent = checker.risk_level;
        // Simple color coding for risk
        checkerRisk.style.color = checker.risk_level === 'High' ? 'var(--accent-red)' :
            checker.risk_level === 'Medium' ? 'orange' : 'var(--accent-green)';

        document.getElementById('checker-details').textContent = checker.details;
    }
});
