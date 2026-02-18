#!/usr/bin/env python3
"""
Magic Mirror - AI-powered voice assistant with camera vision
Connects to Ollama at 192.168.1.151 for AI responses
Orpheus-FastAPI at 192.168.1.151:5005 voices all output with ZAC
"""

import io
import time
import requests
import speech_recognition as sr
import cv2
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play as play_audio


class MagicMirror:
    def __init__(
        self,
        ollama_url="http://192.168.1.151:11434",
        orpheus_url="http://192.168.1.151:5005",
    ):
        self.ollama_url = ollama_url
        self.orpheus_url = orpheus_url
        self.conversation_history = []
        self.recognizer = sr.Recognizer()

    def capture_image(self):
        """Capture photo from macOS camera"""
        camera = cv2.VideoCapture(0)
        time.sleep(1)
        ret, frame = camera.read()
        camera.release()

        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capture_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            return filename, frame
        return None, None

    def analyze_image(self, image_path, prompt=None):
        """Analyze image using Ollama with vision capabilities"""
        try:
            import base64

            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")

            mirror_prompt = """You are a magical mirror with personality. You gaze upon the person before you and offer insightful, thoughtful, and occasionally witty commentary about their appearance and what you perceive. Speak as the wise, magical mirror from fairy tales - be perceptive, caring, and evocative in your description. 

IMPORTANT: Use emotion tags in your responses to add expression. Available tags:
- <laugh> or <chuckle> for laughter
- <sigh> for sighing
- <cough> or <sniffle> for subtle sounds
- <groan>, <yawn>, <gasp> for emotional expression

IMPORTANT: Keep responses concise and natural. Do not add any extra commentary, explanations, or filler at the end. End your response when you're done speaking.

IMPORTANT: Do NOT use any emojis or emoticons (like :), :D, :(, etc.). Use only plain text.

IMPORTANT: Do NOT use any asterisks (*). Do not use bold, italic, or any formatting with asterisks. Use only plain text.

Compliment the person in this image: """

            full_prompt = prompt or mirror_prompt

            payload = {
                "model": "qwen3-vl:2b",
                "prompt": full_prompt,
                "images": [image_data],
                "stream": False,
            }

            response = requests.post(
                f"{self.ollama_url}/api/generate", json=payload, timeout=120
            )

            if response.status_code == 200:
                return response.json().get("response", "I analyzed the image.")
        except Exception as e:
            return f"I tried to look at the photo but encountered: {str(e)}"
        return None

    def ask_ollama(self, query, image_context=None):
        """Send query to Ollama and get response"""
        print(f"Sending to Ollama: {query}")
        system_prompt = """You are a Magic Mirror with personality. You're insightful, 
        occasionally witty, and care deeply about the people who look into you. 
        You can see and analyze the world through your camera. When someone asks
        what you think of them, give thoughtful, personalized feedback.

IMPORTANT: Use emotion tags in your responses to add expression. Available tags:
- <laugh> or <chuckle> for laughter
- <sigh> for sighing
- <cough> or <sniffle> for subtle sounds
- <groan>, <yawn>, <gasp> for emotional expression

Use these naturally to enhance your magical mirror personality.

IMPORTANT: Keep responses concise and natural. Do not add any extra commentary, explanations, or filler at the end. End your response when you're done speaking.

IMPORTANT: Do NOT use any emojis or emoticons (like :), :D, :(, etc.). Use only plain text.

IMPORTANT: Do NOT mention voice names, speakers, or tones. Never refer to 'zac', 'voice', 'tone', or similar words in your response."""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation_history[-6:])

        if image_context:
            query = f"{query}\n\n[VISUAL INPUT: {image_context}]"

        messages.append({"role": "user", "content": query})

        payload = {"model": "llama3", "messages": messages, "stream": False}

        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat", json=payload, timeout=30
            )
            print(f"Ollama response status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"Ollama response: {result}")
                reply = result.get("message", {}).get("content", "")
                messages.append({"role": "assistant", "content": reply})
                self.conversation_history = messages
                return reply
            else:
                print(f"Ollama error: {response.text}")
        except Exception as e:
            print(f"Ollama request error: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"

        return None

    def speak(self, text):
        """Speak text using Orpheus-FastAPI with ZAC voice"""
        print(f"Mirror says: {text}")
        text = text.replace("zac", "").replace("ZAC", "").strip()

        try:
            payload = {
                "model": "orpheus",
                "input": text,
                "voice": "zac",
                "response_format": "wav",
                "speed": 1.0,
            }

            response = requests.post(
                f"{self.orpheus_url}/v1/audio/speech", json=payload, timeout=120
            )

            if response.status_code == 200:
                audio = AudioSegment.from_wav(io.BytesIO(response.content))
                play_audio(audio)
            else:
                print(f"Orpheus TTS error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            print("Orpheus TTS timed out - server may be busy, trying again...")
            time.sleep(2)
            try:
                response = requests.post(
                    f"{self.orpheus_url}/v1/audio/speech", json=payload, timeout=180
                )
                if response.status_code == 200:
                    audio = AudioSegment.from_wav(io.BytesIO(response.content))
                    play_audio(audio)
            except Exception as e:
                print(f"Retry failed: {e}")
        except Exception as e:
            print(f"Speech generation error: {e}")

    def listen_for_speech(self, timeout=5, phrase_time_limit=10):
        """Listen for voice input from microphone"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = self.recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("I didn't catch that.")
            return None
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return None

    def take_photo_and_analyze(self, prompt="What do you think of me?"):
        """Capture photo and get AI analysis"""
        image_path, frame = self.capture_image()

        if image_path:
            self.speak("Let me look at you...")
            analysis = self.analyze_image(image_path, prompt)
            if analysis:
                self.speak(analysis)
                return analysis
            else:
                self.speak("I took the photo but couldn't analyze it.")
        else:
            self.speak("I tried to take a photo but couldn't access the camera.")
        return None

    def voice_command_loop(self):
        """Main loop for voice interactions"""
        greeting = "Good day. I am your Magic Mirror. How may I serve you today?"
        self.speak(greeting)

        active = True
        while active:
            user_input = self.listen_for_speech()

            if user_input is None:
                continue

            user_input = user_input.lower()

            if any(word in user_input for word in ["exit", "quit", "goodbye", "stop"]):
                self.speak("Until next time. May you continue to shine.")
                active = False
                break

            """When testing is over all commands to be diverted through here"""
            if "mirror mirror" in user_input:
                user_input = user_input.replace("mirror mirror", "").strip()
                """
                response = self.ask_ollama(user_input)
                    if response:
                        self.speak(response)
                    else:
                        print("No response from Ollama")
                """

            if any(
                word in user_input
                for word in [
                    "take photo",
                    "look at me",
                    "what do you think",
                    "what do you see",
                    "how do i look",
                    "how am i looking",
                    "how i look",
                    "what do you think of me",
                    "how do i look today",
                    "analyze me",
                    "look at",
                ]
            ):
                self.take_photo_and_analyze(user_input)
            else:
                response = self.ask_ollama(user_input)
                if response:
                    self.speak(response)
                else:
                    print("No response from Ollama")

    def run(self):
        """Start the Magic Mirror"""
        self.voice_command_loop()


def main():
    mirror = MagicMirror()
    mirror.run()


if __name__ == "__main__":
    main()
