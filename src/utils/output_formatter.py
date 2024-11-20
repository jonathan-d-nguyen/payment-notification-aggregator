# src/utils/output_formatter.py
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
