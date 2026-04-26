import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

class GeminiVLMClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            print("Warning: GEMINI_API_KEY not found in environment or passed to constructor")

    def guess_celebrity(self, image: Image.Image) -> str:
        """
        Guesses the celebrity in the image using Gemini 2.5 Flash.
        """
        if not self.api_key:
            return "Error: Gemini API Key is missing. Please set GEMINI_API_KEY in your environment or enter it in the sidebar."

        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = """
        Identify the celebrity in this image. 
        If you recognize them, provide:
        1. Name
        2. Brief description/claim to fame
        3. A fun fact if available.
        
        If you don't recognize any celebrity, just say so.
        """
        
        try:
            response = model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f"Error identifying celebrity: {str(e)}"

    def analyze_image(self, image: Image.Image, prompt: str) -> str:
        """
        General image analysis using Gemini 2.5 Flash.
        """
        if not self.api_key:
            return "Error: Gemini API Key is missing."

        model = genai.GenerativeModel('gemini-2.5-flash')
        
        try:
            response = model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
