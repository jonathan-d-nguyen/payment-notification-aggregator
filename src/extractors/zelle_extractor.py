from bs4 import BeautifulSoup
import re
from typing import Dict

def extract_zelle_data(html_content: str) -> Dict:
    """Extract Zelle transaction data from email HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = ' '.join([text for text in soup.stripped_strings])
    
    # Extract amount and sender
    pattern = r"deposited the \$(\d+\.\d{2}) payment from ([^(]+)"
    match = re.search(pattern, text_content)
    
    if not match:
        raise ValueError("No Zelle transfer information found in this email")
    
    amount = match.group(1)
    sender = match.group(2).strip()
    
    # Extract confirmation number
    conf_pattern = r"confirmation number (\d+)"
    conf_match = re.search(conf_pattern, text_content)
    confirmation = conf_match.group(1) if conf_match else "No confirmation number found"
    
    # Extract account info
    account_pattern = r"into your account \((.*?)\)"
    account_match = re.search(account_pattern, text_content)
    account_info = account_match.group(1) if account_match else "Account info not found"
    
    return {
        'sender': sender,
        'amount': f"${amount}",
        'confirmation': confirmation,
        'account': account_info,
        'direction': 'incoming'
    }

