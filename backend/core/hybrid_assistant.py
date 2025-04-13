from .context_engine import ContextManager
from .models import Message
from typing import List

class HybridAssistant:
    def __init__(self):
        self.context_manager = ContextManager()
        self.chat_history: List[Message] = []

    def receive_message(self, msg: Message):
        self.chat_history.append(msg)

        if self.context_manager.should_update(self.chat_history):
            context = self.context_manager.generate_context(self.chat_history)
        else:
            context = self.context_manager.get_context()

        # Combine context with the latest message
        payload = f"Context:\n{context}\n\nNew Message:\n{msg.content}"
        
        # Call the AI model here (mocked below)
        response = self.get_model_response(payload)

        # Save the response
        bot_msg = Message(sender="Assistant", content=response)
        self.chat_history.append(bot_msg)

        return bot_msg

    def get_model_response(self, prompt: str) -> str:
        # 🔁 Placeholder – integrate OpenAI, Claude, etc. later
        return f"(Mocked Response) You said: {prompt.splitlines()[-1]}"


# Think of it as the central coordinator that:

# Accepts user messages

# Decides whether to update memory

# Fetches relevant contexts

# Delegates responses to underlying chat models (OpenAI, Claude, etc.)

# Merges multiple contexts if needed (PDF, chatbot link, podcast…)