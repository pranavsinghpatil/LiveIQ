"""
Database configuration and connection management for VoxStitch.
"""

import os
from dotenv import load_dotenv
import supabase

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Supabase Storage Bucket
BUCKET_NAME = "voxstitch-uploads"
