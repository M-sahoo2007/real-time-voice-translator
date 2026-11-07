import os

import queue

import tempfile

import threading

import tkinter as tk

import webbrowser

from tkinter import ttk



import requests

import speech_recognition as sr

from gtts import gTTS

from playsound import playsound





# ========================= CONFIGURATION =========================



APP_TITLE = "LinguaSync - Real-Time Voice Translator"



LIBRETRANSLATE_URL = "http://127.0.0.1:5000"

LANGUAGES_URL = f"{LIBRETRANSLATE_URL}/languages"

TRANSLATE_URL = f"{LIBRETRANSLATE_URL}/translate"



REQUEST_TIMEOUT = 20

LANGUAGE_TIMEOUT = 10

LISTEN_TIMEOUT = 5

PHRASE_TIME_LIMIT = 10

PAUSE_BETWEEN_PHRASES = 1.5



SPEECH_CODES = {

    "en": "en-US", "hi": "hi-IN", "bn": "bn-IN",

    "es": "es-ES", "zh": "zh-CN", "ru": "ru-RU",

    "ja": "ja-JP", "ko": "ko-KR", "de": "de-DE",

    "fr": "fr-FR", "ta": "ta-IN", "te": "te-IN",

    "kn": "kn-IN", "gu": "gu-IN", "pa": "pa-IN",

}



TTS_CODES = {"zh": "zh-CN"}



PREFERRED_LANGUAGES = [

    "en", "hi", "bn", "es", "zh", "ru", "ja", "ko",

    "de", "fr", "ta", "te", "kn", "gu", "pa",

]



LANGUAGE_LABELS = {

    "en": "English", "hi": "Hindi", "bn": "Bengali",

    "es": "Spanish", "zh": "Chinese", "ru": "Russian",

    "ja": "Japanese", "ko": "Korean", "de": "German",

    "fr": "French", "ta": "Tamil", "te": "Telugu",

    "kn": "Kannada", "gu": "Gujarati", "pa": "Punjabi",

}





# ========================= GLOBAL STATE =========================



stop_event = threading.Event()

message_queue = queue.Queue()



worker_thread = None

keep_running = False

closing = False



available_languages = {}

language_targets = {}

language_mapping = {}





# ========================= TKINTER WINDOW =========================



win = tk.Tk()

win.title(APP_TITLE)

win.geometry("700x490")

win.resizable(False, False)



try:

    app_icon = tk.PhotoImage(file="icon.png")

    win.iconphoto(False, app_icon)

except (tk.TclError, OSError):

    app_icon = None





# ========================= GUI DESIGN =========================



tk.Label(

    win,

    text="LinguaSync: Real-Time Voice Translator",

    font=("Arial", 16, "bold"),

).pack(pady=10)



tk.Label(win, text="Recognized Text").pack()

input_text = tk.Text(win, height=5, width=65, wrap="word")

input_text.pack(pady=5)



tk.Label(win, text="Translated Text").pack()

output_text = tk.Text(win, height=5, width=65, wrap="word")

output_text.pack(pady=5)



status_label = tk.Label(

    win,

    text="Status: Connecting to LibreTranslate...",

    fg="blue",

)

status_label.pack(pady=8)



language_frame = tk.Frame(win)

language_frame.pack(pady=8)



tk.Label(language_frame, text="Input Language:").grid(

    row=0, column=0, padx=5

)

input_lang = ttk.Combobox(

    language_frame, state="readonly", width=18

)

input_lang.grid(row=0, column=1, padx=5)



tk.Label(language_frame, text="Output Language:").grid(

    row=0, column=2, padx=5

)

output_lang = ttk.Combobox(

    language_frame, state="readonly", width=18

)

output_lang.grid(row=0, column=3, padx=5)



button_frame = tk.Frame(win)

button_frame.pack(pady=12)



run_button = tk.Button(

    button_frame,

    text="Start Translation",

    command=lambda: run_translator(),

    width=18,

    bg="green",

    fg="white",

)

run_button.grid(row=0, column=0, padx=7)



