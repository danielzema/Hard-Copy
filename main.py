import datetime
import textwrap
import questionary
from questionary import Style
import google_calendar
import text_formatter
import printer_bluetooth

# --- UI CONFIGURATION ---
# Professional "Nord" Theme: Clean, minimal, and high contrast without being neon.
custom_style = Style([
    ('qmark', 'hidden'),              # Hides the default (?)
    ('question', 'fg:#eceff4 bold'),  # Snow White for main headers
    ('answer', 'fg:#88c0d0 bold'),    # Calm Blue for the selected answer
    ('pointer', 'fg:#88c0d0 bold'),   # Calm Blue for the arrow
    ('highlighted', 'fg:#88c0d0 bold'), # Blue highlight
    ('selected', 'fg:#a3be8c'),       # Soft Green for checked items
    ('separator', 'fg:#4c566a'),      # Dark Grey for lines
    ('instruction', 'fg:#4c566a italic'), # Dark Grey for instructions
    ('text', 'fg:#d8dee9'),           # Off-white standard text
])

# --- COLUMN WIDTHS ---
W_ICON = 4
W_TIME = 10
W_TITLE = 35
W_DESC = 25

def shorten(text, limit):
    """Cuts text and adds '..' if too long."""
    if not text: return ""
    text = text.replace('\n', ' ') 
    return (text[:limit-3] + '...') if len(text) > limit else text

def main():
    print("\n   🖨️   HARD-COPY    \n")
    #print("   Fetching your schedule...\n")
    
    try:
        all_events = google_calendar.get_upcoming_data(7)
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return

    # --- OUTER LOOP: DATE SELECTION (MAIN SCREEN) ---
    while True:
        base = datetime.date.today()
        date_options = []
        
        # Build Date Menu
        for i in range(7):
            current_date = base + datetime.timedelta(days=i)
            date_str = current_date.strftime("%d-%m-%Y")
            nice_date = current_date.strftime("%a, %d %b")
            
            items = all_events.get(date_str, [])
            count = len(items)
            
            if i == 0: day_label = "TODAY"
            elif i == 1: day_label = "TOMORROW"
            else: day_label = nice_date.upper()

            # Format: "TODAY          (3 items)"
            label = f"{day_label:<12} ({count} items)"
            
            date_options.append(questionary.Choice(title=label, value=date_str))
        
        date_options.append(questionary.Separator())
        date_options.append(questionary.Choice(title="❌  Exit", value="EXIT"))

        selected_date_str = questionary.select(
            "SELECT DATE:",
            choices=date_options,
            style=custom_style,
            use_indicator=True,
            pointer="»"
        ).ask()

        if selected_date_str == "EXIT" or selected_date_str is None:
            print("Exiting. 👋")
            break

        # --- INNER LOOP: TASK SELECTION ---
        while True:
            day_events = all_events.get(selected_date_str, [])
            
            task_choices = []
            
            if not day_events:
                task_choices.append(questionary.Separator(line="   (No items for this day)"))
            else:
                header = (
                    f"   {'TYPE':<{W_ICON}} "
                    f"{'TIME':<{W_TIME}} "
                    f"{'TITLE':<{W_TITLE}} "
                    f"{'DESC'}"
                )
                underline = "   " + "─" * (W_ICON + W_TIME + W_TITLE + W_DESC)

                task_choices.append(questionary.Separator(line=header))
                task_choices.append(questionary.Separator(line=underline))
                
                for e in day_events:
                    is_task = e.get('type') == 'task' or e['time_label'] == '[Task]'
                    
                    if is_task:
                        icon = "√"
                        time_display = "Task"
                    else:
                        icon = "•"
                        time_display = e['time_label']

                    title_short = shorten(e['title'], W_TITLE)
                    desc_short = shorten(e['description'], W_DESC)
                    
                    label = (
                        f"{icon:<{W_ICON}} "
                        f"{time_display:<{W_TIME}} "
                        f"{title_short:<{W_TITLE}} "
                        f"{desc_short}"
                    )
                    
                    task_choices.append(questionary.Choice(title=label, value=e))
            
            task_choices.append(questionary.Separator(line=" ")) 
            task_choices.append(questionary.Choice(title="🔙  Go Back", value="BACK"))

            selected_event = questionary.select(
                "SELECT ITEM TO PREVIEW:",
                choices=task_choices,
                style=custom_style,
                use_indicator=True,
                pointer="»",
                instruction="(Use arrow keys to navigate)" 
            ).ask()

            if selected_event == "BACK" or selected_event is None:
                break # Go back to Date Menu

            # --- PREVIEW & PRINT ---
            print("\n" + "─"*50)
            print(f" 🔎 RECEIPT PREVIEW")
            print("─"*50)
            print(f" Title:  {selected_event['title']}")
            print(f" Time:   {selected_event['due']}")
            
            desc = selected_event.get('description', '')
            if desc:
                print(f" Desc:   {textwrap.fill(desc, width=50, initial_indent='', subsequent_indent='         ')}")
            else:
                print(f" Desc:   (None)")
            print("─" * 50)
            
            confirm = questionary.confirm(
                "🖨️   Print this receipt?", 
                default=True,
                style=custom_style,
                qmark="" 
            ).ask()

            if confirm:
                print("Sending to printer...")
                try:
                    text, bold_words = text_formatter.format_single_task_reciept(selected_event)
                    if bold_words:
                        printer_bluetooth.print_text_with_bold(text, bold_words)
                    else:
                        printer_bluetooth.print_text(text)
                    print("✅ Printed successfully!\n")
                    
                    # --- LOGIC UPDATE ---
                    # Break the inner loop to return to the Date Selection screen
                    break 
                    
                except Exception as e:
                    print(f"❌ Printer Error: {e}\n")
            else:
                print("Cancelled.\n")
                # Loop continues, staying on the Task Selection screen

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")