import genanki
from typing import List
from .schemas import Flashcard
import random

class AnkiDeckBuilder:
    def __init__(self):
        self.model = genanki.Model(
            1607392319,
            'MeshCards Basic',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
            ])

    def create_apkg(self, cards: List[Flashcard], deck_name: str, output_path: str):
        # Generate a random deck ID
        deck_id = random.randrange(1 << 30, 1 << 31)
        deck = genanki.Deck(deck_id, deck_name)

        for card in cards:
            # Sanitize tags: replace spaces with underscores
            tags = [t.replace(" ", "_") for t in card.tags]
            note = genanki.Note(
                model=self.model,
                fields=[card.front, card.back],
                tags=tags
            )
            deck.add_note(note)

        genanki.Package(deck).write_to_file(output_path)
