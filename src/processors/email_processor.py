# src/processors/email_processor.py
"""
Abstract base class for processing payment notification emails from Gmail accounts.
Provides common email connection handling and defines the interface for email
processing implementations.

Features:
- Secure IMAP connection management for Gmail
- Abstract methods for email searching and processing
- Automatic connection cleanup

Child classes must implement:
- search_emails(): Define search criteria for specific payment providers
- process_emails(): Extract and structure payment data from matching emails

Usage:
Extend this class to create specific email processors for different payment
providers (e.g., Venmo, Zelle) while maintaining consistent connection handling
and interface structure.
"""

from abc import ABC, abstractmethod
import imaplib
import email
from typing import List, Dict

class EmailProcessor(ABC):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.mail = None

    def connect(self):
        """Establish connection to Gmail"""
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.username, self.password)
        self.mail.select('inbox')

    def disconnect(self):
        """Close Gmail connection"""
        try:
            self.mail.close()
            self.mail.logout()
        except:
            pass

    @abstractmethod
    def search_emails(self) -> List[str]:
        """Search for relevant emails"""
        pass

    @abstractmethod
    def process_emails(self) -> List[Dict]:
        """Process emails and extract data"""
        pass

