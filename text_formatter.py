import time
import quotes

MAX_WIDTH = 30
MAX_TEXT_SPACE = MAX_WIDTH - 2 

# Class to enable printing of bold text
class BoldText(str):
    """Marker string subtype used to signal bold formatting."""

def bold(text: str) -> "BoldText":
    return BoldText(text)

def _unwrap_text_and_flag(text, bold_flag: bool):
    is_bold = bold_flag or isinstance(text, BoldText)
    return str(text), is_bold

#-----------------------------------------------------------------------------#
# Text formatting functions

def top_bottom_border(): 
    return "+" + "-" * MAX_WIDTH + "+"

def empty_line():
    return "|" + " " * MAX_WIDTH + "|"

def padded_text_left(text, bold=False):
    text_value, is_bold = _unwrap_text_and_flag(text, bold)
    lines = wrap_text(text_value)
    result = []
    for line in lines:
        if len(line) > MAX_TEXT_SPACE:
            result.append("| " + line[:MAX_TEXT_SPACE] + " |")
        else:
            padding = MAX_TEXT_SPACE - len(line)
            result.append("| " + line + " " * padding + " |")
    return ("\n".join(result), text_value if is_bold else None)

def padded_text_middle(text, bold=False):
    text_value, is_bold = _unwrap_text_and_flag(text, bold)
    lines = wrap_text(text_value)
    result = []
    for line in lines:
        if len(line) > MAX_TEXT_SPACE:
            result.append("| " + line[:MAX_TEXT_SPACE - 1] + " |")
        else:
            total_padding = MAX_TEXT_SPACE - len(line)
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding
            result.append("| " + " " * left_padding + line + " " * right_padding + " |")
    return ("\n".join(result), text_value if is_bold else None)

def wrap_text(text):
    if not text:
        return [""]
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if not current_line:
            current_line = word
        elif len(current_line) + 1 + len(word) <= MAX_TEXT_SPACE:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word 
    if current_line:
        lines.append(current_line)
    
    return lines

#-----------------------------------------------------------------------------#
# Receipt formatting functions

# ----- Headers --------------------------------------------------------------#
def format_reciept_header_quote():
    reciept, bold_reciept = padded_text_middle(bold("TASK RECEIPT"))
    line = padded_text_middle(len("TASK RECEIPT") * "-")[0]
    quote = quotes.get_random_quote()
    motivation_line, bold_quote = padded_text_middle(bold(quote))
    date_line = padded_text_left("Date: " + time.strftime("%A, " +"%d-%m-%Y"))[0]
    time_line = padded_text_left("Time: " + time.strftime("%H:%M"))[0]
    lines = [
        top_bottom_border(),
        empty_line(),
        reciept,
        line,
        empty_line(),
        motivation_line,
        empty_line(),
        date_line,
        time_line,
        empty_line(),
    ]
    full_text = "\n".join(lines)
    bold_words = [bw for bw in [bold_reciept, bold_quote] if bw]
    return (full_text, bold_words)

# ----- Body -----------------------------------------------------------------#

def format_single_task_body_google_calendar(title: str, description: str, due_date: str):
    task_line, bold_word = padded_text_left(bold("Task information"))
    separator_line = padded_text_left(len("Task information") * "-")[0]
    title_line = padded_text_left(title)[0]
    due_line = padded_text_left("Due: " + due_date)[0]
    
    lines = [
        task_line,
        separator_line,
        empty_line(),
        title_line,
        empty_line(),
    ]
    
    # Only add description if it actually exists (not empty)
    if description:
        desc_line = padded_text_left(description)[0]
        lines.append(desc_line)
        lines.append(empty_line())
        
    lines.append(due_line)
    lines.append(empty_line())
    
    full_text = "\n".join(lines)
    return (full_text, bold_word)

# ----- Footer ----------------------------------------------------------------#
def format_single_task_footer(): 
    footer_line, bold_word = padded_text_left(bold("Check when completed: [ ]"))
    lines = [
        top_bottom_border(),
        empty_line(),
        footer_line,
        empty_line(),
        top_bottom_border(),
    ]
    full_text = "\n".join(lines)
    return (full_text, bold_word)

# ----- Full Receipt ---------------------------------------------------------#
# THIS IS THE FUNCTION THAT WAS CAUSING THE ERROR
def format_single_task_reciept(task_data):
    """
    Accepts a dictionary 'task_data' containing: title, description, due
    """
    
    # 1. Header
    header_text, header_bold = format_reciept_header_quote()
    
    # 2. Body - Extract data from the dictionary here
    body_text, body_bold = format_single_task_body_google_calendar(
        title=task_data['title'], 
        description=task_data['description'], 
        due_date=task_data['due']
    )
    
    # 3. Footer
    footer_text, footer_bold = format_single_task_footer()
    
    full_text = header_text + "\n" + body_text + "\n" + footer_text
    
    bold_words = []
    if isinstance(header_bold, list):
        bold_words.extend(header_bold)
    elif header_bold:
        bold_words.append(header_bold)
    if body_bold:
        bold_words.append(body_bold)
    if footer_bold:
        bold_words.append(footer_bold)
    
    return (full_text, bold_words)