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

