"""
Configuration management with validation.
"""
import os
from dataclasses import dataclass, field
from typing import Optional
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    # API Keys
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    
    # Timezone
    timezone: ZoneInfo = field(default_factory=lambda: ZoneInfo("America/New_York"))
    timezone_name: str = "America/New_York"
    
    # OpenAI settings
    model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o"))
    max_tool_rounds: int = 8
    
    # Conversation settings
    max_history_messages: int = 20
    state_ttl_seconds: int = 3600  # 1 hour
    pending_action_ttl_seconds: int = 300  # 5 minutes
    
    # Calendar settings
    calendar_id: str = "primary"
    token_path: str = "token.json"
    default_event_duration_minutes: int = 60
    max_search_results: int = 10
    search_window_days: int = 30
    
    # Assistant identity
    owner_name: str = field(default_factory=lambda: os.getenv("OWNER_NAME", "Brandon"))
    assistant_name: str = "your assistant"
    
    def __post_init__(self):
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")


# Singleton
config = Config()
