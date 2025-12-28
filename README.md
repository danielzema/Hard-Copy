# 🖨️ Hard Copy

Get things done by printing your To-Do-List as a physical receipt.

(This project was made for personal use, but an installationguide is provided on the bottom of this page.)

## How it works:
Hard Copy polls the Google Tasks API to retrieve your data and uses the Questionary library to provide an interactive, keyboard-driven menu system. Once you select a task, the app parses the data into a formatted receipt and transmits it via Bluetooth serial protocol or cable to a thermal ESC/POS printer that produces the receipt.

## Background and Inspiration
Digital tasks are incredibly efficient for organization and accessibility, but I suffer from a major flaw which this project is built on top of: "Out of sight, out of mind." Once I close my laptop and can't see my tasks, it feels like my goals are locked behind the screen. Writing the tasks down on a piece of paper solves this by existing in my real-world space, but manually keeping track of a digital and physical To-Do-List is double the work. Therefore I wanted to solve this by just printing my digital one.

Instead of printing a plain list of tasks I got inspired by my friend who works at a café. They keep track of orders via receipts: When an order is fulfilled a line is drawn over the receipt and then thrown away. Beyond keeping track of whose order is next, my friend told me that he gets a psychological "reward" seeing the pile of receipts shrink, which keeps him going in an otherwise very repetitive job. I've tried to recreate that feeling of dopamine in this project by printing tasks as receipts, with a box to be checked when fulfilled. For an even better "reward", consider buying a receipt pin to further demolish those tasks and see the pile of completed tasks grow! 

## Example Receipt
```text
+------------------------------+
|                              |
|         TASK RECEIPT         |  
|         ------------         |
|                              |
|  "Action is the foundational | <- Randomly chosen motivational quote for every receipt 
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
## 🛠️ Installation
This may not be for everyone, you will need to... 

Buy and configure a receipt printer, set up a Google Cloud project and clone this repository.

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
