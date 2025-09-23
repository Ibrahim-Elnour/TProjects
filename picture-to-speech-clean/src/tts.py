from typing import Optional
import os
import pyttsx3
try:
    from google.cloud import texttospeech
    _HAS_GCLOUD = True
except Exception:
    _HAS_GCLOUD = False

class TTS:
    def __init__(self, backend: str = "pyttsx3", voice: Optional[str] = None, rate: Optional[int] = None):
        self.backend = backend
        self.voice = voice
        self.rate = rate
        if backend == "pyttsx3":
            self.engine = pyttsx3.init()
            if rate is not None:
                self.engine.setProperty("rate", rate)
            if voice is not None:
                for v in self.engine.getProperty("voices"):
                    if voice.lower() in (v.name or "").lower():
                        self.engine.setProperty("voice", v.id)
                        break
        elif backend == "gcloud":
            if not _HAS_GCLOUD:
                raise RuntimeError("google-cloud-texttospeech not installed.")
            if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
                raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS env var for Google Cloud TTS.")
            self.client = texttospeech.TextToSpeechClient()
        else:
            raise ValueError("Unsupported TTS backend. Use 'pyttsx3' or 'gcloud'.")

    def speak(self, text: str, *, language_code: str = "en-US", voice_name: Optional[str] = None):
        if not text:
            return
        if self.backend == "pyttsx3":
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            input_text = texttospeech.SynthesisInput(text=text)
            voice_params = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name or "",
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = self.client.synthesize_speech(input=input_text, voice=voice_params, audio_config=audio_config)
            import tempfile, subprocess, sys, pathlib
            with tempfile.TemporaryDirectory() as td:
                mp3_path = pathlib.Path(td) / "out.mp3"
                mp3_path.write_bytes(response.audio_content)
                if sys.platform == "darwin":
                    subprocess.run(["afplay", str(mp3_path)], check=False)
                elif sys.platform.startswith("linux"):
                    subprocess.run(["mpg123", str(mp3_path)], check=False)
                elif sys.platform == "win32":
                    os.startfile(str(mp3_path))
