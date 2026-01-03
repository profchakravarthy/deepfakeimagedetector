import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
client = None

if GENAI_API_KEY:
    try:
        client = genai.Client(api_key=GENAI_API_KEY)
    except Exception as e:
        print(f"Error initializing GenAI client: {e}")
else:
    print("Warning: GENAI_API_KEY not found in environment variables. Agents will not function.")

# Use a model that supports vision
MODEL_NAME = "gemini-2.0-flash-exp" 

class GeminiAgent:
    """Agent specialized in detecting AI-generated images."""
    
    def __init__(self):
        self.client = client
        self.system_instruction = """
        You are an expert AI Forensics Analyst using 'Gemini 3' level reasoning. 
        Your task is to CRITICALLY analyze images for digital forgery and AI generation.
        
        DO NOT be polite. DO NOT give the benefit that it is real. Be skeptical.
        
        Scrutinize for:
        1. **SynthID / Watermarks**: Check for invisible AI watermarks.
        2. **Physics**: Impossible lighting, shadows, reflections.
        3. **Anatomy**: Malformed hands, teeth, eyes, hair melding into skin.
        4. **Texture**: "Plastic" or overly smooth skin, background blur anomalies.
        5. **Context**: Nonsensical text, objects blending into each other.

        Response JSON format:
        {
            "is_ai_generated": boolean, 
            "confidence_score": integer (0-100),
            "reasoning": "string"
        }
        """

    def analyze(self, image):
        if not self.client:
            return {"is_ai_generated": False, "confidence_score": 0, "reasoning": "API Key missing."}
            
        try:
            prompt = "Analyze this image. Is it AI-generated? probability > 50 means true. Return JSON."
            
            response = self.client.models.generate_content(
                model="gemini-3-pro-preview",
                contents=[prompt, image],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.4 # Lower temperature for analytical precision
                )
            )
            return self._parse_response(response.text)
        except Exception as e:
            print(f"GeminiAgent Error: {e}")
            return {"error": str(e), "is_ai_generated": False, "confidence_score": 0, "reasoning": "Analysis failed. Check server logs."}

    def _parse_response(self, text):
        import json
        try:
            clean_text = text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            # Fallback if boolean is missing or string
            if isinstance(data.get("is_ai_generated"), str):
                data["is_ai_generated"] = data["is_ai_generated"].lower() == "true"
            return data
        except:
             # Fallback heuristic
             lower_text = text.lower()
             is_ai = "yes" in lower_text or "true" in lower_text or "ai-generated" in lower_text
             return {
                "is_ai_generated": is_ai,
                "confidence_score": 50,
                "reasoning": text[:200]
            }

class AIImageWebCheckerAgent:
    """Agent specialized in checking for image misuse on the internet."""
    
    def __init__(self):
        self.client = client
        self.system_instruction = """
        You are the 'AI Image Web Checker'. Your goal is to identify potential misuse of an image on the internet.
        Since you cannot browse the live web in real-time without tools, you will analyze the image for:
        - Deepfakes of public figures (Policy violation potential).
        - Copyrighted characters appearing in unauthorized contexts.
        - Known hate symbols or extremist imagery.
        - NSF contents that might be distributed non-consensually.
        
        Provide a JSON response with:
        - "misuse_detected": boolean
        - "risk_level": string (Low, Medium, High)
        - "details": string (Explain potential misuse scenarios found or cleared)
        """

    def check(self, image):
        if not self.client:
            return {"misuse_detected": False, "risk_level": "Unknown", "details": "API Key missing."}

        try:
            prompt = "Check this image for misuse potential. Return JSON."
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=[prompt, image],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction
                )
            )
            return self._parse_response(response.text)
        except Exception as e:
            print(f"WebChecker Error: {e}")
            return {"error": str(e), "misuse_detected": False, "risk_level": "Unknown", "details": "Check failed. Check server logs."}

    def _parse_response(self, text):
        import json
        try:
            clean_text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except:
            return {
                "misuse_detected": False,
                "risk_level": "Low",
                "details": text[:200] + "..."
            }

gemini_agent = GeminiAgent()
web_checker_agent = AIImageWebCheckerAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        image = Image.open(file.stream)
        
        # Run agents (sequentially for this demo, could be parallel)
        ai_detection_result = gemini_agent.analyze(image)
        misuse_result = web_checker_agent.check(image)
        
        return jsonify({
            "ai_detection": ai_detection_result,
            "misuse_check": misuse_result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
