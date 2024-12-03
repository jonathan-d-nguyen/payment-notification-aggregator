# src/extractors/venmo_extractor.py
"""
Parses Venmo payment notification emails to extract transaction details.
Takes HTML content from a Venmo email notification and returns a dictionary containing:
- actor: The person who sent/received the payment
- amount: The payment amount
- note: The payment memo/note (if provided)
- direction: Whether the payment was incoming or outgoing
"""

from bs4 import BeautifulSoup
import re
from typing import Dict

def extract_venmo_data(html_content: str) -> Dict:
    """Extract Venmo transaction data from email HTML content"""
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
    
    # Initialize actor variable
    actor = None
    
    # Determine payment direction and actor
    if re.search(r'paid you', payment_text, re.IGNORECASE):
        direction = "incoming"
        # Extract the person who paid you (comes before "paid you")
        actor_match = re.search(r'(.*?)\s+paid you', payment_text, re.IGNORECASE)
        if actor_match:
            actor = actor_match.group(1).strip()
        else:
            actor = "Unknown sender"
    elif re.search(r'You paid', payment_text, re.IGNORECASE):
        direction = "outgoing"
        # Extract who you paid (comes after "You paid")
        actor_match = re.search(r'You paid\s+(.*?)(?:\s+|$)', payment_text, re.IGNORECASE)
        if actor_match:
            actor = actor_match.group(1).strip()
        else:
            actor = "Unknown recipient"
    else:
        raise ValueError("Could not determine payment direction")
    
    # Try to find note/memo
    note = "No note provided"
    note_patterns = [
        r'for "(.*?)"',
        r'note: "(.*?)"',
        r'memo: "(.*?)"'
    ]
    
    for pattern in note_patterns:
        note_match = re.search(pattern, html_content, re.IGNORECASE)
        if note_match:
            note = note_match.group(1).strip()
            break
    
    return {
        'actor': actor,
        'amount': amount,
        'note': note,
        'direction': direction
    }

