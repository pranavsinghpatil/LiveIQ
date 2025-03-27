# Media Processor

## Purpose
The Media Processor handles various types of media inputs (audio, video, podcasts, transcripts, screenshots) and extracts chat content using advanced AI models.

## Features

### 1. Audio Processing
```python
class AudioProcessor:
    def __init__(self):
        self.whisper = OpenAI(model="whisper-1")
        self.gpt4 = OpenAI(model="gpt-4")
        
    async def process_audio(self, file_path: str) -> ProcessedAudio:
        """
        Process audio files (podcasts, voice notes) using Whisper API
        """
        # Transcribe audio
        transcript = await self._transcribe_audio(file_path)
        
        # Extract chat segments
        chat_segments = await self._extract_chat_segments(transcript)
        
        # Analyze speakers
        speakers = await self._identify_speakers(file_path)
        
        # Generate summary
        summary = await self._generate_summary(transcript)
        
        return ProcessedAudio(
            transcript=transcript,
            chat_segments=chat_segments,
            speakers=speakers,
            summary=summary,
            metadata=self._extract_metadata(file_path)
        )
        
    async def _transcribe_audio(self, file_path: str) -> str:
        """
        Transcribe audio using Whisper API
        """
        with open(file_path, "rb") as audio_file:
            transcript = await self.whisper.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                language="en",
                response_format="text"
            )
        return transcript
        
    async def _extract_chat_segments(self, transcript: str) -> List[ChatSegment]:
        """
        Extract chat segments using GPT-4
        """
        response = await self.gpt4.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Extract chat segments from the transcript. Identify speakers and their messages."
                },
                {"role": "user", "content": transcript}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        segments = json.loads(response.choices[0].message.content)
        return [ChatSegment(**segment) for segment in segments]
```

### 2. Video Processing
```python
class VideoProcessor:
    def __init__(self):
        self.vision = OpenAI(model="gpt-4-vision-preview")
        self.audio_processor = AudioProcessor()
        
    async def process_video(self, file_path: str) -> ProcessedVideo:
        """
        Process video files and extract chat content
        """
        # Extract audio track
        audio_path = await self._extract_audio(file_path)
        
        # Process audio
        audio_result = await self.audio_processor.process_audio(audio_path)
        
        # Extract key frames
        frames = await self._extract_key_frames(file_path)
        
        # Analyze visual content
        visual_analysis = await self._analyze_visual_content(frames)
        
        # Combine audio and visual analysis
        chat_content = await self._combine_analysis(
            audio_result,
            visual_analysis
        )
        
        return ProcessedVideo(
            transcript=audio_result.transcript,
            chat_content=chat_content,
            visual_analysis=visual_analysis,
            metadata=self._extract_metadata(file_path)
        )
        
    async def _extract_key_frames(self, file_path: str) -> List[str]:
        """
        Extract key frames from video
        """
        cap = cv2.VideoCapture(file_path)
        frames = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process frame (detect scene changes, etc.)
            if self._is_key_frame(frame):
                frame_path = f"frames/{uuid.uuid4()}.jpg"
                cv2.imwrite(frame_path, frame)
                frames.append(frame_path)
                
        cap.release()
        return frames
        
    async def _analyze_visual_content(
        self,
        frames: List[str]
    ) -> List[VisualAnalysis]:
        """
        Analyze visual content using GPT-4 Vision
        """
        analyses = []
        
        for frame in frames:
            with open(frame, "rb") as image_file:
                response = await self.vision.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "Analyze the visual content of this frame from a chat conversation."
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "image": base64.b64encode(image_file.read()).decode()
                                }
                            ]
                        }
                    ],
                    max_tokens=300
                )
                
            analyses.append(
                VisualAnalysis(
                    frame=frame,
                    content=response.choices[0].message.content
                )
            )
            
        return analyses
```

