# /// script
# dependencies = [
#   "numpy",
#   "openai",
#   "playsound3",
#   "sounddevice",
#   "scipy",
#   "httpx",
#   "pynput",
#   "pyperclip"
# ]
# ///

import os
import threading
import time

import numpy as np
import pyperclip
import sounddevice as sd
from openai import OpenAI
from playsound3 import playsound
from pynput import keyboard
from scipy.io.wavfile import write

# --- Configuration ---
OUTPUT_FILENAME = "recorded_audio.wav"
SAMPLE_RATE = 16000  # Standard audio sample rate
CHANNELS = 1

# --- Global Variables ---
is_recording = False
audio_frames = []
stream = None
indicator_thread = None


def recording_indicator():
    """Displays an indicator while recording."""
    try:
        playsound("start.mp3", block=False)
    except Exception as e:
        print(f"\nCould not play start sound: {e}")

    i = 0
    animation_frames = ["", ".", "..", "..."]
    while is_recording:
        padding = " " * (
            len(animation_frames[-1]) - len(animation_frames[i % len(animation_frames)])
        )

        print(
            f"🎤 Capturing audio{animation_frames[i % len(animation_frames)]}{padding}",
            end="\r",
        )
        i += 1
        time.sleep(0.5)
    print(" " * 30, end="\r")  # Clear the line


def start_recording():
    """Starts the audio recording process."""
    global is_recording, audio_frames, stream, indicator_thread
    if is_recording:
        return

    is_recording = True
    audio_frames = []
    indicator_thread = None

    try:
        indicator_thread = threading.Thread(target=recording_indicator)
        indicator_thread.start()

        def callback(indata, frames, time, status):
            if status:
                print(status)
            if is_recording:
                audio_frames.append(indata.copy())

        stream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback
        )
        stream.start()
    except Exception as e:
        print(f"\nFailed to start recording: {e}")
        is_recording = False
        if indicator_thread and indicator_thread.is_alive():
            indicator_thread.join()
        # Ensure stream is cleaned up if it was partially created
        if stream:
            try:
                stream.close()
            except Exception:
                pass  # Ignore errors during cleanup
            stream = None


def stop_recording():
    """Stops the audio recording and saves the file."""
    global is_recording, stream, indicator_thread
    if not is_recording:
        return

    is_recording = False
    if indicator_thread:
        indicator_thread.join()

    if stream:
        try:
            stream.stop()
            stream.close()
        except Exception as e:
            print(f"Error closing stream: {e}")
    stream = None

    if not audio_frames:
        print("No audio was recorded.")
        return

    try:
        recording = np.concatenate(audio_frames, axis=0)
        write(OUTPUT_FILENAME, SAMPLE_RATE, recording)
        print(f"Recording saved to {OUTPUT_FILENAME}")
    except Exception as e:
        print(f"Failed to save recording: {e}")
        return

    transcription = transcribe(OUTPUT_FILENAME)
    if transcription:
        print(f"Transcription: {transcription}")
        try:
            pyperclip.copy(transcription)
        except Exception as e:
            print(f"Failed to copy to clipboard: {e}")

        try:
            playsound("success.mp3", block=False)
        except Exception as e:
            print(f"Could not play success sound: {e}")


def transcribe(file_address: str) -> str:
    try:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            print("Error: OPENAI_API_KEY environment variable is not set")
            return ""
        client = OpenAI(api_key=key)
        with open(file_address, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                temperature=0.0,
                file=audio_file,
                prompt="Transcribe completely and exactly what is said. Language may be Persian or English. No summary. sentence prefrebly should be meningful. usually my sentences are about software development. ",
                response_format="text",
            )
        return transcription if isinstance(transcription, str) else ""
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""


def toggle_recording():
    """Toggles the recording state."""
    if is_recording:
        threading.Thread(target=stop_recording).start()
    else:
        threading.Thread(target=start_recording).start()


def main():
    """Main function to start the keyboard listener."""
    print("Audio recording script is running.")
    print("Press 'f9' to toggle recording.")

    def on_activate_hotkey():
        toggle_recording()

    # The hotkey to toggle recording
    hotkey = keyboard.GlobalHotKeys({"<f9>": on_activate_hotkey})
    hotkey.start()
    hotkey.join()


if __name__ == "__main__":
    main()
