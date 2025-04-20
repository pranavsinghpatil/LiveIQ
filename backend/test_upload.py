"""
Test script to verify the /api/chats/upload endpoint.
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API endpoint
API_URL = "http://localhost:8000/upload"

def test_upload_text():
    """Test uploading text content"""
    
    # Prepare form data
    form_data = {
        "user_id": "test_user_upload",
        "title": "Test Upload via Script",
        "media_type": "text",
        "content": "This is a test content uploaded via script"
    }
    
    print(f"Sending POST request to {API_URL} with data:")
    print(json.dumps(form_data, indent=2))
    
    # Send POST request
    response = requests.post(API_URL, data=form_data)
    
    # Print response
    print(f"\nResponse status code: {response.status_code}")
    
    try:
        response_json = response.json()
        print(f"Response JSON: {json.dumps(response_json, indent=2)}")
        
        # Check if ID is in the response
        if response_json.get("status") == "success":
            data = response_json.get("data", {})
            if "id" in data and data["id"]:
                print(f"\n✅ SUCCESS: ID was returned: {data['id']}")
            else:
                print("\n❌ ERROR: No ID was returned in the response")
        else:
            print(f"\n❌ ERROR: Response status is not 'success'")
    except Exception as e:
        print(f"\n❌ ERROR parsing response: {str(e)}")
        print(f"Raw response: {response.text}")

if __name__ == "__main__":
    test_upload_text()
