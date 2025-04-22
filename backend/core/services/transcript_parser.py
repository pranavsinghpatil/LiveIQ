import re
from typing import Dict, List, Any

def smart_parse_speakers(transcript: str) -> Dict[str, Any]:
    """
    Attempts to infer speakers and their utterances from a transcript.
    Returns:
        {
            "num_speakers": int,
            "speakers": List[Dict[str, str]],  # Each: {"id": str, "name": str}
            "dialogue": Dict[str, List[str]]  # key is speaker id
        }
    """
    lines = [line.strip() for line in transcript.splitlines() if line.strip()]
    speaker_pattern = re.compile(r"^([A-Za-z0-9_\- ]+):\s*(.+)$")
    dialogue = {}
    speaker_counts = {}
    speaker_name_to_id = {}
    last_speaker = None
    speaker_id_counter = 1

    for line in lines:
        match = speaker_pattern.match(line)
        if match:
            speaker, message = match.groups()
            speaker = speaker.strip()
            # Assign a unique speaker id
            if speaker not in speaker_name_to_id:
                speaker_name_to_id[speaker] = f"speaker_{speaker_id_counter}"
                speaker_id_counter += 1
            spk_id = speaker_name_to_id[speaker]
            dialogue.setdefault(spk_id, []).append(message.strip())
            speaker_counts[spk_id] = speaker_counts.get(spk_id, 0) + 1
            last_speaker = spk_id
        else:
            # If line does not match, try to assign to last speaker
            if last_speaker:
                dialogue[last_speaker].append(line)
            else:
                dialogue.setdefault("unknown", []).append(line)

    # Heuristic: If only one speaker, try to split by Q/A or other patterns
    if len(dialogue) == 1 and "unknown" in dialogue:
        alt_pattern = re.compile(r"^(Q|A|[0-9]+)[\.:\)]\s*(.+)$", re.IGNORECASE)
        new_dialogue = {}
        for line in dialogue["unknown"]:
            match = alt_pattern.match(line)
            if match:
                speaker, message = match.groups()
                if speaker not in speaker_name_to_id:
                    speaker_name_to_id[speaker] = f"speaker_{speaker_id_counter}"
                    speaker_id_counter += 1
                spk_id = speaker_name_to_id[speaker]
                new_dialogue.setdefault(spk_id, []).append(message.strip())
            else:
                new_dialogue.setdefault("unknown", []).append(line)
        if len(new_dialogue) > 1:
            dialogue = new_dialogue

    # Prepare speaker metadata list
    speakers = []
    for name, spk_id in speaker_name_to_id.items():
        speakers.append({"id": spk_id, "name": name})
    if "unknown" in dialogue:
        speakers.append({"id": "unknown", "name": "Unknown"})

    return {
        "num_speakers": len(speakers),
        "speakers": speakers,
        "dialogue": dialogue
    }

# For backward compatibility, you can alias smart_parse_speakers as parse_speakers
parse_speakers = smart_parse_speakers