# LinguaSync User Manual

## Overview
LinguaSync listens through the microphone, recognizes spoken words, translates the text using local LibreTranslate, and plays translated speech.

## Before starting
- Connect a working microphone and audio output device.
- Install LibreTranslate and the required Argos language models.
- Ensure internet access is available for Google speech recognition and gTTS.
- The development setup was tested with English and Hindi translation models.

## Start the translation service
Run this in PowerShell and leave the terminal open:
```powershell
libretranslate --host 127.0.0.1 --port 5000 --load-only en,hi
```

## Translate speech
1. Launch LinguaSync.
2. Select the spoken language under **Input Language**.
3. Select a different target under **Output Language**.
4. Click **Start Translation**.
5. Wait for the microphone-ready status, then speak clearly.
6. Review **Recognized Text** and **Translated Text**.
7. Listen to the generated translated speech.

## Stop
Click **Kill Execution**. The worker stops after its current blocking operation completes. A network request or audio playback already in progress may take some time to finish. The spoken words `stop` and `exit` are also treated as stop commands.

## About Project
Click **About Project** to view application information and the repository link.

## Troubleshooting
- **LibreTranslate connection error:** Start the local server and confirm `http://127.0.0.1:5000` is reachable.
- **No microphone:** Check Windows microphone permissions and the default input device.
- **Speech recognition error:** Check internet connectivity.
- **Language pair unavailable:** Install the required models and verify the pair is supported by LibreTranslate.
- **No translated voice:** Check internet connectivity and audio output.

## Connectivity and privacy
Speech recognition uses Google's online recognition service, and gTTS generates speech online. The application is not fully offline. Avoid speaking confidential information unless you are comfortable using an online speech-recognition service.
