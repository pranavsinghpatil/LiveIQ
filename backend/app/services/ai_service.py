import json
import time
import asyncio
from typing import Optional
from datetime import datetime
import google.generativeai as genai
from groq import AsyncGroq
from app.config import get_settings
from app.schemas import GeminiAnalysisOutput
from app.models import TrendEnum

settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# Configure Groq
groq_client = AsyncGroq(api_key=settings.groq_api_key)


# ── Groq Commentary ────────────────────────────────────────────────────────────

async def generate_groq_commentary(event_data: dict) -> tuple[str, int]:
    """
    Generate fast one-liner commentary using Groq Llama 3.1 8B.
    Target: under 2 seconds.
    Returns: (commentary_text, latency_ms)
    """
    start = time.time()

    prompt = f"""You are a live sports commentator. Generate ONE engaging one-liner commentary for this event update.
Keep it under 20 words. Be specific about the score and action.

Event: {event_data.get('home_team')} vs {event_data.get('away_team')}
Sport: {event_data.get('sport', 'Sports')}
Score: {event_data.get('home_score', '0')} - {event_data.get('away_score', '0')}
Status: {event_data.get('status', 'In Progress')}
Latest data: {json.dumps(event_data, default=str)[:500]}

Commentary (one line only):"""

    if settings.groq_api_key == "your_groq_api_key_here":
        import random
        home = event_data.get('home_team', 'Home')
        away = event_data.get('away_team', 'Away')
        home_score = event_data.get('home_score', '0')
        away_score = event_data.get('away_score', '0')

        templates = [
            # Attacking plays
            f"{home} driving forward with purpose — the pressure is building.",
            f"Brilliant combination play from {home}, finding space in the final third.",
            f"{away} pushing high up the pitch, looking to press intensely.",
            f"A dangerous cross whipped in — nobody could get on the end of it.",
            f"The referee waves play on as {home} appeal for a foul on the edge of the box.",
            f"Quick free-kick caught {away}'s defense completely flat-footed.",
            f"Inch-perfect through ball finds the striker — but the offside flag is up.",
            f"Corner for {home}. The set piece routine looks practiced and deliberate.",
            f"{away} goalkeeper commanded the box well, punching clear under pressure.",
            f"The winger cuts inside and fires — deflected wide for a corner.",

            # Tactical
            f"{home} switching to a high press in midfield, suffocating {away}'s buildup.",
            f"The midfield battle is intense — neither side giving an inch.",
            f"{away} dropping deep, sitting in a compact block of four at the back.",
            f"Possession shifts quickly — {home} recycling patiently, looking for an opening.",
            f"That substitution could change the shape of this match completely.",
            f"{home} exploiting the wide areas effectively, stretching {away}'s defensive line.",
            f"A tactical foul breaks up what could have been a devastating counter-attack.",

            # Score-aware
            f"At {home_score}–{away_score}, {home} will be frustrated they can't find the breakthrough.",
            f"Leading {home_score}–{away_score}, {away} sitting deep and protecting their advantage.",
            f"This is nervous territory — a single goal could completely swing the tie.",
            f"With the score at {home_score}–{away_score}, both managers watching the clock carefully.",

            # Defensive moments
            f"Outstanding recovery tackle from {away}'s center-back — crucial interception.",
            f"Last-ditch block on the line — {away} somehow keeping this level.",
            f"{home}'s backline dealing with everything thrown at them, so composed.",
            f"Counter-attack alert! {away} springing forward with pace and numbers.",

            # Individual moments
            f"The captain stepping up to lead by example — driving his team forward.",
            f"A loose touch in midfield invites pressure — {home} pounce immediately.",
            f"Individual brilliance from the No.10 — beating two defenders before the shot.",
            f"An absolute thunderbolt from range! The goalkeeper had no chance.",
            f"Great save! Pushed it onto the post — the woodwork keeping {away} out.",
            f"He goes down clutching his hamstring — could be a serious concern here.",
            f"The youngster is having a tremendous impact since coming on as substitute.",

            # Atmosphere / general
            f"The tempo has lifted considerably in the last five minutes.",
            f"Both managers animated on the touchline, sensing the game is at a tipping point.",
            f"Long ball over the top — chased down superbly, showing real determination.",
            f"Good penalty shout waved away — the away side absolutely furious.",
            f"Stoppage time to be announced — both benches on their feet.",
            f"The play is end-to-end now, this is enthralling stuff.",
            f"A moment of quality in the chaos — threading the needle between three defenders.",
        ]

        text = random.choice(templates)
        return text, 50

    try:
        response = await groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.8,
        )
        latency_ms = int((time.time() - start) * 1000)
        text = response.choices[0].message.content.strip()
        return text, latency_ms
    except Exception as e:
        latency_ms = int((time.time() - start) * 1000)
        return f"Commentary unavailable: {str(e)[:50]}", latency_ms


