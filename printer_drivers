import win32print

# This is the exact name of the printer as Windows knows it.
# The name is found in device manager.
PRINTER_NAME = r"POS-58 Printer"

def print_text(text: str):
    
    """
    Send plain text to the printer using the Windows print spooler.

    High level algorithm:
    1. Open a handle to the printer by name.
    2. Start a new print document in RAW mode (so bytes are sent as-is).
    3. Start a page in that document.
    4. Encode the text to bytes in a code page the printer understands.
    5. Send the bytes to the printer.
    6. End the page and the document.
    7. Close the printer handle.
    """

    # 1
    # Open a connection
    # If the name is wrong or the printer is not available, this will raise an error.
    hPrinter = win32print.OpenPrinter(PRINTER_NAME)

    try:
        # Document information tuple:
        # (document name (what appears in the print queue), 
        # output file (None = send directly to printer), 
        # data type (RAW = send bytes, dont interpret)).
        doc_info = ("Python POS Test", None, "RAW")

        # 2
        # Tell Windows we're starting a new print job
        win32print.StartDocPrinter(hPrinter, 1, doc_info)

        # 3
        # Start a "page" in the document.
        win32print.StartPagePrinter(hPrinter)

        # some extra paper so the text isn't printed right at the very edge.
        payload = text + "\n\n\n\n"

        # 4
        # Encode the Python string (Unicode) into a sequence of bytes.
        # "cp437" is a character set supported by ESC/POS printers.
        # errors="replace" is used to replace a char that cant be encoded with a placeholder,
        # instead of raising an exception (continues to print).
        data = payload.encode("cp437", errors="replace")

        # 5 
        win32print.WritePrinter(hPrinter, data)

        # 6
        # Signal end of page 
        win32print.EndPagePrinter(hPrinter)
        # Signal end of entire print job
        win32print.EndDocPrinter(hPrinter)

    # 7
    finally:
        # No matter if errors occur we close the job to not take up resources.
        win32print.ClosePrinter(hPrinter)

if __name__ == "__main__":
    print_text("Trust")
