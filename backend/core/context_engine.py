from .models import Message
from typing import List
from datetime import datetime, timedelta

class ContextManager:
    def __init__(self):
        self.last_update: datetime = datetime.now()
        self.cache_summary = ""

    def should_update(self, messages: List[Message], threshold=5, minutes_gap=2):
        # Update context if enough new messages OR time gap exceeded
        time_since_last = datetime.now() - self.last_update
        if len(messages) >= threshold or time_since_last > timedelta(minutes=minutes_gap):
            return True
        return False

    def generate_context(self, messages: List[Message]):
        """Naive summarization for now (can plug in OpenAI/GPT later)"""
        recent_msgs = messages[-10:]  # Last 10 msgs for context
        summary = "\n".join([f"{msg.sender}: {msg.content}" for msg in recent_msgs])
        self.cache_summary = summary
        self.last_update = datetime.now()
        return summary

    def get_context(self):
        return self.cache_summary

# This file does:

# Keeps memory updated after every new message

# Applies a benchmarking rule (e.g., after 5 messages or every N mins)

# Summarizes context so far

# Lets hybrid assistant recall older stuff smartly
# --------------------------------------------
# Replace naive summarization with GPT or langchain summarizer

# Use Redis or Supabase to persist summaries