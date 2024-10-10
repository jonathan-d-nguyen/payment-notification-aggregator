import imaplib
import email
import os
from email.header import decode_header
from bs4 import BeautifulSoup, Comment
from datetime import datetime, timedelta
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

def extract_venmo_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    actor_name = soup.find(string=lambda text: isinstance(text, Comment) and 'actor name' in text).next_sibling.strip()
    amount = soup.find(string=lambda text: isinstance(text, Comment) and 'amount' in text).next_sibling.strip()
    note = soup.find(string=lambda text: isinstance(text, Comment) and 'note' in text).next_sibling.strip()
    
    return actor_name, amount, note

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
