# 🖨️ Hard Copy

Get things done by printing your To-Do-List as a physical receipt.

## How it works:
Hard Copy polls the Google Tasks API to retrieve your data and uses the Questionary library to provide an interactive, keyboard-driven menu system. Once you select a task, the app parses the data into a receipt format and transmits it via Bluetooth serial protocol to a thermal ESC/POS printer that produces the receipt.

## Background ## 
Digital tasks are incredibly efficient for organization, but they suffer from a major flaw: "Out of sight, out of mind." Once you close a tab or lock your phone, your goals vanish behind a screen. A physical copy of your tasks solves this by existing in your real-world space. They sit on your desk, unignorable, and stare at you waiting to be completed. Beyond visibility, there is the psychological "reward." Physically marking a check-box on a paper receipt provides a sense of accomplishment that a digital interface simply cannot replicate.

## Example Receipt
```text
+------------------------------+
|                              |
|         TASK RECEIPT         |  
|         ------------         |
|                              |
|  "Action is the foundational | <- Randomly chosen 
|   key to all success."       |    motivational quote
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
| Don't forget to ask Adam     | <- Description/Comments
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
## 🛠️ Installation

### 1. Clone the Repository
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

### 4. Printer Configuration
Pair your ESC/POS thermal printer via Bluetooth.

Identify your COM Port (Windows: Device Manager → Ports).

Open printer_bluetooth.py and update the SERIAL_PORT variable:

```python
SERIAL_PORT = "COM4"  # Replace with your actual port
```

## 🚀 Usage
Run the application:

```bash
python main.py
```
