import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/tasks.readonly'
]

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_upcoming_data(days=7):
    creds = get_credentials()
    calendar_service = build('calendar', 'v3', credentials=creds)
    tasks_service = build('tasks', 'v1', credentials=creds)

    now = datetime.datetime.utcnow()
    end_time = now + datetime.timedelta(days=days)
    iso_now = now.isoformat() + 'Z'
    iso_end = end_time.isoformat() + 'Z'

    grouped_data = {}
    
    # 1. CALENDAR
    events_result = calendar_service.events().list(
        calendarId='primary', timeMin=iso_now, timeMax=iso_end,
        singleEvents=True, orderBy='startTime'
    ).execute()
    
    for event in events_result.get('items', []):
        title = event.get('summary', 'No Title')
        # --- CHANGE: Empty string if no description ---
        desc = event.get('description', '').replace('\n', ' ').strip()
        
        start = event['start'].get('dateTime', event['start'].get('date'))
        if 'T' in start:
            dt_obj = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
            date_str = dt_obj.strftime("%Y-%m-%d")
            time_label = dt_obj.strftime("%H:%M")
        else:
            date_str = start
            time_label = "All Day"

        item = {
            "title": title,
            "description": desc,
            "due": f"{date_str} at {time_label}",
            "time_label": time_label,
            "raw_date": date_str
        }
        if date_str not in grouped_data: grouped_data[date_str] = []
        grouped_data[date_str].append(item)

    # 2. TASKS
    results = tasks_service.tasklists().list(maxResults=1).execute()
    items = results.get('items', [])
    if items:
        tasklist_id = items[0]['id']
        tasks_result = tasks_service.tasks().list(
            tasklist=tasklist_id, showCompleted=False, dueMin=iso_now, dueMax=iso_end
        ).execute()

        for task in tasks_result.get('items', []):
            title = task.get('title', 'No Title')
            # --- CHANGE: Empty string if no description ---
            desc = task.get('notes', '').replace('\n', ' ').strip()
            due_raw = task.get('due')

            if due_raw:
                dt_obj = datetime.datetime.fromisoformat(due_raw.replace('Z', '+00:00'))
                date_str = dt_obj.strftime("%Y-%m-%d")
                
                item = {
                    "title": title,
                    "description": desc,
                    "due": f"{date_str} (Task)",
                    "time_label": "[Task]",
                    "raw_date": date_str
                }
                if date_str not in grouped_data: grouped_data[date_str] = []
                grouped_data[date_str].append(item)

    return grouped_data
