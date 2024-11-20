# main.py
import os
from dotenv import load_dotenv
from src.processors.zelle_processor import ZelleProcessor
from src.processors.venmo_processor import VenmoProcessor

def main():
    # Load environment variables
    load_dotenv()
    username = os.environ.get('GMAIL_USERNAME')
    password = os.environ.get('GMAIL_PASSWORD')

    if not username or not password:
        print("Error: Gmail credentials not found in environment variables.")
        return

    # # Process Zelle transactions
    try:
        print("\nProcessing Zelle transactions...")
        zelle_processor = ZelleProcessor(
            username=username, 
            password=password,
            output_file="output/zelle_transactions.txt"
        )
        zelle_processor.connect()
        zelle_transactions = zelle_processor.process_emails()
        print(f"Processed {len(zelle_transactions)} Zelle transactions")
        print("Output has been written to output/zelle_transactions.txt")
    except Exception as e:
        print(f"Error processing Zelle transactions: {str(e)}")
    finally:
        zelle_processor.disconnect()

    # Process Venmo transactions
    # try:
    #     print("\nProcessing Venmo transactions...")
    #     venmo_processor = VenmoProcessor(
    #         username=username, 
    #         password=password,
    #         output_file="output/venmo_transactions.txt"
    #     )
    #     venmo_processor.connect()
    #     venmo_transactions = venmo_processor.process_emails()
    #     print(f"Processed {len(venmo_transactions)} Venmo transactions")
    #     print("Output has been written to output/venmo_transactions.txt")
    # except Exception as e:
    #     print(f"Error processing Venmo transactions: {str(e)}")
    # finally:
    #     venmo_processor.disconnect()

if __name__ == "__main__":
    main()

