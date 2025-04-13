from .models import ChatThread, Message
from typing import Dict
from uuid import uuid4
from datetime import datetime

# In-memory simulation (replace with Supabase later)
THREADS: Dict[str, ChatThread] = {}

def create_thread(title=None, source=None):
    thread_id = str(uuid4())
    THREADS[thread_id] = ChatThread(id=thread_id, title=title, source=source, messages=[])
    return THREADS[thread_id]

def add_message(thread_id, sender, content, metadata=None):
    msg = Message(
        id=str(uuid4()),
        sender=sender,
        content=content,
        timestamp=datetime.now(),
        metadata=metadata or {}
    )
    THREADS[thread_id].messages.append(msg)
    return msg

def link_threads(primary_id, secondary_id):
    THREADS[primary_id].linked_thread_ids.append(secondary_id)

def get_merged_thread(thread_id):
    base = THREADS[thread_id]
    all_msgs = list(base.messages)

    for linked_id in base.linked_thread_ids:
        linked_thread = THREADS.get(linked_id)
        if linked_thread:
            all_msgs.extend(linked_thread.messages)

    # Sort messages by time
    all_msgs.sort(key=lambda msg: msg.timestamp)
    return all_msgs


# This handles:

# Creating threads

# Adding messages

# Linking threads

# Retrieving hybrid views