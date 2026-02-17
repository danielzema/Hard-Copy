# 🖨️ Hard Copy

Get things done by printing your To-Do-List as a physical receipt.

## Notes
This project was first made for personal use in a private repository, but later copied to this public repository and modified for general use.

An installationguide is provided on the bottom of this page.

## How it works:
Hard Copy polls the Google Tasks API to retrieve your data and uses the Questionary library to provide an interactive, keyboard-driven menu system. Once you select a task, the app parses the data into a formatted receipt and transmits it via Bluetooth serial protocol or cable to a thermal ESC/POS printer that produces the receipt.

## Background and Inspiration
Digital tasks are incredibly efficient for organization and accessibility, but I suffer from a flaw which make them less usable for me: "Out of sight, out of mind." Writing the tasks down on a piece of paper solves this by existing in my real-world space, but manually keeping track of a digital and physical To-Do-List is double the work. Therefore I wanted to solve this by just printing my digital one.

I got inspired by my friend who works at a café and keeps track of orders via receipts: When an order is fulfilled a line is drawn over the receipt and then thrown away. Beyond keeping track of whose order is next, my friend told me that he gets a psychological "reward" seeing the pile of receipts shrink, which keeps him going in an otherwise very repetitive job. I've tried to recreate that feeling of dopamine in this project by printing tasks as receipts, with a box to be checked when fulfilled. 

## Example Receipt
```text
+------------------------------+
|                              |
|         TASK RECEIPT         |  
|         ------------         |
|                              |
|  "Action is the foundational | <- Randomly chosen motivational quote or proverb for every receipt 
|   key to all success."       |   
|                              |
| Date: 28-12-2025             | <- Print date and time
| Time: 15:30                  |
|                              |
+------------------------------+
|                              |
| Task Information             |
| ----------------             |
|                              |
| Write READ.ME                | <- Task title
|                              |
| Don't forget to ask Adam     | <- Description and comments
| about the structure.         |
|                              | 
| Due: 28-12-2025 at 17:00     | <- Due date 
|                              |
+------------------------------+
|                              |
| Check when completed: [ ]    | <- Checkbox
|                              |
+------------------------------+
```
## Installation
This may not be for everyone, you will need to... 

Buy and configure a receipt printer, set up a Google Cloud project and clone this repository.

### 1. Clone this Repository
Python 3.7+ is required.

```bash
git clone https://github.com/danielzema/hard-copy.git

cd hard-copy
```

### 2. Install Dependencies
```bash
pip install google-api-python-client google-auth-oauthlib questionary pyserial
```
### 3. Google API Setup
Go to the Google Cloud Console.

Create a new project and enable the Google Tasks API.

Go to Credentials → Create Credentials → OAuth 2.0 Client IDs (Select "Desktop App").

Download the JSON file, rename it to credentials.json, and place it in the root folder of this project.

Alternative (no rename needed):

```bash
HARD_COPY_CREDENTIALS_PATH=/full/path/to/client_secret_xxx.json python main.py
```

The app can also auto-import the newest `client_secret*.json` from `~/Downloads` on first run.

If browser popup does not open on macOS, the app now falls back to terminal auth and prints a login URL + code prompt.
You can force this mode with:

```bash
HARD_COPY_OAUTH_NO_BROWSER=1 python main.py
```

### 4. Printer Configuration
Pair your ESC/POS thermal printer via Bluetooth.

Identify your COM Port (Windows: Device Manager → Ports).

Open ```printer_bluetooth.py``` and update the ```SERIAL_PORT``` variable:

```python
SERIAL_PORT = "COM4"  # Replace with your actual port
```

## Usage
Run the application:
The Questionary menu will guide you further.

```bash
python main.py
```
