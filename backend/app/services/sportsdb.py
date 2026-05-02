import json
import httpx
from datetime import datetime
from typing import List, Optional
from app.config import get_settings

settings = get_settings()

SPORTSDB_BASE = "https://www.thesportsdb.com/api/v1/json"
MOCK_FILE_PATH = "mock_livescore.json"


import random

_mock_data_state = None

def _load_mock_data() -> List[dict]:
    global _mock_data_state
    try:
        if _mock_data_state is None:
            with open(MOCK_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                _mock_data_state = data.get("events", [])
        
        # Simulate dynamic changes for the demo
        for event in _mock_data_state:
            status = event.get("status", "")
            if status in ("Live", "1H", "2H", "In Progress", "Q1", "Q2", "Q3", "Q4", "Set 1", "Set 2", "Set 3"):
                # 15% chance to score on each poll
                if random.random() < 0.15:
                    if random.random() < 0.5:
                        current = int(event.get("home_score", 0) or 0)
                        event["home_score"] = str(current + 1)
                    else:
                        current = int(event.get("away_score", 0) or 0)
                        event["away_score"] = str(current + 1)
                
                # Ensure the event stream has unique timestamps
                event["simulated_clock"] = datetime.utcnow().isoformat()
        
        return _mock_data_state
    except FileNotFoundError:
        return []


async def fetch_live_events(sport: Optional[str] = None) -> List[dict]:
    """Fetch live/upcoming events from TheSportsDB or mock file."""
    if settings.use_mock:
        events = _load_mock_data()
        if sport:
            events = [e for e in events if e.get("strSport", "").lower() == sport.lower()]
        return events

    api_key = settings.sportsdb_api_key
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Fetch events for multiple sports
            all_events = []
            sports_to_fetch = [sport] if sport else ["Soccer", "Basketball", "Tennis"]
            for s in sports_to_fetch:
                # TheSportsDB upcoming events by league (example: EPL = 4328)
                url = f"{SPORTSDB_BASE}/{api_key}/eventsday.php"
                params = {"d": datetime.utcnow().strftime("%Y-%m-%d"), "s": s}
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    events = data.get("events") or []
                    all_events.extend(events)
            return all_events
        except Exception as e:
            print(f"[SportsDB] Error fetching events: {e}")
            return _load_mock_data()


async def fetch_event_detail(event_id: str) -> Optional[dict]:
    """Fetch detailed info for a specific event."""
    if settings.use_mock:
        events = _load_mock_data()
        return next((e for e in events if str(e.get("idEvent")) == str(event_id)), None)

    api_key = settings.sportsdb_api_key
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"{SPORTSDB_BASE}/{api_key}/lookupevent.php"
            resp = await client.get(url, params={"id": event_id})
            if resp.status_code == 200:
                data = resp.json()
                events = data.get("events") or []
                return events[0] if events else None
        except Exception as e:
            print(f"[SportsDB] Error fetching event {event_id}: {e}")
            return None


def normalize_event(raw: dict) -> dict:
    """Normalize TheSportsDB API response to our internal format."""
    return {
        "id": str(raw.get("idEvent", raw.get("id", ""))),
        "sport": raw.get("strSport", raw.get("sport", "Sports")),
        "league": raw.get("strLeague", raw.get("league")),
        "home_team": raw.get("strHomeTeam", raw.get("home_team", "Home Team")),
        "away_team": raw.get("strAwayTeam", raw.get("away_team", "Away Team")),
        "home_score": str(raw.get("intHomeScore", raw.get("home_score", ""))) if raw.get("intHomeScore") is not None else raw.get("home_score", ""),
        "away_score": str(raw.get("intAwayScore", raw.get("away_score", ""))) if raw.get("intAwayScore") is not None else raw.get("away_score", ""),
        "status": raw.get("strStatus", raw.get("status", "NotStarted")),
        "venue": raw.get("strVenue", raw.get("venue")),
        "event_date": raw.get("dateEvent", raw.get("event_date")),
        "raw_data": raw,
    }
