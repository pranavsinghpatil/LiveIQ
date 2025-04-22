"""
Chat Ingestor Service
Handles all incoming media (text, files, links) and extracts content.
"""

import os
from typing import Dict, Any
from app.utils.media_processor import media_processor
import tempfile
import logging
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

class ChatIngestor:
    """
    A unified service that ingests different media types for chat creation.
    """

    async def ingest(self, media_type: str, content: str = None, file_path: str = None, file_type: str = None) -> dict:
        try:
            if media_type == "file":
                logger.info(f"Ingesting file: {file_path} of type {file_type}")

                if file_type and "image" in file_type:
                    from PIL import Image
                    import pytesseract

                    img = Image.open(file_path)
                    extracted_text = pytesseract.image_to_string(img)
                    return {
                        "content": extracted_text.strip(),
                        "metadata": {"source": "OCR"},
                        "created_at": datetime.utcnow().isoformat()
                    }

                elif file_type in ["application/pdf"]:
                    import fitz  # PyMuPDF
                    doc = fitz.open(file_path)
                    text = "\n".join([page.get_text() for page in doc])
                    return {
                        "content": text.strip(),
                        "metadata": {"source": "PDF"},
                        "created_at": datetime.utcnow().isoformat()
                    }

                else:
                    return {
                        "content": None,
                        "metadata": {"error": "Unsupported or binary file type"}
                    }

            elif media_type == "text":
                return {
                    "content": content,
                    "metadata": {"source": "form"},
                    "created_at": datetime.utcnow().isoformat()
                }

            else:
                return {
                    "content": None,
                    "metadata": {"error": "Unsupported media_type"}
                }

        except Exception as e:
            logger.error("Error in chat_ingestor.ingest(): %s", str(e))
            traceback.print_exc()
            return {
                "content": None,
                "metadata": {"error": str(e)}
            }


# Singleton export
chat_ingestor = ChatIngestor()

# Optional: CLI Debugging Utility
if __name__ == "__main__":
    import sys, asyncio
    path = sys.argv[1]
    print(asyncio.run(ChatIngestor().ingest("file", None, path, "image/jpeg")))
