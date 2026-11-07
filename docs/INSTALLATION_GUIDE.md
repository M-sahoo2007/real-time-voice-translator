# LinguaSync Installation Guide (Windows)

1. Obtain `LinguaSync_Setup.exe`.
2. Run the installer and follow the setup wizard.
3. Select the optional desktop shortcut if desired.
4. Finish installation and launch LinguaSync.

## Separate translation-service setup
The Windows installer contains the desktop application, not LibreTranslate or Argos language models. Install LibreTranslate and the required models separately. For the tested English/Hindi setup, start:
```powershell
libretranslate --host 127.0.0.1 --port 5000 --load-only en,hi
```
Keep the server running before launching LinguaSync.

## Internet requirement
Internet access is required for Google speech recognition and gTTS. Text translation uses the local LibreTranslate service and its installed models.

## Uninstall
Open **Windows Settings → Apps → Installed apps**, select **LinguaSync**, and choose **Uninstall**.
