# src/utils/output_formatter.py
"""
Formats payment transaction data into human-readable output strings.
Takes a transaction dictionary and creates formatted strings for both
console display and file logging purposes.

Handles both Venmo and Zelle transaction formats, including:
- Transaction date
- Sender information
- Payment amount
- Payment notes (Venmo)
- Confirmation numbers (Zelle)
- Account details (Zelle)

Returns a tuple of two strings:
1. Console output: Formatted for terminal display
2. File output: Formatted for log file writing

Each field uses fallback values if data is missing from the transaction.
"""

from typing import Dict

def format_output(transaction: Dict) -> tuple:
    """Format transaction for both console and file output"""
    console_output = [
        f"\nDate: {transaction.get('date', 'No date')}",
        f"Received from: {transaction.get('sender', 'Unknown sender')}",
        f"Amount: {transaction.get('amount', '$0.00')}",
        f"Note: {transaction.get('note', 'No note')}",  # Added for Venmo compatibility
        f"Confirmation: {transaction.get('confirmation', 'No confirmation')}",  # For Zelle
        f"Account: {transaction.get('account', 'No account info')}",  # For Zelle
        "---"
    ]
    
    file_output = console_output.copy()
    
    return (
        "\n".join(console_output),  # For console printing
        "\n".join(file_output)      # For file writing
    )
