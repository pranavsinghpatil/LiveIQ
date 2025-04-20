"""
Test script to verify Supabase connection and operations.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json
import uuid

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL exists: {SUPABASE_URL is not None}")
print(f"SUPABASE_KEY exists: {SUPABASE_KEY is not None}")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: Missing Supabase credentials in .env file")
    exit(1)

# Create Supabase client
try:
    print("Creating Supabase client...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client created successfully!")
except Exception as e:
    print(f"ERROR creating Supabase client: {str(e)}")
    exit(1)

# Test inserting a record
try:
    print("\nTesting insert operation...")
    test_id = str(uuid.uuid4())[:8]  # Generate a short unique ID
    
    # Create test data
    test_data = {
        "user_id": "test_user_" + test_id,
        "title": "Test Chat " + test_id,
        "content": "This is a test chat content",
        "media_type": "text",
        "created_at": "2025-04-20T08:00:00"
    }
    
    print(f"Inserting test data: {json.dumps(test_data, indent=2)}")
    
    # Insert into chats table
    insert_result = supabase.table("chats").insert(test_data).execute()
    
    # Check for errors
    if hasattr(insert_result, 'error') and insert_result.error:
        print(f"ERROR during insert: {insert_result.error}")
        exit(1)
    
    # Print the result
    print("Insert successful!")
    print(f"Response data: {json.dumps(insert_result.data, indent=2)}")
    
    # Check if ID was returned
    if insert_result.data and len(insert_result.data) > 0:
        inserted_id = insert_result.data[0].get("id")
        print(f"Inserted record ID: {inserted_id}")
    else:
        print("WARNING: No data returned from insert operation")
    
    # Test select operation
    print("\nTesting select operation...")
    select_result = supabase.table("chats").select("*").eq("user_id", test_data["user_id"]).execute()
    
    if hasattr(select_result, 'error') and select_result.error:
        print(f"ERROR during select: {select_result.error}")
    else:
        print(f"Select returned {len(select_result.data)} records")
        print(f"First record: {json.dumps(select_result.data[0] if select_result.data else {}, indent=2)}")
    
except Exception as e:
    print(f"ERROR during test operations: {str(e)}")

print("\nTest completed!")