### 3. Screenshot Processing
```python
class ScreenshotProcessor:
    def __init__(self):
        self.vision = OpenAI(model="gpt-4-vision-preview")
        self.tesseract = pytesseract.TessBaseAPI()
        
    async def process_screenshot(self, file_path: str) -> ProcessedScreenshot:
        """
        Process chat screenshots and extract content
        """
        # Extract text using OCR
        extracted_text = await self._extract_text(file_path)
        
        # Analyze layout and structure
        layout = await self._analyze_layout(file_path)
        
        # Extract chat messages
        messages = await self._extract_messages(
            extracted_text,
            layout
        )
        
        # Analyze visual elements
        visual_elements = await self._analyze_visual_elements(file_path)
        
        return ProcessedScreenshot(
            text=extracted_text,
            messages=messages,
            visual_elements=visual_elements,
            metadata=self._extract_metadata(file_path)
        )
        
    async def _extract_text(self, file_path: str) -> str:
        """
        Extract text using Tesseract OCR
        """
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
        
    async def _analyze_layout(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze screenshot layout using GPT-4 Vision
        """
        with open(file_path, "rb") as image_file:
            response = await self.vision.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze the layout of this chat screenshot. Identify message bubbles, timestamps, and UI elements."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "image": base64.b64encode(image_file.read()).decode()
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
        return json.loads(response.choices[0].message.content)
```

### 4. Transcript Processing
```python
class TranscriptProcessor:
    def __init__(self):
        self.gpt4 = OpenAI(model="gpt-4")
        
    async def process_transcript(self, file_path: str) -> ProcessedTranscript:
        """
        Process chat transcripts and structure content
        """
        # Read transcript
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Parse transcript format
        format_type = await self._detect_format(content)
        
        # Extract messages
        messages = await self._extract_messages(
            content,
            format_type
        )
        
        # Generate metadata
        metadata = await self._generate_metadata(messages)
        
        # Create summary
        summary = await self._generate_summary(messages)
        
        return ProcessedTranscript(
            messages=messages,
            format_type=format_type,
            metadata=metadata,
            summary=summary
        )
        
    async def _detect_format(self, content: str) -> str:
        """
        Detect transcript format using GPT-4
        """
        response = await self.gpt4.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Analyze this chat transcript and identify its format (e.g., JSON, CSV, plain text)."
                },
                {"role": "user", "content": content[:1000]}  # Sample first 1000 chars
            ],
            temperature=0.3,
            max_tokens=100
        )
        return response.choices[0].message.content
```

### 5. Media Storage
```python
class MediaStorage:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = os.getenv('MEDIA_BUCKET')
        
    async def store_media(
        self,
        file_path: str,
        media_type: str
    ) -> str:
        """
        Store processed media files
        """
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
        
    async def get_media_url(self, s3_path: str) -> str:
        """
        Generate presigned URL for media access
        """
        bucket, key = self._parse_s3_path(s3_path)
        url = await self.s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket,
                'Key': key
            },
            ExpiresIn=3600
        )
        return url
```

## API Integration

### 1. Media Upload Routes
```python
@router.post("/upload/audio")
async def upload_audio(
    file: UploadFile,
    processor: AudioProcessor = Depends(get_processor)
) -> ProcessedAudio:
    """
    Upload and process audio file
    """
    # Save uploaded file
    file_path = f"uploads/{file.filename}"
    with open(file_path, 'wb') as f:
        content = await file.read()
        f.write(content)
        
    # Process audio
    result = await processor.process_audio(file_path)
    
    # Store processed file
    storage = MediaStorage()
    result.file_url = await storage.store_media(file_path, 'audio')
    
    return result

@router.post("/upload/video")
async def upload_video(
    file: UploadFile,
    processor: VideoProcessor = Depends(get_processor)
) -> ProcessedVideo:
    """
    Upload and process video file
    """
    file_path = f"uploads/{file.filename}"
    with open(file_path, 'wb') as f:
        content = await file.read()
        f.write(content)
        
    result = await processor.process_video(file_path)
    
    storage = MediaStorage()
    result.file_url = await storage.store_media(file_path, 'video')
    
    return result
```

## Recent Updates
- Added GPT-4 Vision support
- Enhanced audio processing
- Improved video analysis
- Added screenshot OCR
- Enhanced transcript parsing

## Best Practices
- Efficient media handling
- Secure file storage
- Error handling
- Progress tracking
- Resource cleanup
