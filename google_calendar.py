import datetime
import os
import os.path
import pathlib
import shutil
import webbrowser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

PROJECT_DIR = pathlib.Path(__file__).resolve().parent
TOKEN_PATH = PROJECT_DIR / 'token.json'


def _import_credentials_from_downloads_if_available(target_path: pathlib.Path):
    downloads_dir = pathlib.Path.home() / 'Downloads'
    if not downloads_dir.exists():
        return None

    candidates = sorted(downloads_dir.glob('client_secret*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        return None

    latest = candidates[0]
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(latest, target_path)
    return target_path


def _resolve_credentials_file():
    env_path = os.getenv('HARD_COPY_CREDENTIALS_PATH')
    search_paths = [
        pathlib.Path(env_path).expanduser() if env_path else None,
        PROJECT_DIR / 'credentials.json',
        pathlib.Path.cwd() / 'credentials.json',
        pathlib.Path.home() / '.config' / 'hard-copy' / 'credentials.json',
    ]

    google_app_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if google_app_creds:
        search_paths.append(pathlib.Path(google_app_creds).expanduser())

    for path in search_paths:
        if path and path.exists() and path.is_file():
            return path

    imported = _import_credentials_from_downloads_if_available(PROJECT_DIR / 'credentials.json')
    if imported:
        print(f"   Imported OAuth client file from Downloads: {imported}")
        return imported

    raise FileNotFoundError(
        "Google OAuth client file not found. Add credentials.json to the project root, "
        "or set HARD_COPY_CREDENTIALS_PATH to the JSON path from Google Cloud Console."
    )


def _run_oauth_flow(credentials_path: pathlib.Path):
    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)

    no_browser = os.getenv('HARD_COPY_OAUTH_NO_BROWSER', '').strip().lower() in {'1', 'true', 'yes'}

    try:
        if no_browser:
            raise RuntimeError('Browser launch disabled by HARD_COPY_OAUTH_NO_BROWSER')

        print('   Opening browser for Google authorization...')
        return flow.run_local_server(
            port=0,
            open_browser=True,
            authorization_prompt_message='Please visit this URL to authorize this application: {url}',
        )
    except Exception:
        print('   Browser authorization did not open. Falling back to terminal flow...')
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        print(f'   Open this URL and complete login:\n   {auth_url}')
        try:
            webbrowser.open(auth_url)
        except Exception:
            pass

        code = input('   Paste the authorization code here: ').strip()
        if not code:
            raise RuntimeError('No authorization code provided.')

        flow.fetch_token(code=code)
        return flow.credentials

# Authenticate and get Google Tasks service
def get_credentials():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    # if there are no (valid) credentials available
    if not creds or not creds.valid:
        # ask for new token if old
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                # Token refresh failed (likely expired), remove and regenerate
                print("   Outdated token: removing and generating a new one...")
                TOKEN_PATH.unlink(missing_ok=True)
                creds = None
        
        # Generate new credentials if refresh failed or no valid creds exist
        if not creds:
            credentials_path = _resolve_credentials_file()
            creds = _run_oauth_flow(credentials_path)
        # w for writing to the file
        with open(TOKEN_PATH, 'w') as token:
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
                "raw_date": raw_date_key # Used for internal grouping
            }

            # Group tasks by their raw date
            if item_data["raw_date"] not in grouped_data: 
                grouped_data[item_data["raw_date"]] = []
            grouped_data[item_data["raw_date"]].append(item_data)

    return grouped_data