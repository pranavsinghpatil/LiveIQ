"""
Supabase client configuration for VoxStitch.
"""

from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing required Supabase environment variables")

# === DEV-ONLY: SUPABASE RATE-LIMIT BYPASS ===
# In development, all supabase requests use the SERVICE_ROLE_KEY for rate-limit-free access.
# REMOVE THIS BLOCK IN PRODUCTION!
SUPABASE_RATE_FREE = os.getenv("SUPABASE_RATE_FREE", "true").lower() == "true"

# Accept SUPABASE_KEY as the service role key if SERVICE_ROLE_KEY is not set
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if SUPABASE_RATE_FREE:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    if SUPABASE_URL and SERVICE_ROLE_KEY:
        supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    else:
        raise RuntimeError("SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_KEY) not set for rate-free mode!")
else:
# === END DEV-ONLY BLOCK ===   
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
