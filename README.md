# Nano Banana Pro - AI Image Analysis App

A high-aesthetic web application leveraging **Google Gemini 3 Pro** and **Gemini 2.0 Flash** agents to perform advanced AI forensics and web integrity checks on images.

![App Screenshot](https://via.placeholder.com/800x400?text=Nano+Banana+Pro+UI+Preview)

## 🚀 Features

*   **Dual-Agent System**:
    *   **Gemini Agent**: Uses rigorous "Gemini 3 Pro" reasoning to detect AI artifacts (synths, lighting, anatomy).
    *   **AI Image Web Checker**: Simulates a web integrity check for deepfakes, copyright misuse, and sensitive content.
*   **Premium UI**: Fully responsive, dark-mode interface with "Nano Banana" yellow accents, glassmorphism, and smooth animations.
*   **Real-time Analysis**: Drag-and-drop interface with instant feedback.
*   **Modern Tech Stack**: Built with Flask and the latest `google-genai` SDK.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/nano-banana-pro.git
    cd nano-banana-pro/nano_banana_app
    ```

2.  **Install Dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**:
    *   Rename `.env.example` to `.env`.
    *   Add your Google GenAI API Key:
        ```env
        GENAI_API_KEY=your_actual_api_key_here
        ```
    *   *Note*: Ensure your key has access to `gemini-3-pro-preview` and `gemini-2.0-flash-exp`.

## 🏃‍♂️ Usage

1.  Start the Flask server:
    ```bash
    python app.py
    ```
2.  Open your browser and navigate to:
    `http://127.0.0.1:5000`
3.  Upload an image to see the agents in action!

## 🔧 Tech Stack

*   **Backend**: Python, Flask, Google GenAI SDK
*   **Frontend**: HTML5, Vanilla CSS3, Vanilla JavaScript
*   **AI Models**: Gemini 3 Pro Preview, Gemini 2.0 Flash Exp

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)
