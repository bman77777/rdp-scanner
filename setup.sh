#!/bin/bash

# RDP Scanner Setup Script

echo "Setting up RDP Scanner..."

# Check if required tools are installed
echo "Checking for required tools..."
if ! command -v masscan &> /dev/null; then
    echo "masscan could not be found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y masscan
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install masscan
    fi
fi

if ! command -v nmap &> /dev/null; then
    echo "nmap could not be found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y nmap
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install nmap
    fi
fi

if ! command -v msfconsole &> /dev/null; then
    echo "Metasploit could not be found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Install Metasploit on Linux
        sudo apt install -y curl
        curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/configs/msfupdate.erb -o msfinstall
        chmod 755 msfinstall
        ./msfinstall
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Install Metasploit on macOS
        brew install metasploit-framework
    fi
fi

# Install Python requirements
echo "Installing Python requirements..."
pip3 install -r requirements.txt

echo "Setup complete!"
echo "Usage: python3 rdp_scanner.py [target_ranges]"
echo "Example: python3 rdp_scanner.py 0.0.0.0/0"