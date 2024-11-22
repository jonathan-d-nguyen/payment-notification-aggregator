#!/bin/bash

echo "🔒 Starting Repository Security Scan..."
echo "=====================================\n"

# Function to check for sensitive files
check_sensitive_files() {
    echo "📁 Checking for sensitive files..."
    sensitive_files=(
        ".env"
        "*.pem"
        "*.key"
        "*id_rsa*"
        "*.pfx"
        "*.p12"
        "*.pkcs12"
        "*password*"
        "*credential*"
        "*.keystore"
        "*.jks"
    )
    
    found_sensitive=false
    for pattern in "${sensitive_files[@]}"; do
        files=$(find . -name "$pattern" -not -path "./.git/*" 2>/dev/null)
        if [ ! -z "$files" ]; then
            echo "⚠️  WARNING: Potentially sensitive file(s) found matching pattern '$pattern':"
            echo "$files"
            found_sensitive=true
        fi
    done
    
    if [ "$found_sensitive" = false ]; then
        echo "✅ No common sensitive files found"
    fi
    echo
}

# Function to check for sensitive data in commits
check_sensitive_commits() {
    echo "📜 Checking git history for sensitive data..."
    sensitive_patterns=(
        "password="
        "api_key"
        "secret"
        "token"
        "aws_access"
        "private_key"
    )
    
    found_sensitive=false
    for pattern in "${sensitive_patterns[@]}"; do
        matches=$(git log -p | grep -i "$pattern" | grep -v "secret.*=.*\${.*}" | grep -v "password.*=.*\${.*}")
        if [ ! -z "$matches" ]; then
            echo "⚠️  WARNING: Potentially sensitive data found in git history matching '$pattern'"
            echo "    Run 'git log -p | grep -i \"$pattern\"' for details"
            found_sensitive=true
        fi
    done
    
    if [ "$found_sensitive" = false ]; then
        echo "✅ No obvious sensitive data found in commit history"
    fi
    echo
}

# Function to check for unsafe file permissions
check_file_permissions() {
    echo "🔐 Checking file permissions..."
    world_writable=$(find . -type f -perm -002 -not -path "./.git/*" 2>/dev/null)
    if [ ! -z "$world_writable" ]; then
        echo "⚠️  WARNING: World-writable files found:"
        echo "$world_writable"
    else
        echo "✅ No world-writable files found"
    fi
    echo
}

# Function to check for large files
check_large_files() {
    echo "📦 Checking for large files (>10MB)..."
    large_files=$(find . -type f -size +10M -not -path "./.git/*" 2>/dev/null)
    if [ ! -z "$large_files" ]; then
        echo "⚠️  WARNING: Large files found:"
        echo "$large_files"
    else
        echo "✅ No large files found"
    fi
    echo
}

# Run all checks
check_sensitive_files
check_sensitive_commits
check_file_permissions
check_large_files

echo "🏁 Security scan complete!"

