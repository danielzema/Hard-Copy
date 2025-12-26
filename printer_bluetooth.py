import serial          
import time
import text_formatter            

SERIAL_PORT = "COM4" # <- change to Bluetooth port

ESC_BOLD_ON = b'\x1b\x45\x01'   # Enable bold
ESC_BOLD_OFF = b'\x1b\x45\x00'  # Disable bold

def send_to_printer(data: bytes):
    # Open the serial connection to the printer.
    # "with" automatically closes the port.

    # Create object
    with serial.Serial(
        SERIAL_PORT,     
        # Speed
        baudrate=9600,
        # Data size
        bytesize=8,      
        # No parity bits needed?
        parity="N",       
        # One stop bit to tell serial communication that session is over.
        # change to 2 if channel is noisy
        stopbits=1,       
        timeout=1    
    ) as ser:
        
        ser.write(data)   
        # Force data to leave buffer
        ser.flush()      
        
        # Printer needs delay or it wont work all the time...
        time.sleep(0.3)

# Convert string to bytes
def print_text(text: str):
    # Replace em dash and en dash with regular hyphen for CP437 compatibility
    text = text.replace('–', '-').replace('—', '-')
    payload = text + "\n\n\n\n" 
    data = payload.encode("cp437", errors="replace")
    send_to_printer(data)

# Print text with multiple words in bold
def print_text_with_bold(text: str, bold_words):
    """Print text with specified words/phrases bolded."""
    # Replace em dash and en dash with regular hyphen for CP437 compatibility
    text = text.replace('–', '-').replace('—', '-')
    
    # Handle if bold_words is a string or list
    if isinstance(bold_words, str):
        bold_words = [bold_words]
    
    if not bold_words:
        print_text(text)
        return
    
    # Build bytes with bold commands for each bold word
    result = b""
    remaining_text = text
    
    for bold_word in bold_words:
        if not bold_word or bold_word not in remaining_text:
            continue
        
        # Find the bold word and split
        index = remaining_text.find(bold_word)
        if index != -1:
            # Add text before bold word
            result += remaining_text[:index].encode("cp437", errors="replace")
            # Add bold word with ESC commands
            result += ESC_BOLD_ON + bold_word.encode("cp437", errors="replace") + ESC_BOLD_OFF
            # Update remaining text
            remaining_text = remaining_text[index + len(bold_word):]
    
    # Add any remaining text
    result += remaining_text.encode("cp437", errors="replace")
    result += b"\n\n\n\n"
    send_to_printer(result)

if __name__ == "__main__":
    text, bold_words = text_formatter.format_single_task()
    print_text_with_bold(text, bold_words)