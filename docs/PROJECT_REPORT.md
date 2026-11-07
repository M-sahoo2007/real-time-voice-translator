# LinguaSync: Real-Time Voice Translator
## Project Documentation

### 1. Introduction
LinguaSync is a Python desktop application for spoken-language translation. It combines microphone speech recognition, text translation, and synthesized speech output.

### 2. Problem statement
A user may need a simple desktop workflow to convert spoken input from one language into another. LinguaSync brings recognition, translation, and voice playback into one graphical interface.

### 3. Objectives
- Capture speech from a microphone.
- Convert speech into text.
- Translate recognized text into a selected target language.
- Display recognized and translated text.
- Generate and play translated speech.
- Provide controls to start and request stopping the process.

### 4. Technologies
| Component | Technology |
|---|---|
| Language | Python |
| GUI | Tkinter |
| Microphone and recognition | PyAudio, SpeechRecognition |
| Speech recognition service | Google recognition service |
| Translation API | Local LibreTranslate |
| Translation engine | Argos Translate |
| Speech generation | gTTS |
| Audio playback | playsound |
| HTTP | Requests |
| EXE packaging | cx_Freeze |
| Installer | Inno Setup |

### 5. Workflow
1. User selects source and target languages.
2. Application opens the microphone.
3. SpeechRecognition captures a phrase and requests speech recognition.
4. Recognized text is displayed.
5. Text and language pair are sent to local LibreTranslate.
6. Translated text is displayed.
7. gTTS generates speech audio.
8. playsound plays the audio.
9. Listening continues until stop is requested or an error occurs.

### 6. Interface
The GUI contains recognized-text and translated-text areas, a status display, input/output language selectors, Start Translation, Kill Execution, and About Project controls.

### 7. Development testing summary
Reported development tests covered English-to-Hindi and Hindi-to-English translation, microphone recognition, translated voice playback, multiple phrases in one session, start/stop behavior, unavailable translation server, missing microphone, unavailable internet, executable launch, and installer installation/uninstallation. These are development-session test results, not independent validation on every Windows computer.

### 8. Requirements and limitations
- English and Hindi models were confirmed in the tested setup.
- Other languages require their corresponding supported models.
- Google speech recognition and gTTS require internet access.
- LibreTranslate and Argos language models are separate prerequisites and are not bundled in the desktop installer.
- A working microphone and audio output device are required.

### 9. Conclusion
LinguaSync demonstrates a desktop workflow for speech recognition, text translation, and translated speech playback. It has been packaged as a Windows executable and installer. Further validation should be performed on a clean Windows computer with the translation service and models installed.

### 10. Future enhancements
Potential improvements include expanding tested language coverage, adding offline speech recognition and offline text-to-speech, improving prerequisite checks, and adding user settings.