kill_button = tk.Button(

    button_frame,

    text="Kill Execution",

    command=lambda: kill_execution(),

    width=18,

    bg="red",

    fg="white",

)

kill_button.grid(row=0, column=1, padx=7)



about_button = tk.Button(

    button_frame,

    text="About Project",

    command=lambda: open_about_page(),

    width=18,

)

about_button.grid(row=0, column=2, padx=7)





# ========================= GUI MESSAGE QUEUE =========================



def send_message(message_type, message=None):

    """Queue worker-thread results for the Tkinter main thread."""

    message_queue.put((message_type, message))





def set_status(message):

    """Update the status label from the Tkinter main thread only."""

    status_label.config(text=f"Status: {message}")





def process_messages():

    """Apply queued updates to GUI widgets on the main thread."""

    global keep_running

    global available_languages, language_targets, language_mapping



    if closing:

        return



    try:

        while True:

            message_type, message = message_queue.get_nowait()



            if message_type == "input":

                input_text.insert(tk.END, str(message) + "\n")

                input_text.see(tk.END)



            elif message_type == "output":

                output_text.insert(tk.END, str(message) + "\n")

                output_text.see(tk.END)



            elif message_type == "status":

                set_status(str(message))



            elif message_type == "languages":

                available_languages = message["available_languages"]

                language_targets = message["language_targets"]

                language_mapping = message["mapping"]



                display_names = message["display_names"]

                input_lang["values"] = display_names

                output_lang["values"] = display_names

                input_lang.set(message["input_default"])

                output_lang.set(message["output_default"])



                set_status(message["status"])

                run_button.config(state="normal")



            elif message_type == "language_error":

                set_status(str(message))

                run_button.config(state="disabled")



            elif message_type == "finished":

                keep_running = False

                run_button.config(state="normal")

                set_status(message or "Ready")



    except queue.Empty:

        pass

    except tk.TclError:

        return



    if not closing:

        try:

            win.after(100, process_messages)

        except tk.TclError:

            pass





# ========================= LOAD SERVER LANGUAGES =========================



def load_languages():

    """

    Load language data in a worker thread.

    This function deliberately does not access Tkinter widgets.

    """

    try:

        response = requests.get(

            LANGUAGES_URL,

            timeout=LANGUAGE_TIMEOUT,

        )

        response.raise_for_status()

        languages = response.json()



        new_available_languages = {}

        new_language_targets = {}



        for language in languages:

            code = language.get("code")

            name = language.get("name", code)



            if not code:

                continue



            new_available_languages[code] = LANGUAGE_LABELS.get(

                code, name

            )

            new_language_targets[code] = set(

                language.get("targets", [])

            )



        selected_codes = [

            code for code in PREFERRED_LANGUAGES

            if code in new_available_languages

        ]



        for code in new_available_languages:

            if code not in selected_codes:

                selected_codes.append(code)



        if not selected_codes:

            raise RuntimeError(

                "The translation server returned no supported languages."

            )



        display_names = [

            f"{new_available_languages[code]} ({code})"

            for code in selected_codes

        ]



        mapping = {

            f"{new_available_languages[code]} ({code})": code

            for code in selected_codes

        }



        input_default = (

            "English (en)"

            if "English (en)" in display_names

            else display_names[0]

        )

        output_default = (

            "Hindi (hi)"

            if "Hindi (hi)" in display_names

            else display_names[min(1, len(display_names) - 1)]

        )



        send_message(

            "languages",

            {

                "available_languages": new_available_languages,

                "language_targets": new_language_targets,

                "display_names": display_names,

                "mapping": mapping,

                "input_default": input_default,

                "output_default": output_default,

                "status": (

                    "LibreTranslate connected. "

                    f"{len(selected_codes)} languages loaded."

                ),

            },

        )



    except requests.exceptions.ConnectionError:

        send_message(

            "language_error",

            "Cannot connect to LibreTranslate. Start the local server.",

        )

    except requests.exceptions.Timeout:

        send_message(

            "language_error",

            "LibreTranslate connection timed out.",

        )

    except requests.exceptions.RequestException as error:

        send_message("language_error", f"Could not load languages: {error}")

    except (ValueError, RuntimeError) as error:

        send_message("language_error", str(error))

    except Exception as error:

        send_message(

            "language_error",

            f"Unexpected language-loading error: {error}",

        )