# ── Gemini Analysis ────────────────────────────────────────────────────────────

GEMINI_ANALYSIS_PROMPT = """You are an expert sports analyst. Analyze the following rolling window of 50 sports event updates and provide structured analysis.

Event: {home_team} vs {away_team} ({sport})
Current Score: {home_score} - {away_score}
Status: {status}
{weather_context}

Rolling Event Stream (last 50 updates):
{event_stream}

Provide your analysis in the following JSON format ONLY (no other text):
{{
  "updated_summary": "2-3 sentence narrative summary of the current state of the game",
  "key_moments": ["moment 1", "moment 2", "moment 3", "moment 4", "moment 5"],
  "trend": "momentum|stable|reversal",
  "prediction": "Your prediction for the outcome with reasoning",
  "confidence": 0.75
}}

Rules:
- trend must be exactly one of: momentum, stable, reversal
- confidence must be a float between 0.0 and 1.0
- key_moments must have exactly 5 items
- Return ONLY valid JSON, no markdown code blocks"""


async def generate_gemini_analysis(
    event_data: dict,
    event_stream: list,
    weather_conditions: Optional[str] = None,
) -> tuple[GeminiAnalysisOutput, int]:
    """
    Deep analysis using Gemini 1.5 Flash.
    Returns structured output validated with Pydantic.
    Retries once on malformed response.
    """
    start = time.time()

    weather_context = ""
    if weather_conditions:
        weather_context = f"Current Weather: {weather_conditions}"

    prompt = GEMINI_ANALYSIS_PROMPT.format(
        home_team=event_data.get("home_team", "Home"),
        away_team=event_data.get("away_team", "Away"),
        sport=event_data.get("sport", "Sports"),
        home_score=event_data.get("home_score", "0"),
        away_score=event_data.get("away_score", "0"),
        status=event_data.get("status", "In Progress"),
        weather_context=weather_context,
        event_stream=json.dumps(event_stream[:50], default=str)[:8000],
    )

    if settings.gemini_api_key == "your_gemini_api_key_here":
        import random
        return GeminiAnalysisOutput(
            updated_summary=f"Mock Analysis: The game between {event_data.get('home_team')} and {event_data.get('away_team')} is heating up. Tactical adjustments are visible.",
            key_moments=["Strong start", "Midfield control established", "Momentum shift", "Defense tightening", "Final push imminent"],
            trend=random.choice([TrendEnum.momentum, TrendEnum.stable, TrendEnum.reversal]),
            prediction=f"Prediction: {event_data.get('home_team')} will likely maintain pressure.",
            confidence=0.85
        ), 120

    for attempt in range(2):
        try:
            response = await asyncio.to_thread(
                gemini_model.generate_content,
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=1024,
                ),
            )
            latency_ms = int((time.time() - start) * 1000)
            raw_text = response.text.strip()

            # Strip markdown code blocks if present
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]

            parsed = json.loads(raw_text)
            # Validate trend
            if parsed.get("trend") not in ["momentum", "stable", "reversal"]:
                parsed["trend"] = "stable"
            # Ensure key_moments is list of 5
            moments = parsed.get("key_moments", [])
            while len(moments) < 5:
                moments.append("No additional key moments recorded")
            parsed["key_moments"] = moments[:5]

            return GeminiAnalysisOutput(**parsed), latency_ms

        except Exception as e:
            if attempt == 0:
                await asyncio.sleep(1)
                continue
            latency_ms = int((time.time() - start) * 1000)
            # Fallback response
            return GeminiAnalysisOutput(
                updated_summary=f"Analysis unavailable: {str(e)[:100]}",
                key_moments=["Data processing", "Awaiting analysis", "System retry", "Check back soon", "Pipeline active"],
                trend=TrendEnum.stable,
                prediction="Unable to generate prediction at this time",
                confidence=0.5,
            ), latency_ms


