# 🎙️ OpenSuperWhisper Transcriber

![Doge](doge.jpg)

A Python script that records audio from your microphone, transcribes it using OpenAI's Speech-To-Text, and copies the text to your clipboard. It uses a global hotkey to start and stop recording, making it easy to capture audio from any application.

## ✨ Features

- **⌨️ Global Hotkey**: Press `F9` anywhere in your OS to start or stop recording.
- **🔊 Audio Cues**: Plays sounds to indicate the start of recording and successful transcription.
- **✍️ Automatic Transcription**: Uses the OpenAI API for high-quality audio-to-text conversion.
- **📋 Clipboard Integration**: Automatically copies the transcribed text to the clipboard for immediate use.


## 🛠️ Prerequisites

- Python 3.13+
- An OpenAI API key
- uv

## 🚀 Installation

1.  **Clone the repository (or download the script):**
    ```bash
    git clone https://github.com/bbkgh/opensuperwhisper.git
    cd opensuperwhisper
    ```

2.  **Set your OpenAI API Key:**
    The script requires your OpenAI API key to be set as an environment variable.

    For Linux/macOS:
    ```bash
    export OPENAI_API_KEY='your_openai_api_key'
    ```
    
    And possibly `https_proxy` environment variable
    
    To make this permanent, add it to your shell's profile script (e.g., `.zshrc`, `.bashrc`, or your PowerShell profile).

## ▶️ Usage

1.  **Run the script from your terminal:**
    ```bash
    uv run main.py
    ```
    The script will run in the background and listen for the hotkey.

2.  **Start/Stop Recording:**
    - Press `F9` to start recording. You will hear a "start" sound.
    - Press `F9` again to stop recording.

3.  **Get Your Transcription:**
    - After stopping the recording, the script saves the audio to `recorded_audio.wav`.
    - It then sends the audio to the OpenAI API for transcription.
    - The transcribed text is printed to the console and copied to your clipboard. You will hear a "success" sound.

## ⚙️ Customization

You can modify the following constants in `main.py`:
- `hotkey`: Change the key combination for toggling the recording in the `main` function.
- `prompt`: In the `transcribe` function, you can change the prompt sent to OpenAI to better suit your needs. 


##  Problems

- Shortcut activation doesn't work in some apps. For capturing them you can use keboard library (run as sudo)
- Streaming/Online transcription and filling text boxes (high latency)