# ========================= TRANSLATION =========================



def translate_text(text, source, target):

    """Translate text using the local LibreTranslate API."""

    payload = {

        "q": text,

        "source": source,

        "target": target,

        "format": "text",

    }



    response = requests.post(

        TRANSLATE_URL,

        json=payload,

        timeout=REQUEST_TIMEOUT,

    )

    response.raise_for_status()



    translated = response.json().get("translatedText")

    if not translated:

        raise RuntimeError(

            "Translation server returned an empty result."

        )



    return translated





# ========================= TEXT TO SPEECH =========================



def speak_text(text, language_code):

    """Generate and play translated speech."""

    tts_code = TTS_CODES.get(language_code, language_code)

    audio_path = None



    try:

        with tempfile.NamedTemporaryFile(

            suffix=".mp3",

            delete=False,

        ) as audio_file:

            audio_path = audio_file.name



        speech = gTTS(text=text, lang=tts_code, timeout=15)

        speech.save(audio_path)



        if not stop_event.is_set():

            playsound(audio_path)



    finally:

        if audio_path and os.path.exists(audio_path):

            try:

                os.remove(audio_path)

            except OSError:

                pass





# ========================= TRANSLATION WORKER =========================



def translation_worker(source_code, target_code):

    """Run microphone recognition, translation, and speech in a worker."""

    recognizer = sr.Recognizer()

    recognizer.operation_timeout = 15

    final_status = "Ready"



    try:

        send_message("status", "Opening microphone...")



        with sr.Microphone() as microphone:

            send_message(

                "status",

                "Adjusting microphone for background noise...",

            )

            recognizer.adjust_for_ambient_noise(

                microphone,

                duration=0.5,

            )



            send_message("status", "Microphone ready. Speak now!")



            while not stop_event.is_set():

                try:

                    audio = recognizer.listen(

                        microphone,

                        timeout=LISTEN_TIMEOUT,

                        phrase_time_limit=PHRASE_TIME_LIMIT,

                    )

                except sr.WaitTimeoutError:

                    continue



                if stop_event.is_set():

                    break



                speech_language = SPEECH_CODES.get(

                    source_code, source_code

                )



                try:

                    speech_text = recognizer.recognize_google(

                        audio,

                        language=speech_language,

                    )

                except sr.UnknownValueError:

                    send_message(

                        "status",

                        "Speech not understood. Please speak again.",

                    )

                    continue

                except sr.RequestError as error:

                    raise RuntimeError(

                        f"Speech recognition service error: {error}"

                    ) from error



                if not speech_text.strip():

                    continue



                if speech_text.lower().strip() in {"stop", "exit"}:

                    final_status = "Stop command received."

                    break



                send_message("input", speech_text)



                if stop_event.is_set():

                    break



                send_message(

                    "status",

                    "Translating with LibreTranslate...",

                )



                try:

                    translated_text = translate_text(

                        speech_text, source_code, target_code

                    )

                except requests.exceptions.ConnectionError as error:

                    raise RuntimeError(

                        "Cannot connect to LibreTranslate. "

                        "Start the local server and try again."

                    ) from error

                except requests.exceptions.Timeout as error:

                    raise RuntimeError(

                        "LibreTranslate request timed out."

                    ) from error

                except requests.exceptions.HTTPError as error:

                    raise RuntimeError(

                        f"Translation API error: {error}"

                    ) from error



                if stop_event.is_set():

                    break



                send_message("output", translated_text)

                send_message(

                    "status",

                    "Generating translated voice...",

                )



                try:

                    speak_text(translated_text, target_code)

                except Exception as error:

                    raise RuntimeError(

                        f"Text-to-speech failed: {error}"

                    ) from error



                if stop_event.is_set():

                    break



                send_message(

                    "status",

                    "Translation completed. Listening...",

                )



                if stop_event.wait(PAUSE_BETWEEN_PHRASES):

                    break



    except OSError as error:

        final_status = f"Microphone or audio device error: {error}"

        send_message("output", final_status)



    except RuntimeError as error:

        final_status = str(error)

        send_message("output", final_status)



    except Exception as error:

        final_status = f"Application error: {error}"

        send_message("output", final_status)



    finally:

        if stop_event.is_set() and final_status == "Ready":

            final_status = "Translation stopped."

        send_message("finished", final_status)





