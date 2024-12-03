# src/processors/zelle_processor.py
"""
Processes Navy Federal Zelle payment notification emails to extract transaction data.
Searches for recent Zelle payment emails, extracts transaction details, and outputs
the formatted results to both console and a text file. Handles up to 10 most recent
transactions and includes payment details with formatted dates.
"""

from .email_processor import EmailProcessor
from ..extractors.zelle_extractor import extract_zelle_data
from ..utils.output_formatter import format_output  # Remove write_transactions_to_file
import email
import email.utils
from datetime import datetime

class ZelleProcessor(EmailProcessor):
    def __init__(self, username: str, password: str, output_file: str = "output/zelle_transactions.txt"):
        super().__init__(username, password)
        self.output_file = output_file

    def search_emails(self):
        """Search for Navy Federal Zelle emails"""
        _, message_numbers = self.mail.search(
            None, 
            '(FROM "noreply@mail.navyfederal.org" SUBJECT "We deposited your payment")'
        )
        return message_numbers[0].split()

    def process_emails(self):
        """Process Zelle emails and extract transaction data"""
        email_ids = self.search_emails()
        recent_emails = email_ids[-10:] if len(email_ids) > 10 else email_ids
        transactions = []

        with open(self.output_file, "w") as output_file:
            for num in reversed(recent_emails):
                _, msg_data = self.mail.fetch(num, '(RFC822)')
                email_message = email.message_from_bytes(msg_data[0][1])
                
                # Get date
                date_tuple = email.utils.parsedate_tz(email_message['Date'])
                if date_tuple:
                    local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                    formatted_date = local_date.strftime("%A %b %d @ %H%M")

                # Get HTML content
                html_content = None
                for part in email_message.walk():
                    if part.get_content_type() == "text/html":
                        html_content = part.get_payload(decode=True).decode()
                        break

                if html_content:
                    try:
                        transaction = extract_zelle_data(html_content)
                        transaction['date'] = formatted_date
                        transactions.append(transaction)
                        
                        # Format and output the transaction
                        console_output, file_output = format_output(transaction)
                        print(console_output)
                        output_file.write(file_output + "\n")
                        
                    except Exception as e:
                        error_msg = f"Error processing email: {str(e)}"
                        print(error_msg)
                        output_file.write(error_msg + "\n")

        return transactions

