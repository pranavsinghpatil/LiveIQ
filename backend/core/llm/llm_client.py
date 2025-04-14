"""
LLM Client for VoxStitch
Provides a unified interface to multiple LLM providers
"""

import os
import json
import logging
import time
import sys
from typing import Dict, List, Optional, Union, Any, Tuple
from enum import Enum
import requests
from dotenv import load_dotenv
from dataclasses import dataclass
from functools import wraps

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import LLM libraries
try:
    import openai
except ImportError:
    openai = None
    logger.warning("OpenAI library not installed. OpenAI models will not be available.")

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    logger.warning("Google Generative AI library not installed. Gemini models will not be available.")

try:
    import anthropic
except ImportError:
    anthropic = None
    logger.warning("Anthropic library not installed. Claude models will not be available.")

try:
    import mistralai.client
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage
except ImportError:
    mistralai = None
    MistralClient = None
    ChatMessage = None
    logger.warning("Mistral AI library not installed. Mistral models will not be available.")

try:
    import deepseek
except ImportError:
    deepseek = None
    logger.warning("DeepSeek library not installed. DeepSeek models will not be available.")

class LLMClientError(Exception):
    """Custom exception class for LLM client errors"""
    pass

class ModelProvider(str, Enum):
    """Enum for supported model providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MISTRAL = "mistral"
    GOOGLE = "google"
    DEEPSEEK = "deepseek"

# Default models for each provider
DEFAULT_MODELS = {
    ModelProvider.OPENAI: "gpt-3.5-turbo",
    ModelProvider.ANTHROPIC: "claude-3-opus-20240229",
    ModelProvider.MISTRAL: "mistral-large-latest",
    ModelProvider.GOOGLE: "gemini-1.5-pro",
    ModelProvider.DEEPSEEK: "deepseek-chat"
}

# Request timeouts and retry configuration
REQUEST_TIMEOUT = 60  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

@dataclass
class Message:
    """Message class for unified interface"""
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        """For backward compatibility"""
        return {"role": self.role, "content": self.content}

def retry_on_error(max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Decorator for retrying API calls on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (requests.RequestException, TimeoutError) as e:
                    retries += 1
                    if retries >= max_retries:
                        raise LLMClientError(f"Failed after {max_retries} retries: {str(e)}")
                    logger.warning(f"Retry {retries}/{max_retries} after error: {str(e)}")
                    time.sleep(delay)
        return wrapper
    return decorator

class LLMClient:
    """Unified client for multiple LLM providers"""
    
    def __init__(self, user_api_keys: Optional[Dict[str, str]] = None):
        """
        Initialize LLM client with API keys from environment variables
        
        Args:
            user_api_keys: Optional dictionary of user-provided API keys that override environment variables
                           Format: {"openai": "sk-...", "google": "..."}
        """
        # Load API keys from environment variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "YOUR_DEFAULT_GEMINI_API_KEY")  # Default Gemini API key
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        
        # Override with user-provided API keys if available
        if user_api_keys:
            if "openai" in user_api_keys:
                self.openai_api_key = user_api_keys["openai"]
            if "anthropic" in user_api_keys:
                self.anthropic_api_key = user_api_keys["anthropic"]
            if "mistral" in user_api_keys:
                self.mistral_api_key = user_api_keys["mistral"]
            if "google" in user_api_keys:
                self.google_api_key = user_api_keys["google"]
            if "deepseek" in user_api_keys:
                self.deepseek_api_key = user_api_keys["deepseek"]
        
        # Initialize clients
        self._init_clients()
        
    def _init_clients(self):
        """Initialize API clients for each provider"""
        # OpenAI
        if self.openai_api_key and openai is not None:
            try:
                openai.api_key = self.openai_api_key
                logger.info("OpenAI client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        
        # Anthropic (Claude)
        if self.anthropic_api_key and anthropic is not None:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
                logger.info("Anthropic client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")
                self.anthropic_client = None
        else:
            self.anthropic_client = None
            
        # Mistral
        if self.mistral_api_key and MistralClient is not None:
            try:
                self.mistral_client = MistralClient(api_key=self.mistral_api_key)
                logger.info("Mistral client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Mistral client: {e}")
                self.mistral_client = None
        else:
            self.mistral_client = None
            
        # Google (Gemini)
        if self.google_api_key and genai is not None:
            try:
                genai.configure(api_key=self.google_api_key)
                logger.info("Google Gemini client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Google Gemini client: {e}")
        
        # DeepSeek
        if self.deepseek_api_key and deepseek is not None:
            try:
                # DeepSeek client initialization (using REST API approach)
                logger.info("DeepSeek client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize DeepSeek client: {e}")
    
    def generate_text(self, 
                     prompt: str, 
                     provider: ModelProvider = ModelProvider.GOOGLE,  # Default to Google Gemini
                     model: Optional[str] = None,
                     max_tokens: int = 1000,
                     temperature: float = 0.7) -> str:
        """
        Generate text using the specified provider and model
        
        Args:
            prompt: The text prompt
            provider: The model provider (OpenAI, Anthropic, etc.)
            model: The specific model to use (defaults to provider's default)
            max_tokens: Maximum tokens in the response
            temperature: Temperature for response generation
            
        Returns:
            Generated text response
            
        Raises:
            LLMClientError: If there's an error with the LLM API
        """
        try:
            if provider == ModelProvider.OPENAI:
                return self._generate_openai(prompt, model, max_tokens, temperature)
            elif provider == ModelProvider.ANTHROPIC:
                return self._generate_anthropic(prompt, model, max_tokens, temperature)
            elif provider == ModelProvider.MISTRAL:
                return self._generate_mistral(prompt, model, max_tokens, temperature)
            elif provider == ModelProvider.GOOGLE:
                return self._generate_google(prompt, model, max_tokens, temperature)
            elif provider == ModelProvider.DEEPSEEK:
                return self._generate_deepseek(prompt, model, max_tokens, temperature)
            else:
                raise LLMClientError(f"Unsupported provider: {provider}")
        except Exception as e:
            if not isinstance(e, LLMClientError):
                raise LLMClientError(f"Error generating text with {provider}: {str(e)}")
            raise
    
    def chat(self,
            messages: List[Message],
            provider: ModelProvider = ModelProvider.GOOGLE,  # Default to Google Gemini
            model: Optional[str] = None,
            max_tokens: int = 1000,
            temperature: float = 0.7) -> str:
        """
        Generate a chat response using the specified provider and model
        
        Args:
            messages: List of messages in the conversation
            provider: The model provider (OpenAI, Anthropic, etc.)
            model: The specific model to use (defaults to provider's default)
            max_tokens: Maximum tokens in the response
            temperature: Temperature for response generation
            
        Returns:
            Generated chat response
            
        Raises:
            LLMClientError: If there's an error with the LLM API
        """
        try:
            if provider == ModelProvider.OPENAI:
                return self._chat_openai(messages, model, max_tokens, temperature)
            elif provider == ModelProvider.ANTHROPIC:
                return self._chat_anthropic(messages, model, max_tokens, temperature)
            elif provider == ModelProvider.MISTRAL:
                return self._chat_mistral(messages, model, max_tokens, temperature)
            elif provider == ModelProvider.GOOGLE:
                return self._chat_google(messages, model, max_tokens, temperature)
            elif provider == ModelProvider.DEEPSEEK:
                return self._chat_deepseek(messages, model, max_tokens, temperature)
            else:
                raise LLMClientError(f"Unsupported provider: {provider}")
        except Exception as e:
            if not isinstance(e, LLMClientError):
                raise LLMClientError(f"Error generating chat response with {provider}: {str(e)}")
            raise
    
    # OpenAI implementation
    def _generate_openai(self, prompt: str, model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text using OpenAI"""
        if openai is None:
            raise LLMClientError("OpenAI library not installed. Please install openai.")
        if not self.openai_api_key:
            raise LLMClientError("OpenAI API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.OPENAI]
        
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise LLMClientError(f"OpenAI generation failed: {str(e)}")
    
    def _chat_openai(self, messages: List[Message], model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate chat response using OpenAI"""
        if openai is None:
            raise LLMClientError("OpenAI library not installed. Please install openai.")
        if not self.openai_api_key:
            raise LLMClientError("OpenAI API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.OPENAI]
        
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[m.to_dict() for m in messages],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise LLMClientError(f"OpenAI chat failed: {str(e)}")
    
    # Anthropic (Claude) implementation
    def _generate_anthropic(self, prompt: str, model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text using Anthropic Claude"""
        if anthropic is None:
            raise LLMClientError("Anthropic library not installed. Please install anthropic.")
        if not self.anthropic_client:
            raise LLMClientError("Anthropic API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.ANTHROPIC]
        
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise LLMClientError(f"Anthropic generation failed: {str(e)}")
    
    def _chat_anthropic(self, messages: List[Message], model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate chat response using Anthropic Claude"""
        if anthropic is None:
            raise LLMClientError("Anthropic library not installed. Please install anthropic.")
        if not self.anthropic_client:
            raise LLMClientError("Anthropic API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.ANTHROPIC]
        
        # Convert to Anthropic format
        anthropic_messages = []
        for msg in messages:
            role = "user" if msg.role in ["user", "human"] else "assistant"
            anthropic_messages.append({"role": role, "content": msg.content})
        
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=anthropic_messages
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise LLMClientError(f"Anthropic chat failed: {str(e)}")
    
    # Mistral implementation
    def _generate_mistral(self, prompt: str, model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text using Mistral AI"""
        if MistralClient is None or ChatMessage is None:
            raise LLMClientError("Mistral AI library not installed. Please install mistralai.")
        if not self.mistral_client:
            raise LLMClientError("Mistral API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.MISTRAL]
        
        try:
            chat_response = self.mistral_client.chat(
                model=model,
                messages=[ChatMessage(role="user", content=prompt)],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            logger.error(f"Mistral API error: {e}")
            raise LLMClientError(f"Mistral generation failed: {str(e)}")
    
    def _chat_mistral(self, messages: List[Message], model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate chat response using Mistral AI"""
        if MistralClient is None or ChatMessage is None:
            raise LLMClientError("Mistral AI library not installed. Please install mistralai.")
        if not self.mistral_client:
            raise LLMClientError("Mistral API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.MISTRAL]
        
        # Convert to Mistral format
        mistral_messages = []
        for msg in messages:
            role = "user" if msg.role in ["user", "human"] else "assistant"
            mistral_messages.append(ChatMessage(role=role, content=msg.content))
        
        try:
            chat_response = self.mistral_client.chat(
                model=model,
                messages=mistral_messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            logger.error(f"Mistral API error: {e}")
            raise LLMClientError(f"Mistral chat failed: {str(e)}")
    
    # Google (Gemini) implementation
    @retry_on_error()
    def _generate_google(self, prompt: str, model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text using Google Gemini"""
        if genai is None:
            raise LLMClientError("Google Generative AI library not installed. Please install google-generativeai.")
        if not self.google_api_key:
            raise LLMClientError("Google API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.GOOGLE]
        
        try:
            gemini_model = genai.GenerativeModel(model_name=model)
            response = gemini_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Google Gemini API error: {e}")
            raise LLMClientError(f"Google Gemini generation failed: {str(e)}")
    
    @retry_on_error()
    def _chat_google(self, messages: List[Message], model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate chat response using Google Gemini"""
        if genai is None:
            raise LLMClientError("Google Generative AI library not installed. Please install google-generativeai.")
        if not self.google_api_key:
            raise LLMClientError("Google API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.GOOGLE]
        
        try:
            gemini_model = genai.GenerativeModel(model_name=model)
            
            # Convert to Gemini format
            gemini_messages = []
            for msg in messages:
                role = "user" if msg.role in ["user", "human"] else "model"
                gemini_messages.append({"role": role, "parts": [msg.content]})
            
            chat = gemini_model.start_chat(history=gemini_messages)
            response = chat.send_message(
                "",  # Empty message to get response based on history
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Google Gemini API error: {e}")
            raise LLMClientError(f"Google Gemini chat failed: {str(e)}")
    
    # DeepSeek implementation
    @retry_on_error()
    def _generate_deepseek(self, prompt: str, model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text using DeepSeek"""
        if deepseek is None:
            raise LLMClientError("DeepSeek library not installed. Please install deepseek.")
        if not self.deepseek_api_key:
            raise LLMClientError("DeepSeek API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.DEEPSEEK]
        
        try:
            # Using REST API approach since Python SDK might not be available
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                raise LLMClientError(f"DeepSeek API error: {response.text}")
                
            response_json = response.json()
            return response_json["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            logger.error(f"DeepSeek API request error: {e}")
            raise LLMClientError(f"DeepSeek generation failed (request error): {str(e)}")
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            raise LLMClientError(f"DeepSeek generation failed: {str(e)}")
    
    @retry_on_error()
    def _chat_deepseek(self, messages: List[Message], model: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate chat response using DeepSeek"""
        if deepseek is None:
            raise LLMClientError("DeepSeek library not installed. Please install deepseek.")
        if not self.deepseek_api_key:
            raise LLMClientError("DeepSeek API key not configured")
        model = model or DEFAULT_MODELS[ModelProvider.DEEPSEEK]
        
        try:
            # Using REST API approach
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            # Convert to DeepSeek format
            deepseek_messages = []
            for msg in messages:
                role = "user" if msg.role in ["user", "human"] else "assistant"
                deepseek_messages.append({"role": role, "content": msg.content})
            
            data = {
                "model": model,
                "messages": deepseek_messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                raise LLMClientError(f"DeepSeek API error: {response.text}")
                
            response_json = response.json()
            return response_json["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            logger.error(f"DeepSeek API request error: {e}")
            raise LLMClientError(f"DeepSeek chat failed (request error): {str(e)}")
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            raise LLMClientError(f"DeepSeek chat failed: {str(e)}")

# Create a singleton instance
llm_client = LLMClient()

# Convenience functions
def generate_text(prompt: str, provider: str = "google", model: Optional[str] = None) -> str:
    """Generate text using the specified provider and model (default: Google Gemini)"""
    return llm_client.generate_text(prompt, ModelProvider(provider), model)

def chat(messages: List[Dict[str, str]], provider: str = "google", model: Optional[str] = None) -> str:
    """Generate a chat response using the specified provider and model (default: Google Gemini)"""
    # Convert dict messages to Message objects
    msg_objects = [Message(m["role"], m["content"]) for m in messages]
    return llm_client.chat(msg_objects, ModelProvider(provider), model)

# Function to update API keys at runtime
def set_api_key(provider: str, api_key: str):
    """Set or update an API key for a specific provider at runtime"""
    global llm_client
    
    if provider == "openai":
        llm_client.openai_api_key = api_key
        if hasattr(openai, "api_key"):
            openai.api_key = api_key
    elif provider == "anthropic" and hasattr(llm_client, "anthropic_client"):
        llm_client.anthropic_api_key = api_key
        llm_client.anthropic_client = anthropic.Anthropic(api_key=api_key)
    elif provider == "mistral" and hasattr(llm_client, "mistral_client"):
        llm_client.mistral_api_key = api_key
        llm_client.mistral_client = MistralClient(api_key=api_key)
    elif provider == "google":
        llm_client.google_api_key = api_key
        if "google.generativeai" in sys.modules:
            genai.configure(api_key=api_key)
    elif provider == "deepseek":
        llm_client.deepseek_api_key = api_key
    else:
        raise LLMClientError(f"Unsupported provider: {provider}")
    
    logger.info(f"Updated API key for {provider}")

# Create a new client with user-provided API keys
def create_client_with_user_keys(user_api_keys: Dict[str, str]) -> LLMClient:
    """Create a new LLM client with user-provided API keys"""
    return LLMClient(user_api_keys=user_api_keys)
