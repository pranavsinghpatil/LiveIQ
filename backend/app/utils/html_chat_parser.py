from bs4 import BeautifulSoup
from typing import List, Dict
import datetime
import os

def parse_chatgpt_html(filepath: str) -> List[Dict[str, str]]:
    """Extracts a conversation thread from a ChatGPT .html file"""
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    chat_data = []
    blocks = soup.find_all("div", class_="markdown")

    for block in blocks:
        role = "assistant" if "AIAnswer" in block.parent.get("class", []) else "user"
        content = block.get_text(separator="\n").strip()
        chat_data.append({
            "role": role,
            "content": content
        })

    return chat_data

def detect_html_chat_source(filepath: str) -> str:
    """
    Attempts to detect the AI chat platform from an exported HTML file.
    Returns one of: 'chatgpt', 'gemini', 'claude', 'grok', or 'unknown'.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read().lower()
    if "chat.openai.com" in html or "chatgpt" in html:
        return "chatgpt"
    if "gemini.google.com" in html or "gemini ai" in html:
        return "gemini"
    if "claude" in html or "anthropic" in html:
        return "claude"
    if "grok" in html or "x.ai" in html:
        return "grok"
    return "unknown"

# Later: Add more parsers for other platforms as needed
