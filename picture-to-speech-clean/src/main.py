import argparse
from recognition import load_templates
from tts import TTS
from interface import run_camera_loop

def parse_args():
    ap = argparse.ArgumentParser(description="Picture to Speech")
    ap.add_argument("--dataset", default="data/aac", help="Folder containing AAC icon images")
    ap.add_argument("--backend", choices=["pyttsx3", "gcloud"], default="pyttsx3", help="TTS backend")
    ap.add_argument("--voice", default=None, help="Voice name substring (pyttsx3) or exact voice name (gcloud)")
    ap.add_argument("--rate", type=int, default=None, help="Speech rate (pyttsx3 only)")
    ap.add_argument("--threshold", type=float, default=0.60, help="Confidence threshold for speaking")
    return ap.parse_args()

def main():
    args = parse_args()
    bank = load_templates(args.dataset)
    tts = TTS(backend=args.backend, voice=args.voice, rate=args.rate)
    run_camera_loop(bank, tts, confidence_threshold=args.threshold)

if __name__ == "__main__":
    main()
