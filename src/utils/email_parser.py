# src/utils/email_parser.py
"""
Utility function for parsing raw email content received from Amazon SES.
Takes a raw email string and extracts key components into a structured dictionary.

Returns a dictionary containing:
- from: Sender's email address
- subject: Email subject line
- date: Email timestamp
- html_content: Decoded HTML body of the email

Raises ValueError if no HTML content is found in the email.
Used primarily for processing payment notification emails before
passing to specific payment extractors.
"""

import email
from typing import Dict, Optional

def parse_ses_email(email_content: str) -> Dict:
    """
    Parse email content from SES into a structured format
    """
    msg = email.message_from_string(email_content)
    
    # Extract HTML content
    html_content = None
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            html_content = part.get_payload(decode=True).decode()
            break
    
    if not html_content:
        raise ValueError("No HTML content found in email")
        
    return {
        'from': msg['from'],
        'subject': msg['subject'],
        'date': msg['date'],
        'html_content': html_content
    }