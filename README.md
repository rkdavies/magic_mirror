# Magic Mirror - AI Voice Assistant with Computer Vision

A hands-free, voice-activated AI assistant that responds with expressive neural text-to-speech. Built with Python, it integrates computer vision, speech recognition, and local large language models to create an interactive smart mirror experience.

## Overview

Magic Mirror is a voice-controlled AI assistant that:
- Listens for voice commands and responds with natural speech
- Uses computer vision to analyze faces and provide personalized feedback
- Maintains conversational context across interactions
- Delivers responses through high-quality neural text-to-speech

## Technical Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3 |
| **Speech Recognition** | Google Speech API (SpeechRecognition) |
| **Computer Vision** | OpenCV (cv2) |
| **LLM / Vision** | Ollama (qwen3-vl:2b, llama3) |
| **Text-to-Speech** | Orpheus-FastAPI (ZAC voice) |
| **Audio Playback** | Pydub |

## Key Features

- **Voice-First Interaction**: Completely hands-free operation using speech recognition
- **Computer Vision**: On-demand camera activation for face analysis
- **Multi-Model Architecture**: Separate models for visual analysis and conversational AI
- **Natural Speech Output**: Expressive TTS with emotional tags (laughter, sighs, etc.)
- **Character Consistency**: Configurable AI personality with strict output formatting rules

## Architecture

```
User Voice Input → SpeechRecognition → Ollama (llama3) → Orpheus-FastAPI → Audio Output
                       ↓
                  Camera Capture → Ollama (qwen3-vl:2b) → Response
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd magic-mirror

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (macOS)
brew install ffmpeg
```

## Configuration

Edit `magic_mirror.py` to configure your server URLs:

```python
mirror = MagicMirror(
    ollama_url="http://YOUR_OLLAMA_IP:11434",
    orpheus_url="http://YOUR_ORPHEUS_IP:5005"
)
```

## Required Services

1. **Ollama Server** (port 11434)
   - Model: `llama3` for conversational AI
   - Model: `qwen3-vl:2b` for visual analysis

2. **Orpheus-FastAPI** (port 5005)
   - Model: `legraphista/orpheus:latest`
   - Voice: ZAC

## Usage

```bash
python magic_mirror.py
```

### Voice Commands

- **General conversation**: Ask any question
- **Visual analysis**: "How do I look today?", "What do you think of me?", "Look at me"
- **Exit**: Say "Goodbye", "Exit", or "Stop"

## Project Structure

```
magic-mirror/
├── magic_mirror.py       # Main application
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── capture_*.jpg        # Captured images (runtime)
```

## Code Highlights

### Voice Input with Ambient Noise Handling
```python
def listen_for_speech(self, timeout=5, phrase_time_limit=10):
    with sr.Microphone() as source:
        self.recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return self.recognizer.recognize_google(audio)
```

### Vision Model Integration with Base64 Encoding
```python
def analyze_image(self, image_path, prompt=None):
    image_data = base64.b64encode(f.read()).decode("utf-8")
    payload = {"model": "qwen3-vl:2b", "prompt": prompt, "images": [image_data]}
    response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
    return response.json().get("response")
```

### Expressive Neural Text-to-Speech
```python
def speak(self, text):
    payload = {"model": "orpheus", "input": text, "voice": "zac", "response_format": "wav"}
    response = requests.post(f"{self.orpheus_url}/v1/audio/speech", json=payload)
    audio = AudioSegment.from_wav(io.BytesIO(response.content))
    play_audio(audio)
```

## Technical Challenges Solved

- **Consistent Voice Output**: Stripped voice name references from AI responses to prevent model hallucination from switching voices mid-response
- **Camera Privacy**: Camera only activates on explicit voice command, then releases immediately to prevent persistent camera usage
- **Natural Responses**: Configured AI to avoid emojis, asterisks, and filler text for cleaner TTS output
- **Timeout Handling**: Implemented retry logic for TTS requests with extended timeouts for slower model loading
- **Multi-Model Orchestration**: Coordinated separate vision and chat models with distinct system prompts for consistent personality

## Future Enhancements

- Multi-user face recognition for personalized responses
- Integration with smart home devices
- Custom voice selection option
- Expanded visual analysis capabilities
- Web dashboard for configuration

## License

MIT License

## Author

Built as a personal project exploring voice AI, computer vision, and local LLM integration.
