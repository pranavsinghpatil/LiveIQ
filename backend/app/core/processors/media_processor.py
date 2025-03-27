import os
import uuid
import json
import base64
from typing import Dict, List, Any, Optional
from datetime import datetime

import cv2
import numpy as np
from PIL import Image
import pytesseract
from openai import OpenAI
import boto3
import httpx
from pydantic import BaseModel

class ProcessedMedia(BaseModel):
    id: str
    type: str
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    file_url: Optional[str] = None
    created_at: datetime

class MediaProcessor:
    def __init__(self):
        # Initialize AI models
        self.whisper = OpenAI(model="whisper-1")
        self.vision = OpenAI(model="gpt-4-vision-preview")
        self.gpt4 = OpenAI(model="gpt-4")
        
        # Initialize OCR
        self.tesseract = pytesseract.TessBaseAPI()
        
        # Initialize S3 client
        self.s3 = boto3.client('s3')
        self.bucket = os.getenv('MEDIA_BUCKET', 'voxstitch-media')
        
    async def process_media(self, file_path: str, media_type: str) -> ProcessedMedia:
        """Process various types of media files"""
        try:
            if media_type == 'audio':
                content = await self._process_audio(file_path)
            elif media_type == 'video':
                content = await self._process_video(file_path)
            elif media_type == 'image':
                content = await self._process_image(file_path)
            else:
                raise ValueError(f"Unsupported media type: {media_type}")
                
            # Store processed file
            file_url = await self._store_media(file_path, media_type)
            
            return ProcessedMedia(
                id=str(uuid.uuid4()),
                type=media_type,
                content=content,
                metadata=self._extract_metadata(file_path, media_type),
                file_url=file_url,
                created_at=datetime.utcnow()
            )
            
        except Exception as e:
            raise Exception(f"Failed to process {media_type}: {str(e)}")
            
    async def _process_audio(self, file_path: str) -> Dict[str, Any]:
        """Process audio files using Whisper API"""
        with open(file_path, "rb") as audio_file:
            # Transcribe audio
            transcript = await self.whisper.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                language="en",
                response_format="verbose_json"
            )
            
        # Extract chat segments
        segments = await self._extract_chat_segments(transcript.text)
        
        # Generate summary
        summary = await self._generate_summary(transcript.text)
        
        return {
            'transcript': transcript.text,
            'segments': segments,
            'summary': summary,
            'speakers': transcript.speakers if hasattr(transcript, 'speakers') else [],
            'confidence': transcript.confidence if hasattr(transcript, 'confidence') else None
        }
        
    async def _process_video(self, file_path: str) -> Dict[str, Any]:
        """Process video files"""
        # Extract audio for transcription
        audio_path = self._extract_audio(file_path)
        audio_content = await self._process_audio(audio_path)
        
        # Extract and analyze key frames
        frames = await self._extract_key_frames(file_path)
        visual_content = await self._analyze_frames(frames)
        
        # Clean up temporary files
        os.remove(audio_path)
        for frame in frames:
            os.remove(frame)
            
        return {
            'audio': audio_content,
            'visual': visual_content
        }
        
    async def _process_image(self, file_path: str) -> Dict[str, Any]:
        """Process image files (screenshots) using OCR and GPT-4 Vision"""
        # Extract text using OCR
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)
        
        # Analyze image using GPT-4 Vision
        with open(file_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode()
            
        response = await self.vision.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Analyze this chat screenshot. Identify the chat platform, message structure, and any UI elements."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "image": image_data
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        visual_analysis = json.loads(response.choices[0].message.content)
        
        return {
            'text': extracted_text,
            'visual_analysis': visual_analysis,
            'platform': visual_analysis.get('platform'),
            'messages': await self._extract_messages(extracted_text, visual_analysis)
        }
        
    def _extract_audio(self, video_path: str) -> str:
        """Extract audio from video file"""
        audio_path = f"temp/{uuid.uuid4()}.wav"
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        
        # Use ffmpeg to extract audio
        os.system(f'ffmpeg -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {audio_path}')
        
        return audio_path
        
    async def _extract_key_frames(self, video_path: str) -> List[str]:
        """Extract key frames from video"""
        frames = []
        cap = cv2.VideoCapture(video_path)
        
        # Parameters for frame extraction
        frame_interval = int(cap.get(cv2.CAP_PROP_FPS))  # Extract 1 frame per second
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        for i in range(0, total_frames, frame_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                frame_path = f"temp/frame_{uuid.uuid4()}.jpg"
                cv2.imwrite(frame_path, frame)
                frames.append(frame_path)
                
        cap.release()
        return frames
        
    async def _analyze_frames(self, frame_paths: List[str]) -> List[Dict[str, Any]]:
        """Analyze video frames using GPT-4 Vision"""
        analyses = []
        
        for frame_path in frame_paths:
            with open(frame_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode()
                
            response = await self.vision.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze this video frame from a chat conversation."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "image": image_data
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            analyses.append({
                'frame': os.path.basename(frame_path),
                'analysis': json.loads(response.choices[0].message.content)
            })
            
        return analyses
        
    async def _extract_chat_segments(self, text: str) -> List[Dict[str, Any]]:
        """Extract chat segments from text"""
        response = await self.gpt4.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Extract chat segments from this text. Identify speakers and their messages."
                },
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        return json.loads(response.choices[0].message.content)
        
    async def _generate_summary(self, text: str) -> str:
        """Generate summary of chat content"""
        response = await self.gpt4.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Generate a concise summary of this chat conversation."
                },
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content
        
    async def _extract_messages(
        self,
        text: str,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract structured messages from text and analysis"""
        response = await self.gpt4.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Extract structured messages from this chat text. Use the visual analysis to improve accuracy."
                },
                {
                    "role": "user",
                    "content": json.dumps({
                        'text': text,
                        'analysis': analysis
                    })
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        return json.loads(response.choices[0].message.content)
        
    def _extract_metadata(self, file_path: str, media_type: str) -> Dict[str, Any]:
        """Extract metadata from media file"""
        stats = os.stat(file_path)
        
        metadata = {
            'filename': os.path.basename(file_path),
            'size': stats.st_size,
            'created_at': datetime.fromtimestamp(stats.st_ctime).isoformat(),
            'modified_at': datetime.fromtimestamp(stats.st_mtime).isoformat(),
            'media_type': media_type
        }
        
        if media_type == 'video':
            cap = cv2.VideoCapture(file_path)
            metadata.update({
                'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS),
                'fps': cap.get(cv2.CAP_PROP_FPS),
                'frame_count': cap.get(cv2.CAP_PROP_FRAME_COUNT),
                'resolution': f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
            })
            cap.release()
            
        elif media_type == 'image':
            with Image.open(file_path) as img:
                metadata.update({
                    'format': img.format,
                    'mode': img.mode,
                    'resolution': f"{img.width}x{img.height}"
                })
                
        return metadata
        
    async def _store_media(self, file_path: str, media_type: str) -> str:
        """Store processed media in S3"""
        file_id = str(uuid.uuid4())
        key = f"media/{media_type}/{file_id}/{os.path.basename(file_path)}"
        
        with open(file_path, 'rb') as f:
            await self.s3.upload_fileobj(
                f,
                self.bucket,
                key,
                ExtraArgs={'ContentType': f'application/{media_type}'}
            )
            
        return f"s3://{self.bucket}/{key}"
