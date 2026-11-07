from cx_Freeze import Executable, setup

build_exe_options = {
    "include_files": [
        ("icon.png", "icon.png"),
    ],
    "packages": [
        "tkinter",
        "speech_recognition",
        "pyaudio",
        "gtts",
        "playsound",
        "requests",
    ],
    "include_msvcr": True,
}

setup(
    name="LinguaSync",
    version="2.0.1",
    description="LinguaSync - Real-Time Voice Translator",
    options={
        "build_exe": build_exe_options,
    },
    executables=[
        Executable(
            "main.py",
            target_name="voice-translator.exe",
            base="gui",
            icon="icon.ico",
        )
    ],
)