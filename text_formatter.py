import time
import quotes

MAX_WIDTH = 30
MAX_TEXT_SPACE = MAX_WIDTH - 2 

# String in parentheses makes this class inherit string behavior
class BoldText(str):
    """Marker string subtype used to signal bold formatting."""

# Function to create BoldText instances
def bold(text: str) -> "BoldText":
    return BoldText(text)

# Helper to unwrap text and determine bold status
def _unwrap_text_and_flag(text, bold_flag: bool):
    is_bold = bold_flag or isinstance(text, BoldText)
    return str(text), is_bold

def top_bottom_border(): 
    return "+" + "-" * MAX_WIDTH + "+"

def empty_line():
    return "|" + " " * MAX_WIDTH + "|"

def padded_text_left(text, bold=False):
    text_value, is_bold = _unwrap_text_and_flag(text, bold)
    lines = wrap_text(text_value)
    result = []
    for line in lines:
        padding = MAX_TEXT_SPACE - len(line)
        result.append("| " + line + " " * padding + " |")
    return ("\n".join(result), text_value if is_bold else None)

def padded_text_middle(text, bold=False):
    text_value, is_bold = _unwrap_text_and_flag(text, bold)
    lines = wrap_text(text_value)
    result = []
    for line in lines:
        total_padding = MAX_TEXT_SPACE - len(line)
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        result.append("| " + " " * left_padding + line + " " * right_padding + " |")
    return ("\n".join(result), text_value if is_bold else None)

def wrap_text(text):
    if not text: return [""]
    words = text.split()
    lines, current_line = [], ""
    for word in words:
        if not current_line:
            current_line = word
        elif len(current_line) + 1 + len(word) <= MAX_TEXT_SPACE:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word 
    if current_line: lines.append(current_line)
    return lines

def format_reciept_header_quote():
    reciept, bold_reciept = padded_text_middle(bold("TASK RECEIPT"))
    line = padded_text_middle(len("TASK RECEIPT") * "-")[0]
    quote = quotes.get_random_quote()
    motivation_line, bold_quote = padded_text_middle(bold(quote))
    
    date_line = padded_text_left("Date: " + time.strftime("%d-%m-%Y"))[0]
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
    return ("\n".join(lines), [bw for bw in [bold_reciept, bold_quote] if bw])

def format_single_task_body(title: str, description: str, due_date: str):
    task_line, bold_word = padded_text_left(bold("Task Information"))
    sep = padded_text_left(len("Task Information") * "-")[0]
    title_line = padded_text_left(title)[0]
    due_line = padded_text_left("Due: " + due_date)[0]
    
    lines = [task_line, sep, empty_line(), title_line, empty_line()]
    if description:
        lines.append(padded_text_left(description)[0])
        lines.append(empty_line())
    lines.append(due_line)
    lines.append(empty_line())
    return ("\n".join(lines), bold_word)

def format_single_task_footer(): 
    footer_line, bold_word = padded_text_left(bold("Check when completed: [ ]"))
    lines = [top_bottom_border(), empty_line(), footer_line, empty_line(), top_bottom_border()]
    return ("\n".join(lines), bold_word)

def format_single_task_reciept(task_data):
    header_text, header_bolds = format_reciept_header_quote()
    body_text, body_bold = format_single_task_body(task_data['title'], task_data['description'], task_data['due'])
    footer_text, footer_bold = format_single_task_footer()
    full_text = header_text + "\n" + body_text + "\n" + footer_text
    all_bolds = header_bolds + ([body_bold] if body_bold else []) + ([footer_bold] if footer_bold else [])
    return (full_text, all_bolds)