# ========================= START / STOP =========================



def run_translator():

    """Validate language choices and start the translation worker."""

    global worker_thread, keep_running



    if keep_running:

        return



    if not language_mapping:

        set_status("Language list is not ready. Check LibreTranslate.")

        return



    source_code = language_mapping.get(input_lang.get())

    target_code = language_mapping.get(output_lang.get())



    if not source_code or not target_code:

        set_status("Select valid input and output languages.")

        return



    if source_code == target_code:

        set_status("Choose two different languages.")

        return



    if target_code not in language_targets.get(source_code, set()):

        set_status("This language pair is unavailable.")

        return



    stop_event.clear()

    keep_running = True



    input_text.delete("1.0", tk.END)

    output_text.delete("1.0", tk.END)



    run_button.config(state="disabled")

    set_status("Starting translation...")



    worker_thread = threading.Thread(

        target=translation_worker,

        args=(source_code, target_code),

        daemon=True,

        name="LinguaSyncTranslationWorker",

    )

    worker_thread.start()





def kill_execution():

    """Ask the worker to stop after its current blocking operation."""

    if keep_running:

        stop_event.set()

        set_status(

            "Stopping translation. Waiting for the current operation..."

        )





# ========================= ABOUT WINDOW =========================



def open_about_page():

    about = tk.Toplevel(win)

    about.title("About LinguaSync")

    about.geometry("430x300")

    about.resizable(False, False)



    if app_icon:

        try:

            about.iconphoto(False, app_icon)

        except tk.TclError:

            pass



    description = (

        "LinguaSync: Real-Time Voice Translator\n\n"

        "A Python desktop application for voice recognition, "

        "text translation, and translated speech output.\n\n"

        "Main technologies:\n"

        "Python, Tkinter, SpeechRecognition, PyAudio,\n"

        "LibreTranslate, Argos Translate, gTTS, and playsound.\n\n"

        f"Local translation server:\n{LIBRETRANSLATE_URL}\n\n"

        "Speech recognition and gTTS require internet access."

    )



    text_box = tk.Text(about, height=13, width=49, wrap="word")

    text_box.insert("1.0", description)

    text_box.config(state="disabled")

    text_box.pack(padx=10, pady=10)



    ttk.Button(

        about,

        text="Project Repository",

        command=lambda: webbrowser.open(

            "https://github.com/M-sahoo2007/real-time-voice-translator"

        ),

    ).pack(pady=4)





# ========================= APPLICATION CLOSE =========================



def close_application():
    """Request shutdown and wait for the translation worker to finish."""

    global closing

    if closing:
        return

    closing = True
    stop_event.set()

    try:
        run_button.config(state="disabled")
        kill_button.config(state="disabled")
        about_button.config(state="disabled")
        status_label.config(
            text="Status: Closing LinguaSync. Waiting for current operation..."
        )
        _finish_application_close()
    except tk.TclError:
        pass


def _finish_application_close():
    """Destroy the window only after the translation worker has stopped."""

    try:
        if worker_thread is not None and worker_thread.is_alive():
            win.after(150, _finish_application_close)
            return

        win.destroy()
    except tk.TclError:
        pass

win.protocol("WM_DELETE_WINDOW", close_application)





# ========================= APPLICATION STARTUP =========================



win.after(100, process_messages)



threading.Thread(

    target=load_languages,

    daemon=True,

    name="LinguaSyncLanguageLoader",

).start()



win.mainloop()
