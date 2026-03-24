"""
calendar_writer.py  ──  Write a .ics calendar file
Uses 'icalendar' instead of 'ics' (ics is broken on Python 3.14)
Install: pip install icalendar
"""

from icalendar import Calendar, Event
from datetime import datetime, timedelta
import config
import os


def write_ics(summary: str, start_time: str, duration_minutes: int = 30) -> None:
    """
    Create an iCalendar (.ics) file.

    Parameters
    ----------
    summary          : Event title e.g. "Dental Appointment"
    start_time       : ISO 8601 string  e.g. "2025-12-25T10:00:00"
    duration_minutes : Length of appointment in minutes (default 30)
    """
    cal = Calendar()
    cal.add('prodid', '-//Dental PC//EN')
    cal.add('version', '2.0')

    event = Event()
    event.add('summary', summary)

    # Parse the datetime string
    dt_start = datetime.fromisoformat(start_time)
    dt_end   = dt_start + timedelta(minutes=duration_minutes)

    event.add('dtstart', dt_start)
    event.add('dtend',   dt_end)
    event.add('description', 'Appointment booked via Dental PC System')

    cal.add_component(event)

    os.makedirs(config.DATA_DIR, exist_ok=True)
    path = config.ICS_FILE

    with open(path, 'wb') as f:
        f.write(cal.to_ical())

    print(f"📅 Calendar file saved → {path}")