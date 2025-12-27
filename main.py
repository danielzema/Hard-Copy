import datetime
import textwrap
import questionary
from questionary import Style
import google_calendar
import text_formatter
import printer_bluetooth

# Custom style for questionary prompts
custom_style = Style([
    ('qmark', 'hidden'), # Hide the question mark
    ('question', 'fg:#eceff4 bold'), # question text
    ('answer', 'fg:#88c0d0 bold'), # submitted answer text behind the question
    ('pointer', 'fg:#88c0d0 bold'), # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#88c0d0 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#a3be8c'), # style for selected choices
    ('separator', 'fg:#4c566a'), # separator lines
    ('instruction', 'fg:#4c566a italic'), # instructions text
    ('text', 'fg:#d8dee9'), # regular text
])

# Column widths for display
W_ICON, W_TITLE, W_DESC = 4, 30, 30

# Function to shorten text with ellipsis
def shorten(text, limit):
    if not text: return ""
    text = text.replace('\n', ' ') 
    return (text[:limit-2] + '..') if len(text) > limit else text

def main():
    print("\n   🖨️   HARD COPY")
    print("   Fetching tasks...\n")
    
    try:
        all_tasks = google_calendar.get_upcoming_data(7)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    while True:
        # Date Selection
        base = datetime.date.today()
        # Generate date options for the next 7 days
        date_options = []
        for i in range(7):
            current_date = base + datetime.timedelta(days=i)
            raw_key = current_date.strftime("%Y-%m-%d")
            
            # Display Date in Day-Month-Year 
            nice_date = current_date.strftime("%d-%m-%Y")
            day_name = current_date.strftime("%a")

            # Count tasks for the current date
            count = len(all_tasks.get(raw_key, []))
            day_label = "Today" if i == 0 else ("Tomorrow" if i == 1 else f"{day_name} {nice_date}")
            label = f"{day_label:<18} ({count} tasks)"
            date_options.append(questionary.Choice(title=label, value=raw_key))
        
        # Add exit option
        date_options.append(questionary.Separator())
        date_options.append(questionary.Choice(title="❌  Exit", value="EXIT"))

        selected_date = questionary.select("SELECT DATE:", choices=date_options, style=custom_style, pointer="»").ask()
        if selected_date in ["EXIT", None]: break

        while True:
            day_tasks = all_tasks.get(selected_date, [])
            task_choices = []
            
            # Task Selection
            if not day_tasks:
                task_choices.append(questionary.Separator(line="   (No tasks found)"))
            else:
                header = f"   {'TYPE':<{W_ICON}} {'TITLE':<{W_TITLE}} {'DESC'}"
                task_choices.append(questionary.Separator(line=header))
                task_choices.append(questionary.Separator(line="   " + "─" * (W_ICON + W_TITLE + W_DESC)))
                
                # Populate tasks
                for t in day_tasks:
                    label = f"    √   {shorten(t['title'], W_TITLE):<{W_TITLE}} {shorten(t['description'], W_DESC)}"
                    task_choices.append(questionary.Choice(title=label, value=t))
            
            # Add go back option
            task_choices.append(questionary.Separator())
            task_choices.append(questionary.Choice(title="🔙  Go Back", value="BACK"))

            selected_task = questionary.select("SELECT TASK:", choices=task_choices, style=custom_style, pointer="»").ask()
            if selected_task in ["BACK", None]: break

            # Preview Section
            print("\n" + "─"*50 + f"\n 🔎 PREVIEW RECEIPT\n" + "─"*50)
            print(f" Title:  {selected_task['title']}")
            print(f" Due:    {selected_task['due']}") 
            print(f" Desc:   {textwrap.fill(selected_task['description'] or '(None)', width=50, subsequent_indent='         ')}")
            print("─" * 50)
            
            if questionary.confirm("🖨️  Print this task?", default=True, style=custom_style, qmark="").ask():
                try:
                    text, bold_words = text_formatter.format_single_task_reciept(selected_task)
                    printer_bluetooth.print_text_with_bold(text, bold_words) if bold_words else printer_bluetooth.print_text(text)
                    print("✅ Printed successfully!\n")
                    break
                except Exception as e:
                    print(f"❌ Printer Error: {e}\n")
            else:
                print("Cancelled.\n")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\nExiting.")