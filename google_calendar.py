import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

# Authenticate and get Google Tasks service
def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # if there are no (valid) credentials available
    if not creds or not creds.valid:
        # ask for new token if old
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                # Token refresh failed (likely expired), remove and regenerate
                print("   Outdated token: removing and generating a new one...")
                os.remove('token.json')
                creds = None
        
        # Generate new credentials if refresh failed or no valid creds exist
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # w for writing to the file
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Fetch upcoming tasks and group by date
def get_upcoming_data(days=7):
    creds = get_credentials()
    tasks_service = build('tasks', 'v1', credentials=creds)

    # Calculate time range
    now = datetime.datetime.utcnow()
    end_time = now + datetime.timedelta(days=days)
    # Convert to ISO 8601 format with 'Z' for UTC time
    # YYYY-MM-DDTHH:MM:SSZ
    iso_now = now.isoformat() + 'Z'
    iso_end = end_time.isoformat() + 'Z'

    grouped_data = {}

    # Fetch tasks from the primary task list 
    results = tasks_service.tasklists().list(maxResults=1).execute()
    items = results.get('items', [])

    # If there is a primary task list, fetch tasks due in the specified range 
    if items:
        # Only primary tasks needed, modify if needed
        tasklist_id = items[0]['id']
        tasks_result = tasks_service.tasks().list(
            tasklist=tasklist_id,
            showCompleted=False,
            dueMin=iso_now,
            dueMax=iso_end
        ).execute()

        # Process each task
        for task in tasks_result.get('items', []):
            # Extract title, description, and due date
            # if fields are missing, use defaults: 
            # None for description, 'No Title' for title
            title = task.get('title', 'No Title')
            # flatten to one line
            desc = task.get('notes', '').replace('\n', ' ').strip()
            due_raw = task.get('due')
            
            # Parse and format due date
            if due_raw:
                # Convert ISO 8601 string to datetime object
                dt_obj = datetime.datetime.fromisoformat(due_raw.replace('Z', '+00:00'))
                
                # Format date as Day-Month-Year (preferred in Sweden)
                date_str = dt_obj.strftime("%d-%m-%Y")

                # Include time if not an all-day task 
                if "T00:00:00" not in due_raw:
                    time_val = dt_obj.strftime("%H:%M")
                    due_string = f"{date_str} ({time_val})"
                else:
                    due_string = date_str

                raw_date_key = dt_obj.strftime("%Y-%m-%d")
            else: 
                # Handle tasks with NO due date
                due_string = "No Deadline"
                raw_date_key = "Someday" 

            # Create item data structure
            item_data = {
                "title": title,
                "description": desc,
                "due": due_string,
                "raw_date": dt_obj.strftime("%Y-%m-%d") # Used for internal grouping
            }

            # Group tasks by their raw date
            if item_data["raw_date"] not in grouped_data: 
                grouped_data[item_data["raw_date"]] = []
            grouped_data[item_data["raw_date"]].append(item_data)

    return grouped_data