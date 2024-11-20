# src/processors/venmo_processor.py
from .email_processor import EmailProcessor
from ..extractors.venmo_extractor import extract_venmo_data
from ..utils.output_formatter import format_output
import email
import email.utils
from datetime import datetime
from typing import List, Dict

class VenmoProcessor(EmailProcessor):
    def __init__(self, username: str, password: str, output_file: str = "output/venmo_transactions.txt"):
        super().__init__(username, password)
        self.output_file = output_file

    def search_emails(self) -> List[str]:
        """Search for Venmo payment emails"""
        search_criteria = [
            '(FROM "venmo@venmo.com" SUBJECT "paid you")',
            '(FROM "venmo@venmo.com" SUBJECT "You paid")'
        ]
        
        all_email_ids = []
        for criteria in search_criteria:
            _, message_numbers = self.mail.search(None, criteria)
            all_email_ids.extend(message_numbers[0].split())
        
        return all_email_ids

    def process_emails(self) -> List[Dict]:
        """Process Venmo emails and extract transaction data"""
        email_ids = self.search_emails()
        
        # Sort email IDs by date (assuming they're sequential)
        email_ids.sort(reverse=True)
        
        # Get the 10 most recent emails
        recent_emails = email_ids[:10] if len(email_ids) > 10 else email_ids
        transactions = []

        with open(self.output_file, "w") as output_file:
            output_file.write("Connected to Gmail successfully.\n")
            
            for num in recent_emails:
                try:
                    _, msg_data = self.mail.fetch(num, '(RFC822)')
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    # Get the email date
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
                            transaction = extract_venmo_data(html_content)
                            transaction['date'] = formatted_date
                            transactions.append(transaction)
                            
                            # Format the output
                            console_output, file_output = format_output({
                                'date': formatted_date,
                                'sender': transaction['actor'] if transaction['direction'] == 'incoming' else 'You',
                                'amount': transaction['amount'],
                                'note': transaction['note'],
                                'direction': transaction['direction']
                            })
                            
                            print(console_output)
                            output_file.write(file_output + "\n")
                            
                        except ValueError as e:
                            error_msg = f"Error processing email: {str(e)}"
                            print(error_msg)
                            output_file.write(error_msg + "\n")
                        except Exception as e:
                            error_msg = f"Unexpected error: {str(e)}"
                            print(error_msg)
                            output_file.write(error_msg + "\n")
                    else:
                        print("No HTML content found in the email.")
                        output_file.write("No HTML content found in the email.\n")
                        
                except Exception as e:
                    error_msg = f"Error processing email ID {num}: {str(e)}"
                    print(error_msg)
                    output_file.write(error_msg + "\n")

        return transactions

    def format_transaction(self, transaction: Dict) -> Dict:
        """Format transaction data for output"""
        return {
            'date': transaction.get('date', 'No date'),
            'sender': transaction['actor'] if transaction['direction'] == 'incoming' else 'You',
            'recipient': 'You' if transaction['direction'] == 'incoming' else transaction['actor'],
            'amount': transaction['amount'],
            'note': transaction['note'],
            'direction': transaction['direction']
        }

