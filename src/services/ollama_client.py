import base64
import io
import ollama
from PIL import Image

class OllamaVLMClient:
    def __init__(self):
        self.client = ollama

    def summarize_image(self, image, prompt="Describe this image succinctly", model="llava:7b", temperature=0.2, max_tokens=200):
        try:
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=90)
            image_bytes = buffer.getvalue()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            messages = [{"role": "user", "content": prompt, "images": [image_b64]}]
            response = self.client.chat(model=model, messages=messages, options={"temperature": temperature, "num_predict": max_tokens})
            return response.get("message", {}).get("content") or response.get("content")
        except Exception as e:
            raise Exception(f"VLM error: {e}")
