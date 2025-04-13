import re
from typing import List, Dict

def parse_transcript(raw_text: str) -> Dict[str, List[str]]:
    """
    Parses transcript text into speaker-wise dictionary.
    Expected format: 'Speaker Name: their text...'
    """
    lines = raw_text.splitlines()
    speakers = {}

    for line in lines:
        match = re.match(r"^(.*?):\s*(.*)", line)
        if match:
            speaker, content = match.groups()
            speakers.setdefault(speaker, []).append(content)

    return speakers
