"""
Chat Ingestor Service
Handles all incoming media (text, files, links) and extracts content.
"""

import os
from typing import Dict, Any
from app.utils.media_processor import media_processor
import tempfile


class ChatIngestor:
    """
    A unified service that ingests different media types for chat creation.
    """

    async def ingest(self, media_type: str, content: str = None, file_path: str = None, file_type: str = None) -> Dict[str, Any]:
        """
        Ingest a chat from various media types.

        Args:
            media_type: "text", "file", or "link"
            content: Text content or link URL
            file_path: Path to uploaded file
            file_type: MIME type of the file

        Returns:
            Dict with normalized `type`, `content`, `metadata`
        """

        if media_type == "text":
            if not content:
                raise ValueError("No content provided for text upload")
            return {
                "type": "text",
                "content": content,
                "metadata": {}
            }

        elif media_type == "file":
            if not file_path:
                raise ValueError("File path required for file uploads")
            return await media_processor.process_file(file_path)

        elif media_type == "link":
            if not content:
                raise ValueError("No URL provided for link import")
            return await media_processor.process_link(content)

        else:
            raise ValueError(f"Unsupported media type: {media_type}")


# Singleton export
chat_ingestor = ChatIngestor()
