#!/bin/bash

# URLs for the files in the GitHub repository
ASK_PY_URL="https://raw.githubusercontent.com/kmkamyk/ask-cli/main/ask.py"
CONFIG_YML_URL="https://raw.githubusercontent.com/kmkamyk/ask-cli/main/config.yml"

# Destination paths
ASK_PY_DEST="/usr/bin/ask"
CONFIG_YML_DEST="/etc/ask/config.yml"
ASK_CONFIG_DIR="/etc/ask"

# Function to install required packages
install_dependencies() {
    echo "Installing Python 3, pip, and Python dependencies..."

    # Detect the package manager and install Python and pip
    if command -v apt-get &>/dev/null; then
        # Debian-based systems
        echo "Detected Debian-based system. Installing packages..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
        
        # Install Python dependencies using pip
        echo "Installing Python dependencies..."
        sudo pip3 install openai pyyaml
    elif command -v yum &>/dev/null; then
        # RHEL-based systems
        echo "Detected RHEL-based system. Installing packages..."
        sudo yum install -y python3 python3-pip
        
        # Install Python dependencies using pip
        echo "Installing Python dependencies..."
        sudo pip3 install openai pyyaml
    else
        echo "Unsupported distribution. Please ensure the following packages are installed on your system:"
        echo "  - python3"
        echo "  - python3-pip"
        echo "  - Python libraries: openai, pyyaml"
        exit 1
    fi
}

# Installation function
install() {
    echo "Downloading ask.py and config.yml..."

    # Create /etc/ask directory if it doesn't exist
    if [ ! -d "$ASK_CONFIG_DIR" ]; then
        echo "Creating directory $ASK_CONFIG_DIR..."
        sudo mkdir -p $ASK_CONFIG_DIR
    fi

    # Download ask.py with sudo to the correct destination
    echo "Downloading ask.py..."
    sudo curl -sfL $ASK_PY_URL -o $ASK_PY_DEST
    if [ $? -ne 0 ]; then
        echo "Error downloading ask.py"
        exit 1
    fi

    # Download config.yml with sudo to the correct destination
    echo "Downloading config.yml..."
    sudo curl -sfL $CONFIG_YML_URL -o $CONFIG_YML_DEST
    if [ $? -ne 0 ]; then
        echo "Error downloading config.yml"
        exit 1
    fi

    # Set execute permissions for ask.py
    sudo chmod +x $ASK_PY_DEST

    echo "Installation complete!"
}
# Uninstallation function
uninstall() {
    echo "Uninstalling Ask CLI..."

    # Remove ask.py
    sudo rm -f $ASK_PY_DEST

    # Remove config.yml
    sudo rm -f $CONFIG_YML_DEST

    # Remove /etc/ask directory if it's empty
    if [ -d "$ASK_CONFIG_DIR" ]; then
        sudo rmdir $ASK_CONFIG_DIR
    fi

    echo "Uninstallation complete!"
}

# Check for arguments and call the appropriate function
if [ "$1" == "uninstall" ]; then
    uninstall
else
    install_dependencies
    install
fi
