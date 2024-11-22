#!/usr/bin/env python3
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Set

class AWSSecurityScanner:
    def __init__(self):
        # AWS Account ID pattern (12 digits)
        self.aws_account_pattern = r'\d{12}'
        
        # AWS ARN patterns
        self.arn_patterns = [
            r'arn:aws:[a-zA-Z0-9\-]*:[a-zA-Z0-9\-]*:\d{12}:',  # Basic ARN pattern
            r'arn:aws:iam::\d{12}:role/[a-zA-Z0-9\-_/]+',      # IAM Role ARN
            r'arn:aws:ecr:[a-zA-Z0-9\-]*:\d{12}:repository',   # ECR Repository ARN
        ]
        
        # ECR repository patterns
        self.ecr_patterns = [
            r'\d{12}\.dkr\.ecr\.[a-zA-Z0-9\-]+\.amazonaws\.com',  # ECR URL
            r'ecr/[a-zA-Z0-9\-_/]+',                              # ECR path
        ]
        
        # Files to exclude
        self.exclude_dirs = {'.git', 'node_modules', 'venv', '.env', '.venv', '__pycache__'}
        self.exclude_files = {'.pyc', '.pyo', '.pyd', '.git'}
        
        # Initialize results
        self.findings: Dict[str, Set[str]] = {
            'aws_accounts': set(),
            'arns': set(),
            'ecr_repos': set()
        }
        
    def should_scan_file(self, file_path: str) -> bool:
        """Determine if a file should be scanned based on extension and path."""
        path = Path(file_path)
        
        # Check if file is in excluded directory
        if any(excluded in path.parts for excluded in self.exclude_dirs):
            return False
            
        # Check if file has excluded extension
        if path.suffix in self.exclude_files:
            return False
            
        return True
    
    def scan_file(self, file_path: str) -> None:
        """Scan a single file for AWS identifiers."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Scan for AWS Account IDs
                account_matches = re.finditer(self.aws_account_pattern, content)
                for match in account_matches:
                    # Verify it's exactly 12 digits
                    if len(match.group()) == 12:
                        self.findings['aws_accounts'].add((match.group(), file_path))
                
                # Scan for ARNs
                for pattern in self.arn_patterns:
                    arn_matches = re.finditer(pattern, content)
                    for match in arn_matches:
                        self.findings['arns'].add((match.group(), file_path))
                
                # Scan for ECR repositories
                for pattern in self.ecr_patterns:
                    ecr_matches = re.finditer(pattern, content)
                    for match in ecr_matches:
                        self.findings['ecr_repos'].add((match.group(), file_path))
                        
        except UnicodeDecodeError:
            # Skip binary files
            pass
        except Exception as e:
            print(f"Error scanning {file_path}: {str(e)}")
    
    def scan_directory(self, directory: str) -> None:
        """Recursively scan a directory for AWS identifiers."""
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if self.should_scan_file(file_path):
                    self.scan_file(file_path)
    
    def print_findings(self) -> None:
        """Print scanning results in a formatted way."""
        print("\n🔍 AWS Resource Exposure Scan Results")
        print("=====================================")
        
        if not any(self.findings.values()):
            print("✅ No exposed AWS resources found!")
            return
            
        if self.findings['aws_accounts']:
            print("\n⚠️  Exposed AWS Account IDs:")
            print("----------------------------")
            for account, file_path in sorted(self.findings['aws_accounts']):
                print(f"Account: {account}")
                print(f"File: {file_path}\n")
                
        if self.findings['arns']:
            print("\n⚠️  Exposed ARNs:")
            print("----------------")
            for arn, file_path in sorted(self.findings['arns']):
                print(f"ARN: {arn}")
                print(f"File: {file_path}\n")
                
        if self.findings['ecr_repos']:
            print("\n⚠️  Exposed ECR Repositories:")
            print("--------------------------")
            for repo, file_path in sorted(self.findings['ecr_repos']):
                print(f"Repository: {repo}")
                print(f"File: {file_path}\n")
        
        print("\n🔒 Remediation Recommendations:")
        print("-----------------------------")
        print("1. Remove hardcoded AWS Account IDs and ARNs")
        print("2. Use environment variables or AWS Parameter Store")
        print("3. Consider using dynamic ARN construction")
        print("4. Implement infrastructure as code with proper variable management")
        print("5. Review CI/CD pipeline configurations for exposures")

def main():
    if len(sys.argv) != 2:
        print("Usage: python aws_security_scanner.py <directory>")
        sys.exit(1)
        
    directory = sys.argv[1]
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)
        
    scanner = AWSSecurityScanner()
    scanner.scan_directory(directory)
    scanner.print_findings()

if __name__ == "__main__":
    main()
