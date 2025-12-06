from abc import ABC, abstractmethod
import json
import os
from typing import Dict, Any

import google.generativeai as genai
from openai import OpenAI
from anthropic import Anthropic
import ollama

class LLMClient(ABC):
    @abstractmethod
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        pass

class GeminiClient(LLMClient):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        response = self.model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

class AnthropicClient(LLMClient):
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        # Anthropic doesn't enforce JSON mode strictly like OpenAI/Gemini, 
        # so we rely on the prompt and parsing.
        # Ideally, we'd extract the JSON block.
        content = response.content[0].text
        # Simple heuristic to find JSON start/end if there's extra text
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(content[start:end])
            return json.loads(content)
        except json.JSONDecodeError:
             raise ValueError(f"Failed to parse JSON from Anthropic response: {content[:100]}...")

class OllamaClient(LLMClient):
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        response = ollama.chat(model=self.model_name, messages=[
          {
            'role': 'user',
            'content': prompt,
          },
        ], format='json')
        return json.loads(response['message']['content'])

def get_llm_client(provider: str, api_key: str = None, model_name: str = None) -> LLMClient:
    provider = provider.lower()
    if provider == "gemini":
        return GeminiClient(api_key)
    elif provider == "openai":
        return OpenAIClient(api_key)
    elif provider == "anthropic":
        return AnthropicClient(api_key)
    elif provider == "ollama":
        return OllamaClient(model_name or "llama3")
    else:
        raise ValueError(f"Unsupported provider: {provider}")
