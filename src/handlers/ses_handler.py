# src/handlers/ses_handler.py
"""
AWS Lambda handler for processing payment notification emails received through SES.
Identifies and processes emails from Venmo and Navy Federal (Zelle) to extract
payment transaction details. 

The handler:
- Receives SES email events
- Identifies the payment provider (Venmo or Zelle) from the email source
- Routes to appropriate extractor to parse transaction details
- Returns a standardized response containing:
  - messageId: Unique SES message identifier
  - timestamp: When the email was received
  - provider: 'venmo' or 'zelle'
  - status: 'processed' or 'error'
  - data: Extracted transaction details or error message

Designed to work with AWS SES email receiving rules to automatically process
payment notifications.
"""

import json
import email
from typing import Dict, Any
from ..extractors.venmo_extractor import extract_venmo_data
from ..extractors.zelle_extractor import extract_zelle_data

def process_ses_email(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process incoming emails from SES
    Returns processed payment data or error information
    """
    # Get the message content from the SES event
    ses_notification = event['Records'][0]['ses']
    message = ses_notification['mail']
    
    try:
        # Parse email content
        email_content = message.get('content', '')
        
        # Determine email type and extract data
        if 'venmo@venmo.com' in message.get('source', '').lower():
            transaction_data = extract_venmo_data(email_content)
            provider = 'venmo'
        elif 'noreply@mail.navyfederal.org' in message.get('source', '').lower():
            transaction_data = extract_zelle_data(email_content)
            provider = 'zelle'
        else:
            raise ValueError("Unsupported email source")

        # Add metadata
        result = {
            'messageId': message['messageId'],
            'timestamp': message['timestamp'],
            'provider': provider,
            'status': 'processed',
            'data': transaction_data
        }
        
        return result
    
    except Exception as e:
        return {
            'messageId': message['messageId'],
            'timestamp': message['timestamp'],
            'status': 'error',
            'error': str(e)
        }