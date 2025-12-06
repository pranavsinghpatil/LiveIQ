```mermaid
sequenceDiagram
    User->>UI: Select notes + image mode
    UI->>API: /anki/generate request
    API->>LLM: structured prompt
    LLM->>API: JSON text cards
    API->>Banana: image requests (conditional)
    Banana->>API: images returned
    API->>AnkiBuilder: assemble text + images
    AnkiBuilder->>User: Download .apkg
```


---
```markdown
# Image Control Options in UI

+------------------------------------------------+
| Generate Anki Deck                             |
+------------------------------------------------+
| Include Images?   [ Off | Helpful | All | Custom ▼ ] |
| Image Style:      [ Diagrams ▼ ]               |
| Topic:            [ Transformer Attention ]    |
| Max Cards:        [ 30 ]                       |
| Difficulty:       [ Advanced ]                 |
| Study Focus:      [ Conceptual ]               |
| [ Preview Cards ]        [ Generate ]          |
+------------------------------------------------+