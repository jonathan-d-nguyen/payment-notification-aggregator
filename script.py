import imaplib
import email
import os
import re
from email.header import decode_header
from bs4 import BeautifulSoup, Comment
from datetime import datetime, timedelta
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

def extract_venmo_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for payment information with case-insensitive pattern
    payment_pattern = re.compile(r'(paid you|You paid)', re.IGNORECASE)
    payment_element = soup.find(['p', 'div', 'span'], string=payment_pattern)
    
    if not payment_element:
        raise ValueError("No payment information found in this email")
    
    payment_text = payment_element.get_text().strip()
    
    # Find the amount using regex
    amount_pattern = r'\$\d+(?:,\d{3})*(?:\.\d{2})?'
    amount_match = re.search(amount_pattern, html_content)
    if not amount_match:
        raise ValueError("No payment amount found")
    amount = amount_match.group(0)
    
    # Determine payment direction and actor
    if re.search(r'paid you', payment_text, re.IGNORECASE):
        # Someone paid you
        actor_name = payment_text.split('paid')[0].strip()
        direction = "incoming"
    elif re.search(r'You paid', payment_text, re.IGNORECASE):
        # You paid someone
        actor_name = payment_text.split('paid')[1].strip()
        direction = "outgoing"
    else:
        raise ValueError("Could not determine payment direction")
    
    # Try to find note
    note = "No note provided"
    note_element = soup.find(['p', 'div', 'span'], string=re.compile(r'Note:', re.IGNORECASE))
    if note_element:
        note = note_element.get_text().strip()
        note = note.replace('Note:', '').strip()
    
    return {
        'actor': actor_name,
        'amount': amount,
        'note': note,
        'direction': direction
    }

def process_venmo_emails():
    # Get credentials from environment variables
    username = os.environ.get('GMAIL_USERNAME')
    password = os.environ.get('GMAIL_PASSWORD')

    if not username or not password:
        print("Error: Gmail credentials not found in environment variables.")
        return

    # Open the output file
    with open("output.txt", "w") as output_file:
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(username, password)
            mail.select('inbox')
            print("Connected to Gmail successfully.")
            output_file.write("Connected to Gmail successfully.\n")

            # Calculate the date 3 days ago
            date_since = (datetime.now() - timedelta(days=3)).strftime("%d-%b-%Y")

            # Search for Venmo emails from the last 3 days
            _, message_numbers = mail.search(None, f'(FROM "venmo@venmo.com" SINCE "{date_since}")')

            for num in message_numbers[0].split():
                _, msg_data = mail.fetch(num, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)

                subject = decode_header(email_message["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()

                print(f"Processing email: {subject}")
                output_file.write(f"Processing email: {subject}\n")

                # Get the HTML content of the email
                html_content = ""
                for part in email_message.walk():
                    if part.get_content_type() == "text/html":
                        html_content = part.get_payload(decode=True).decode()
                        break

                if html_content:
                    try:
                        actor_name, amount, note = extract_venmo_data(html_content)
                        print(f"Actor Name: {actor_name}")
                        print(f"Amount: {amount}")
                        print(f"Note: {note}")
                        print("---")
                        output_file.write(f"Actor Name: {actor_name}\n")
                        output_file.write(f"Amount: {amount}\n")
                        output_file.write(f"Note: {note}\n")
                        output_file.write("---\n")
                    except Exception as e:
                        print(f"Error processing email: {str(e)}")
                        output_file.write(f"Error processing email: {str(e)}\n")
                else:
                    print("No HTML content found in the email.")
                    output_file.write("No HTML content found in the email.\n")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            output_file.write(f"An error occurred: {str(e)}\n")
        finally:
            try:
                mail.close()
            except:
                pass
            mail.logout()

    print(f"\nOutput has been written to output.txt")

if __name__ == "__main__":
    process_venmo_emails()
