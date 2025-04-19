"""
Media processing utilities for VoxStitch.
Handles processing of various media types including PDFs, images, videos, and links.
"""

import os
from typing import Dict, Any, Optional
import pytesseract
from PIL import Image
import fitz  # PyMuPDF for PDF processing
import requests
from bs4 import BeautifulSoup
import yt_dlp  # Modern replacement for youtube-dl
from fastapi import UploadFile
import aiofiles
import tempfile

class MediaProcessor:
    def __init__(self):
        self.supported_image_types = {'.png', '.jpg', '.jpeg', '.webp'}
        self.supported_video_types = {'.mp4', '.webm', '.mkv'}
        
    def get_media_type(self, filename: str) -> str:
        """Determine media type from filename extension."""
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.pdf':
            return 'pdf'
        elif ext in self.supported_image_types:
            return 'image'
        elif ext in self.supported_video_types:
            return 'video'
        else:
            return 'text'

    async def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process files based on their type."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.pdf':
                result = await self._process_pdf(file_path)
            elif ext in self.supported_image_types:
                result = await self._process_image(file_path)
            elif ext in self.supported_video_types:
                result = await self._process_video(file_path)
            elif ext in {'.txt', '.md', '.csv', '.json'}:
                # Only decode as text for known text file types
                try:
                    text_content = content.decode('utf-8')
                except UnicodeDecodeError:
                    text_content = None
                return {
                    "type": "file",
                    "content": text_content,
                    "metadata": {"warning": "Could not decode file as UTF-8" if text_content is None else ""}
                }
            else:
                # For unknown binary types, do not decode
                return {
                    "type": "file",
                    "content": None,
                    "metadata": {"error": "Unsupported or binary file type"}
                }
            return result
        finally:
            try:
                os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete temp file: {file_path}: {e}")

    async def process_link(self, url: str) -> Dict[str, Any]:
        """Process content from various types of links."""
        if 'youtube.com' in url or 'youtu.be' in url:
            return await self._process_youtube(url)
        elif 'chat.openai.com' in url:
            return await self._process_chatgpt(url)
        else:
            return await self._process_webpage(url)

    async def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF files."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            if not text.strip():
                return {
                    "type": "pdf",
                    "content": None,
                    "metadata": {"error": "No extractable text found in PDF (may be scanned images)."}
                }
            return {
                "type": "pdf",
                "content": text,
                "metadata": {
                    "pages": len(doc),
                    "title": os.path.basename(file_path)
                }
            }
        except Exception as e:
            return {
                "type": "pdf",
                "content": None,
                "metadata": {"error": f"PDF processing error: {str(e)}"}
            }

    async def _process_image(self, file_path: str) -> Dict[str, Any]:
        """Extract text from images using OCR."""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return {
                "type": "image",
                "content": text,
                "metadata": {
                    "size": image.size,
                    "format": image.format
                }
            }
        except Exception as e:
            raise Exception(f"Image processing error: {str(e)}")

    async def _process_video(self, file_path: str) -> Dict[str, Any]:
        """Extract audio transcription from video files."""
        try:
            # Note: Implement actual video transcription using
            # a service like AssemblyAI or Whisper
            return {
                "type": "video",
                "content": "Video transcription placeholder",
                "metadata": {
                    "filename": os.path.basename(file_path)
                }
            }
        except Exception as e:
            raise Exception(f"Video processing error: {str(e)}")

    async def _process_youtube(self, url: str) -> Dict[str, Any]:
        """Extract information and transcripts from YouTube videos."""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "type": "youtube",
                    "content": info.get('description', ''),
                    "metadata": {
                        "title": info.get('title'),
                        "duration": info.get('duration'),
                        "uploader": info.get('uploader')
                    }
                }
        except Exception as e:
            raise Exception(f"YouTube processing error: {str(e)}")

    async def _process_chatgpt(self, url: str) -> Dict[str, Any]:
        """Extract chat content from ChatGPT shared links."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract chat messages
            messages = []
            for msg in soup.select('div.message'):
                text = msg.get_text().strip()
                if text:
                    messages.append(text)
            
            return {
                "type": "chatgpt",
                "content": "\n".join(messages),
                "metadata": {
                    "message_count": len(messages)
                }
            }
        except Exception as e:
            raise Exception(f"ChatGPT processing error: {str(e)}")

    async def _process_webpage(self, url: str) -> Dict[str, Any]:
        """Extract content from general webpages."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            content = "\n".join(line for line in lines if line)
            
            return {
                "type": "webpage",
                "content": content,
                "metadata": {
                    "title": soup.title.string if soup.title else None,
                    "url": url
                }
            }
        except Exception as e:
            raise Exception(f"Webpage processing error: {str(e)}")

media_processor = MediaProcessor()
