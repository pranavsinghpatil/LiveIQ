import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForSeq2SeqGeneration
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from redis import Redis

class ChatProcessor:
    def __init__(self):
        # Initialize AI models
        self.gpt4 = OpenAI(model="gpt-4")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        self.summarizer = AutoModelForSeq2SeqGeneration.from_pretrained("facebook/bart-large-cnn")
        
        # Initialize Redis for caching
        self.redis = Redis(host='localhost', port=6379, db=0)
        
        # Initialize TF-IDF for topic extraction
        self.tfidf = TfidfVectorizer(max_features=100)
        
    async def process_chat(self, chat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process chat data and generate insights"""
        try:
            # Extract messages
            messages = chat_data.get('messages', [])
            if not messages:
                raise ValueError("No messages found in chat data")
                
            # Generate cache key
            cache_key = f"chat:{chat_data.get('id', str(uuid.uuid4()))}"
            
            # Check cache
            cached = await self._get_cached_result(cache_key)
            if cached:
                return cached
                
            # Process chat content
            processed = {
                'id': chat_data.get('id', str(uuid.uuid4())),
                'platform': chat_data.get('platform', 'unknown'),
                'title': chat_data.get('title', 'Untitled Chat'),
                'summary': await self._generate_summary(messages),
                'topics': await self._extract_topics(messages),
                'sentiment': await self._analyze_sentiment(messages),
                'key_insights': await self._extract_insights(messages),
                'processed_at': datetime.utcnow().isoformat(),
                'metadata': self._extract_metadata(chat_data)
            }
            
            # Cache result
            await self._cache_result(cache_key, processed)
            
            return processed
            
    async def _generate_summary(self, messages: List[Dict[str, Any]]) -> str:
        """Generate a concise summary of the chat"""
        # Combine messages into a single text
        text = " ".join([msg['content'] for msg in messages])
        
        # Tokenize text
        inputs = self.tokenizer(text, max_length=1024, truncation=True, return_tensors="pt")
        
        # Generate summary
        summary_ids = self.summarizer.generate(
            inputs["input_ids"],
            max_length=150,
            min_length=40,
            length_penalty=2.0,
            num_beams=4
        )
        
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
    async def _extract_topics(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract key topics from the chat"""
        # Combine messages
        text = " ".join([msg['content'] for msg in messages])
        
        # Transform text using TF-IDF
        tfidf_matrix = self.tfidf.fit_transform([text])
        
        # Get feature names and scores
        feature_names = self.tfidf.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        # Get top topics
        top_indices = np.argsort(scores)[-10:][::-1]
        return [feature_names[i] for i in top_indices]
        
    async def _analyze_sentiment(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment of the chat"""
        response = await self.gpt4.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the sentiment of this conversation. Return a JSON object with overall_sentiment (positive/negative/neutral) and confidence_score (0-1)."
                },
                {
                    "role": "user",
                    "content": json.dumps([msg['content'] for msg in messages])
                }
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        return json.loads(response.choices[0].message.content)
        
    async def _extract_insights(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract key insights from the chat"""
        response = await self.gpt4.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Extract 3-5 key insights or takeaways from this conversation. Return as a JSON array of strings."
                },
                {
                    "role": "user",
                    "content": json.dumps([msg['content'] for msg in messages])
                }
            ],
            temperature=0.5,
            max_tokens=200
        )
        
        return json.loads(response.choices[0].message.content)
        
    def _extract_metadata(self, chat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from chat data"""
        return {
            'message_count': len(chat_data.get('messages', [])),
            'participants': self._get_unique_participants(chat_data.get('messages', [])),
            'duration': self._calculate_duration(chat_data.get('messages', [])),
            'platform': chat_data.get('platform', 'unknown'),
            'created_at': chat_data.get('created_at', datetime.utcnow().isoformat())
        }
        
    def _get_unique_participants(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Get unique participants from messages"""
        return list(set(msg.get('sender', 'unknown') for msg in messages))
        
    def _calculate_duration(self, messages: List[Dict[str, Any]]) -> Optional[float]:
        """Calculate chat duration in seconds"""
        if not messages:
            return None
            
        try:
            start_time = datetime.fromisoformat(messages[0].get('timestamp', ''))
            end_time = datetime.fromisoformat(messages[-1].get('timestamp', ''))
            return (end_time - start_time).total_seconds()
        except (ValueError, TypeError):
            return None
            
    async def _get_cached_result(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached processing result"""
        cached = await self.redis.get(key)
        return json.loads(cached) if cached else None
        
    async def _cache_result(self, key: str, result: Dict[str, Any]):
        """Cache processing result"""
        await self.redis.set(
            key,
            json.dumps(result),
            ex=3600  # 1 hour expiration
        )
