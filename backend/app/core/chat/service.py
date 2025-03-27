from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from fastapi import HTTPException
from pydantic import BaseModel
from redis import Redis

from ..processors.chat_processor import ChatProcessor
from ..processors.media_processor import MediaProcessor

class ChatMetadata(BaseModel):
    id: str
    user_id: str
    title: str
    platform: str
    created_at: datetime
    updated_at: datetime
    message_count: int
    participants: List[str]
    has_media: bool
    tags: List[str] = []

class ChatService:
    def __init__(self):
        self.chat_processor = ChatProcessor()
        self.media_processor = MediaProcessor()
        self.redis = Redis(host='localhost', port=6379, db=0)
        
    async def import_chat(
        self,
        user_id: str,
        chat_data: Dict[str, Any],
        media_files: Optional[List[str]] = None
    ) -> ChatMetadata:
        """Import and process a new chat"""
        try:
            # Generate chat ID
            chat_id = str(uuid.uuid4())
            
            # Process chat content
            processed_chat = await self.chat_processor.process_chat({
                'id': chat_id,
                **chat_data
            })
            
            # Process media if present
            media_content = []
            if media_files:
                for file_path in media_files:
                    media_type = self._get_media_type(file_path)
                    processed_media = await self.media_processor.process_media(
                        file_path,
                        media_type
                    )
                    media_content.append(processed_media)
                    
            # Create metadata
            metadata = ChatMetadata(
                id=chat_id,
                user_id=user_id,
                title=processed_chat['title'],
                platform=processed_chat['platform'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                message_count=processed_chat['metadata']['message_count'],
                participants=processed_chat['metadata']['participants'],
                has_media=bool(media_content),
                tags=self._generate_tags(processed_chat)
            )
            
            # Save chat data
            await self._save_chat_data(
                chat_id,
                processed_chat,
                media_content,
                metadata
            )
            
            return metadata
            
    async def get_chat(self, chat_id: str) -> Dict[str, Any]:
        """Get chat data by ID"""
        # Get chat data from Redis
        chat_data = await self.redis.get(f"chat:{chat_id}")
        if not chat_data:
            raise HTTPException(
                status_code=404,
                detail=f"Chat {chat_id} not found"
            )
            
        return json.loads(chat_data)
        
    async def search_chats(
        self,
        user_id: str,
        query: Optional[str] = None,
        platform: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[ChatMetadata]:
        """Search user's chats"""
        # Get user's chat IDs
        chat_ids = await self._get_user_chats(user_id)
        
        # Get metadata for all chats
        metadata_list = []
        for chat_id in chat_ids:
            metadata = await self._get_chat_metadata(chat_id)
            if metadata:
                metadata_list.append(metadata)
                
        # Apply filters
        filtered_list = self._filter_chats(
            metadata_list,
            query,
            platform,
            start_date,
            end_date,
            tags
        )
        
        # Paginate results
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        return filtered_list[start_idx:end_idx]
        
    async def update_chat(
        self,
        chat_id: str,
        updates: Dict[str, Any]
    ) -> ChatMetadata:
        """Update chat metadata"""
        metadata = await self._get_chat_metadata(chat_id)
        if not metadata:
            raise HTTPException(
                status_code=404,
                detail=f"Chat {chat_id} not found"
            )
            
        # Update allowed fields
        allowed_fields = {'title', 'tags'}
        for field, value in updates.items():
            if field in allowed_fields:
                setattr(metadata, field, value)
                
        metadata.updated_at = datetime.utcnow()
        
        # Save updated metadata
        await self._save_chat_metadata(chat_id, metadata)
        
        return metadata
        
    async def delete_chat(self, chat_id: str):
        """Delete chat and associated data"""
        # Delete chat data
        await self.redis.delete(f"chat:{chat_id}")
        await self.redis.delete(f"chat:metadata:{chat_id}")
        
        # Delete from user's chat list
        metadata = await self._get_chat_metadata(chat_id)
        if metadata:
            await self.redis.srem(
                f"user:chats:{metadata.user_id}",
                chat_id
            )
            
    def _get_media_type(self, file_path: str) -> str:
        """Determine media type from file extension"""
        ext = file_path.lower().split('.')[-1]
        
        if ext in {'mp3', 'wav', 'ogg', 'm4a'}:
            return 'audio'
        elif ext in {'mp4', 'mov', 'avi', 'mkv'}:
            return 'video'
        elif ext in {'jpg', 'jpeg', 'png', 'gif'}:
            return 'image'
        else:
            raise ValueError(f"Unsupported file type: {ext}")
            
    def _generate_tags(self, processed_chat: Dict[str, Any]) -> List[str]:
        """Generate tags from processed chat data"""
        tags = set()
        
        # Add platform tag
        tags.add(processed_chat['platform'].lower())
        
        # Add topic tags
        tags.update(topic.lower() for topic in processed_chat['topics'][:3])
        
        # Add sentiment tag
        sentiment = processed_chat['sentiment']['overall_sentiment'].lower()
        tags.add(f"sentiment:{sentiment}")
        
        return list(tags)
        
    async def _save_chat_data(
        self,
        chat_id: str,
        processed_chat: Dict[str, Any],
        media_content: List[Dict[str, Any]],
        metadata: ChatMetadata
    ):
        """Save chat data to Redis"""
        # Save processed chat
        chat_data = {
            'processed_chat': processed_chat,
            'media_content': media_content,
            'metadata': metadata.dict()
        }
        
        await self.redis.set(
            f"chat:{chat_id}",
            json.dumps(chat_data),
            ex=86400 * 30  # 30 days expiration
        )
        
        # Save metadata separately for quick access
        await self._save_chat_metadata(chat_id, metadata)
        
        # Add to user's chat list
        await self.redis.sadd(
            f"user:chats:{metadata.user_id}",
            chat_id
        )
        
    async def _save_chat_metadata(
        self,
        chat_id: str,
        metadata: ChatMetadata
    ):
        """Save chat metadata to Redis"""
        await self.redis.set(
            f"chat:metadata:{chat_id}",
            metadata.json(),
            ex=86400 * 30  # 30 days expiration
        )
        
    async def _get_chat_metadata(
        self,
        chat_id: str
    ) -> Optional[ChatMetadata]:
        """Get chat metadata from Redis"""
        data = await self.redis.get(f"chat:metadata:{chat_id}")
        return ChatMetadata.parse_raw(data) if data else None
        
    async def _get_user_chats(self, user_id: str) -> List[str]:
        """Get list of user's chat IDs"""
        return list(await self.redis.smembers(f"user:chats:{user_id}"))
        
    def _filter_chats(
        self,
        metadata_list: List[ChatMetadata],
        query: Optional[str] = None,
        platform: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ) -> List[ChatMetadata]:
        """Filter chats based on search criteria"""
        filtered = metadata_list
        
        if query:
            query = query.lower()
            filtered = [
                m for m in filtered
                if query in m.title.lower()
            ]
            
        if platform:
            filtered = [
                m for m in filtered
                if m.platform.lower() == platform.lower()
            ]
            
        if start_date:
            filtered = [
                m for m in filtered
                if m.created_at >= start_date
            ]
            
        if end_date:
            filtered = [
                m for m in filtered
                if m.created_at <= end_date
            ]
            
        if tags:
            tags = set(t.lower() for t in tags)
            filtered = [
                m for m in filtered
                if tags.intersection(t.lower() for t in m.tags)
            ]
            
        return sorted(
            filtered,
            key=lambda x: x.updated_at,
            reverse=True
        )
