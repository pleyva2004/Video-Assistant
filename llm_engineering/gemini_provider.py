import os
from typing import Optional, List

from dotenv import load_dotenv
import google.generativeai as genai

class GeminiClient:
    def __init__(self):
        # Load the .env file from the project root
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure the API key (new way)
        genai.configure(api_key=api_key)
        
        # Initialize the model (new way)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def generate_text(self, prompt: str, system_instruction: Optional[str] = None, 
                     temperature: float = 0.7, top_p: float = 0.95, 
                     top_k: int = 40, max_output_tokens: int = 1000) -> str:
        
        # Create generation config (correct import)
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens,
        )
        
        # Create model with system instruction if provided
        if system_instruction:
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                system_instruction=system_instruction
            )
        else:
            model = self.model
            
        # Generate content (correct method)
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text
    
    def ask_with_context(self, question: str, chunks: List[str], 
                        model_name: str = "gemini-1.5-flash") -> str:
        """Method compatible with your existing interface"""
        context = "\n\n".join(chunks)
        prompt = f"""Answer the following question using the transcript context below:

        Context:
        {context}

        Question: {question}
        """
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    
    def close(self):
        """Close method for consistency"""
        pass 