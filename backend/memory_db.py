"""
Temporary in-memory memory store for hybrid chat messages.
Will be replaced by persistent vector DB in production.
"""

from collections import defaultdict

# Dict structure: { hybrid_id: [msg1, msg2, ...] }
chat_memory = defaultdict(list)

