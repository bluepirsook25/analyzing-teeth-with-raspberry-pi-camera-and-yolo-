"""
main.py  ──  Dental PC Orchestrator
Run: python main.py
"""

import time
import webbrowser
import pyttsx3

import config
from pi_controller import capture_and_download
from analyzer import analyze_teeth
from database import create_appointment
from calendar_writer import write_ics

# ── Voice engine ──────────────────────────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', 160)   # speaking speed (words/min)

def speak(text: str) -> None:
    print(f"🤖 {text}")
    engine.say(text)
    engine.runAndWait()

# ── Main pipeline ─────────────────────────────────────────────────────────────
def main_pipeline() -> None:
    speak("Welcome to Dental PC System.")
    speak("Ensure your Raspberry Pi is on and connected to the same Wi-Fi.")
    time.sleep(1)

    # 1. Capture image via SSH → Pi Camera → SFTP download
    speak("Initiating camera on Raspberry Pi.")
    if not capture_and_download():
        speak("Failed to capture image. Please check Pi connection and try again.")
        return

    # 2. Analyse with YOLOv8n-seg + PIL histogram
    speak("Analysing teeth structure and colour. Please wait.")
    issue, details = analyze_teeth()
    print(f"\n📊 Analysis Result: {details}\n")

    # 3. Act on result
    if issue:
        speak(f"Issue detected: {issue} anomaly found in your teeth.")
        speak("Would you like to book an appointment? Press 1 for Yes, 2 for No.")

        choice = input("Enter choice (1 = Yes / 2 = No): ").strip()

        if choice == '1':
            speak("Opening booking website. Please complete the form.")
            webbrowser.open('http://127.0.0.1:5000/login')

            speak("I will wait 30 seconds while you complete the booking.")
            time.sleep(30)

            # Record appointment (dummy data – website form updates DB directly)
            create_appointment("Dr. Smith", "2025-12-25 10:00:00")
            write_ics("Dental Appointment", "2025-12-25T10:00:00")

            speak("Appointment saved to database and calendar file.")
            speak("Check data/appointments.ics to add it to your calendar app.")

        elif choice == '2':
            speak("No appointment booked. Take care of your teeth!")
        else:
            speak("Invalid choice. Exiting.")

    else:
        speak("Everything looks great. No issues detected. Keep up the good dental hygiene!")

    speak("Dental PC session complete. Goodbye!")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main_pipeline()