# ── Gemini Post-Event Report ───────────────────────────────────────────────────

async def generate_post_event_report(
    event_data: dict,
    full_history: list,
    stored_predictions: list,
    actual_outcome: str,
) -> tuple[dict, int]:
    """Generate full post-event narrative report with prediction accuracy."""
    start = time.time()

    prompt = f"""You are an expert sports journalist. Write a comprehensive post-event report.

Event: {event_data.get('home_team')} vs {event_data.get('away_team')}
Sport: {event_data.get('sport')}
Final Score: {event_data.get('home_score')} - {event_data.get('away_score')}
Outcome: {actual_outcome}

Full Event History (summarized):
{json.dumps(full_history[:50], default=str)[:6000]}

Previous AI Predictions made during the game:
{json.dumps(stored_predictions, default=str)[:2000]}

Generate a JSON report with:
{{
  "narrative": "Full 4-6 paragraph narrative of the game",
  "key_moments": ["moment 1", "moment 2", "moment 3", "moment 4", "moment 5"],
  "prediction_accuracy": 0.75,
  "accuracy_explanation": "Brief explanation of prediction accuracy"
}}

Return ONLY valid JSON."""

    try:
        response = await asyncio.to_thread(
            gemini_model.generate_content,
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.4,
                max_output_tokens=2048,
            ),
        )
        latency_ms = int((time.time() - start) * 1000)
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        return json.loads(raw_text), latency_ms
    except Exception as e:
        latency_ms = int((time.time() - start) * 1000)
        return {
            "narrative": f"Report generation failed: {str(e)[:200]}",
            "key_moments": [],
            "prediction_accuracy": 0.0,
            "accuracy_explanation": "Unable to evaluate",
        }, latency_ms


# ── Groq Debate Prediction (Bonus) ────────────────────────────────────────────

async def generate_groq_prediction(event_data: dict, event_stream: list) -> tuple[str, float, int]:
    """Generate Groq-based prediction for multi-model debate mode."""
    start = time.time()

    prompt = f"""Analyze this sports event and predict the outcome.

Event: {event_data.get('home_team')} vs {event_data.get('away_team')}
Current Score: {event_data.get('home_score', '0')} - {event_data.get('away_score', '0')}
Sport: {event_data.get('sport')}

Recent updates: {json.dumps(event_stream[-10:], default=str)[:2000]}

Respond in JSON only:
{{"prediction": "your prediction here", "confidence": 0.75, "reasoning": "brief reasoning"}}"""

    if settings.groq_api_key == "your_groq_api_key_here":
        return f"Mock Groq Prediction: {event_data.get('away_team')} looks strong on the counter.", 0.70, 60

    try:
        response = await groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5,
        )
        latency_ms = int((time.time() - start) * 1000)
        text = response.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        parsed = json.loads(text)
        return parsed.get("prediction", "No prediction"), float(parsed.get("confidence", 0.5)), latency_ms
    except Exception as e:
        return f"Groq prediction unavailable: {str(e)[:50]}", 0.5, int((time.time() - start) * 1000)
