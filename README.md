# Magic Mirror AI 

**Magic Mirror** is an AI-powered interactive assistant that combines computer vision, voice recognition, and natural language processing to act as a sentient, "magical" mirror. It uses a local Ollama instance for visual and textual reasoning and the Orpheus-FastAPI (ZAC voice) for high-quality text-to-speech output.

---

## Features

* **Voice Interaction:** Fully hands-free operation using Google Speech Recognition.
* **Computer Vision:** Captures real-time images via your webcam to "see" who is standing before it.
* **Multi-Model Intelligence:**
* **Visual Analysis:** Uses `qwen3-vl:2b` to analyze physical appearance and provide compliments.
* **Conversational Logic:** Uses `llama3` to handle general questions and maintain context.


* **Expressive TTS:** Integrates with Orpheus-FastAPI using the **ZAC** voice, supporting emotional tags like `<laugh>`, `<sigh>`, and `<gasp>`.
* **Personality-Driven:** Configured to be wise, caring, and occasionally witty—true to the fairy tale aesthetic.

---

## Architecture

### System Components

| Component | Technology | Role |
| --- | --- | --- |
| **Vision** | OpenCV (CV2) | Captures frames from the system camera. |
| **Brain** | Ollama (`qwen3-vl` & `llama3`) | Processes images and generates text responses. |
| **Voice In** | SpeechRecognition | Converts user speech to text via Google API. |
| **Voice Out** | Orpheus-FastAPI (ZAC) | Converts AI text to expressive WAV audio. |
| **Audio Playback** | Pydub | Handles the playback of generated speech. |

---

## Getting Started

### Prerequisites

1. **Ollama Server:** Ensure Ollama is running on your network (Default IP: `192.168.1.151`).
* Pull models: `ollama pull llama3` and `ollama pull qwen3-vl:2b`.


2. **Orpheus-FastAPI:** A running instance of the Orpheus TTS server at `192.168.1.151:5005` with the `zac` voice installed.
3. **Python 3.x Environment.**

### Installation

```bash
# Install system dependencies (macOS)
brew install ffmpeg

# Install Python dependencies
pip install opencv-python requests SpeechRecognition pydub

```

### Configuration

Modify the `MagicMirror` class initialization in the script if your server IPs differ:

```python
mirror = MagicMirror(
    ollama_url="http://YOUR_IP:11434",
    orpheus_url="http://YOUR_IP:5005"
)

```

---

## Interaction Guide

### How to Use

1. **Run the script:** `python magic_mirror.py`
2. **Wait for the Greeting:** The mirror will introduce itself once the connection is established.
3. **Trigger Phrases:** The mirror listens for specific keywords to trigger the camera:
* *"Mirror, mirror, how do I look today?"*
* *"What do you think of me?"*
* *"Look at me."*


4. **Natural Conversation:** Ask anything else to engage the general LLM.
5. **Termination:** Say *"Goodbye"*, *"Exit"*, or *"Stop"* to close the program.

### Emotional Tags

The mirror uses internal tags to express human-like sounds through the Orpheus engine:

* `<laugh>` / `<chuckle>`
* `<sigh>` / `<gasp>`
* `<sniffle>` / `<yawn>`

---

## System Personality Rules

The mirror is governed by a strict system prompt to maintain its character:

* **No Emojis:** Strictly prohibited to keep the "magical" feel.
* **Plain Text Only:** No bolding, italics, or asterisks (to prevent the TTS from reading formatting symbols).
* **Character Consistency:** Always speaks as a wise, evocative entity from a fairy tale.

---

**Would you like me to generate a `requirements.txt` file or a Docker Compose snippet to help you host the Ollama and Orpheus services?**
