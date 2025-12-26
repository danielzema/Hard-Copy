import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_upcoming_data(days=7):
    creds = get_credentials()
    tasks_service = build('tasks', 'v1', credentials=creds)

    now = datetime.datetime.utcnow()
    end_time = now + datetime.timedelta(days=days)
    iso_now = now.isoformat() + 'Z'
    iso_end = end_time.isoformat() + 'Z'

    grouped_data = {}
    
    results = tasks_service.tasklists().list(maxResults=1).execute()
    items = results.get('items', [])
    
    if items:
        tasklist_id = items[0]['id']
        tasks_result = tasks_service.tasks().list(
            tasklist=tasklist_id,
            showCompleted=False,
            dueMin=iso_now,
            dueMax=iso_end
        ).execute()

        for task in tasks_result.get('items', []):
            title = task.get('title', 'No Title')
            desc = task.get('notes', '').replace('\n', ' ').strip()
            due_raw = task.get('due')

            if due_raw:
                dt_obj = datetime.datetime.fromisoformat(due_raw.replace('Z', '+00:00'))
                
                # Format date as Day-Month-Year
                date_str = dt_obj.strftime("%d-%m-%Y")
                
                if "T00:00:00" not in due_raw:
                    time_val = dt_obj.strftime("%H:%M")
                    due_string = f"{date_str} ({time_val})"
                else:
                    due_string = date_str 

                item_data = {
                    "title": title,
                    "description": desc,
                    "due": due_string,
                    "raw_date": dt_obj.strftime("%Y-%m-%d") # Used for internal grouping
                }

                if item_data["raw_date"] not in grouped_data: 
                    grouped_data[item_data["raw_date"]] = []
                grouped_data[item_data["raw_date"]].append(item_data)

    return grouped_data