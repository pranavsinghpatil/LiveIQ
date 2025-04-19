import sys
print("\n".join(sys.path))

from core.llm.llm_client import chat

response = chat(
    messages=[
        {"role": "user", "content": "What are the insights of the ai revolution?"},
    ],
    provider="google",  # or "openai", "anthropic", etc.
)

print(response)