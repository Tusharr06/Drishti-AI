import base64
import io
import ollama
from PIL import Image
import time
from typing import Optional, Dict, Any, List
import logging

class OllamaVLMClient:
    def __init__(self, host: str = "localhost", port: int = 11434):
        self.client = ollama
        self.host = host
        self.port = port
        self.available_models = []
        self._check_connection()
    
    def _check_connection(self) -> bool:
        try:
            self.available_models = [model['name'] for model in self.client.list()['models']]
            return True
        except Exception as e:
            logging.warning(f"Could not connect to Ollama: {e}")
            return False
    
    def get_available_models(self) -> List[str]:
        try:
            models = self.client.list()
            return [model['name'] for model in models['models']]
        except Exception:
            return ["llava:7b", "llava:13b", "llava-phi3", "bakllava", "minicpm-v", "moondream"]
    
    def check_model_availability(self, model: str) -> bool:
        try:
            available = self.get_available_models()
            return model in available
        except Exception:
            return False
    
    def pull_model(self, model: str) -> bool:
        try:
            self.client.pull(model)
            return True
        except Exception as e:
            logging.error(f"Failed to pull model {model}: {e}")
            return False
    
    def summarize_image(
        self, 
        image: Image.Image, 
        prompt: str = "Describe this image succinctly", 
        model: str = "llava:7b", 
        temperature: float = 0.2, 
        max_tokens: int = 200,
        system_prompt: Optional[str] = None
    ) -> str:
        try:
            if not self.check_model_availability(model):
                raise Exception(f"Model {model} is not available. Please pull it first using: ollama pull {model}")
            
            buffer = io.BytesIO()
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image.save(buffer, format="JPEG", quality=95, optimize=True)
            image_bytes = buffer.getvalue()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({
                "role": "user", 
                "content": prompt, 
                "images": [image_b64]
            })
            
            options = {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_k": 40,
                "top_p": 0.9,
                "repeat_penalty": 1.1
            }
            
            response = self.client.chat(
                model=model, 
                messages=messages, 
                options=options,
                stream=False
            )
            
            result = response.get("message", {}).get("content") or response.get("content")
            
            if not result:
                raise Exception("No response content received from model")
            
            return result.strip()
            
        except Exception as e:
            raise Exception(f"VLM analysis error: {str(e)}")
    
    def batch_analyze_images(
        self, 
        images: List[Image.Image], 
        prompts: List[str], 
        model: str = "llava:7b",
        **kwargs
    ) -> List[Dict[str, Any]]:
        results = []
        
        for i, (image, prompt) in enumerate(zip(images, prompts)):
            try:
                start_time = time.time()
                result = self.summarize_image(image, prompt, model, **kwargs)
                processing_time = time.time() - start_time
                
                results.append({
                    'index': i,
                    'success': True,
                    'result': result,
                    'processing_time': processing_time,
                    'error': None
                })
            except Exception as e:
                results.append({
                    'index': i,
                    'success': False,
                    'result': None,
                    'processing_time': 0,
                    'error': str(e)
                })
        
        return results
    
    def get_model_info(self, model: str) -> Dict[str, Any]:
        try:
            info = self.client.show(model)
            return {
                'name': model,
                'size': info.get('size', 'Unknown'),
                'family': info.get('details', {}).get('family', 'Unknown'),
                'parameter_count': info.get('details', {}).get('parameter_size', 'Unknown'),
                'quantization': info.get('details', {}).get('quantization_level', 'Unknown')
            }
        except Exception as e:
            return {'name': model, 'error': str(e)}
    
    def estimate_processing_time(self, image: Image.Image, model: str = "llava:7b") -> float:
        width, height = image.size
        pixel_count = width * height
        
        base_times = {
            "llava:7b": 2.0,
            "llava:13b": 4.0,
            "llava:34b": 8.0,
            "llava-phi3": 1.5,
            "bakllava": 3.0,
            "minicpm-v": 2.5,
            "moondream": 1.0
        }
        
        base_time = base_times.get(model, 3.0)
        
        if pixel_count > 1000000:
            base_time *= 1.5
        elif pixel_count > 500000:
            base_time *= 1.2
        
        return base_time
