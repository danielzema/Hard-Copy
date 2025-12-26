import datetime
import textwrap
import questionary
from questionary import Style
import google_calendar
import text_formatter
import printer_bluetooth

custom_style = Style([
    ('qmark', 'hidden'),
    ('question', 'fg:#eceff4 bold'),
    ('answer', 'fg:#88c0d0 bold'),
    ('pointer', 'fg:#88c0d0 bold'),
    ('highlighted', 'fg:#88c0d0 bold'),
    ('selected', 'fg:#a3be8c'),
    ('separator', 'fg:#4c566a'),
    ('instruction', 'fg:#4c566a italic'),
    ('text', 'fg:#d8dee9'),
])

W_ICON, W_TITLE, W_DESC = 4, 30, 30

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
        base = datetime.date.today()
        date_options = []
        for i in range(7):
            current_date = base + datetime.timedelta(days=i)
            raw_key = current_date.strftime("%Y-%m-%d")
            
            # Display Date in Day-Month-Year
            nice_date = current_date.strftime("%d-%m-%Y")
            day_name = current_date.strftime("%a")
            
            count = len(all_tasks.get(raw_key, []))
            day_label = "Today" if i == 0 else ("Tomorrow" if i == 1 else f"{day_name} {nice_date}")
            label = f"{day_label:<18} ({count} tasks)"
            date_options.append(questionary.Choice(title=label, value=raw_key))
        
        date_options.append(questionary.Separator())
        date_options.append(questionary.Choice(title="❌  Exit", value="EXIT"))

        selected_date = questionary.select("SELECT DATE:", choices=date_options, style=custom_style, pointer="»").ask()
        if selected_date in ["EXIT", None]: break

        while True:
            day_tasks = all_tasks.get(selected_date, [])
            task_choices = []
            
            if not day_tasks:
                task_choices.append(questionary.Separator(line="   (No tasks found)"))
            else:
                header = f"   {'TYPE':<{W_ICON}} {'TITLE':<{W_TITLE}} {'DESC'}"
                task_choices.append(questionary.Separator(line=header))
                task_choices.append(questionary.Separator(line="   " + "─" * (W_ICON + W_TITLE + W_DESC)))
                
                for t in day_tasks:
                    label = f"    √   {shorten(t['title'], W_TITLE):<{W_TITLE}} {shorten(t['description'], W_DESC)}"
                    task_choices.append(questionary.Choice(title=label, value=t))
            
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