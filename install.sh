#!/bin/bash

# MusicGen AI Installation Script
# Supports macOS, Linux, and Windows (via WSL/Git Bash)
# Version 1.0

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_info "Detected macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        print_info "Detected Linux"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="windows"
        print_info "Detected Windows"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
check_python() {
    print_info "Checking Python installation..."

    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8 or higher."

        if [[ "$OS" == "macos" ]]; then
            print_info "Install Python using Homebrew: brew install python3"
        elif [[ "$OS" == "linux" ]]; then
            print_info "Install Python using: sudo apt-get install python3 python3-pip (Ubuntu/Debian)"
            print_info "Or: sudo yum install python3 python3-pip (CentOS/RHEL)"
        elif [[ "$OS" == "windows" ]]; then
            print_info "Download Python from: https://www.python.org/downloads/"
        fi
        exit 1
    fi

    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
        print_error "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi

    print_success "Python $PYTHON_VERSION found"
}

# Check pip
check_pip() {
    print_info "Checking pip installation..."

    if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
        print_warning "pip not found. Installing pip..."
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        $PYTHON_CMD get-pip.py
        rm get-pip.py
    fi

    print_success "pip is installed"
}

# Check system dependencies
check_dependencies() {
    print_info "Checking system dependencies..."

    # Check for ffmpeg (required for audio processing)
    if ! command_exists ffmpeg; then
        print_warning "ffmpeg not found. Installing ffmpeg..."

        if [[ "$OS" == "macos" ]]; then
            if command_exists brew; then
                brew install ffmpeg
            else
                print_error "Homebrew not found. Please install Homebrew first: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                exit 1
            fi
        elif [[ "$OS" == "linux" ]]; then
            if command_exists apt-get; then
                sudo apt-get update && sudo apt-get install -y ffmpeg
            elif command_exists yum; then
                sudo yum install -y ffmpeg
            else
                print_warning "Please install ffmpeg manually for your Linux distribution"
            fi
        elif [[ "$OS" == "windows" ]]; then
            print_warning "Please download and install ffmpeg from: https://ffmpeg.org/download.html"
            print_warning "Add ffmpeg to your PATH environment variable"
        fi
    else
        print_success "ffmpeg is installed"
    fi

    # Check for git (optional but recommended)
    if ! command_exists git; then
        print_warning "git not found. Git is recommended for version control."
    else
        print_success "git is installed"
    fi
}

# Create virtual environment
create_venv() {
    print_info "Creating Python virtual environment..."

    if [ -d ".venv" ]; then
        print_warning "Virtual environment already exists. Removing old environment..."
        rm -rf .venv
    fi

    $PYTHON_CMD -m venv .venv

    # Activate virtual environment
    if [[ "$OS" == "windows" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi

    print_success "Virtual environment created and activated"
}

# Upgrade pip and install wheel
upgrade_pip() {
    print_info "Upgrading pip and installing wheel..."
    pip install --upgrade pip wheel setuptools
    print_success "pip, wheel, and setuptools upgraded"
}

# Install PyTorch with appropriate backend
install_pytorch() {
    print_info "Installing PyTorch..."

    if [[ "$OS" == "macos" ]]; then
        # Check if Apple Silicon
        if [[ $(uname -m) == "arm64" ]]; then
            print_info "Detected Apple Silicon Mac. Installing PyTorch with MPS support..."
            pip install torch==2.4.1 torchaudio==2.4.1
        else
            print_info "Detected Intel Mac. Installing PyTorch for CPU..."
            pip install torch==2.4.1 torchaudio==2.4.1
        fi
    elif [[ "$OS" == "linux" ]]; then
        # Check for NVIDIA GPU
        if command_exists nvidia-smi; then
            print_info "NVIDIA GPU detected. Installing PyTorch with CUDA support..."
            pip install torch==2.4.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121
        else
            print_info "No NVIDIA GPU detected. Installing PyTorch for CPU..."
            pip install torch==2.4.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cpu
        fi
    else
        print_info "Installing PyTorch for CPU..."
        pip install torch==2.4.1 torchaudio==2.4.1
    fi

    print_success "PyTorch installed successfully"
}

# Install Python dependencies
install_dependencies() {
    print_info "Installing Python dependencies..."

    # Install main requirements
    print_info "Installing Flask and core dependencies..."
    pip install -r requirements.txt

    # Install MusicGen requirements (excluding torch as we already installed it)
    print_info "Installing MusicGen dependencies..."
    pip install transformers==4.44.2
    pip install scipy==1.14.0
    pip install accelerate==0.33.0

    # Install xformers if supported (skip on Windows and older systems)
    if [[ "$OS" != "windows" ]]; then
        print_info "Attempting to install xformers for performance optimization..."
        pip install xformers==0.0.27.post2 || print_warning "xformers installation failed. Continuing without it (optional optimization)."
    fi

    # Install datasets with audio support
    pip install datasets[audio]

    print_success "All Python dependencies installed"
}

# Initialize database
init_database() {
    print_info "Initializing database..."

    $PYTHON_CMD -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully')
"

    print_success "Database initialized"
}

# Create necessary directories
create_directories() {
    print_info "Creating necessary directories..."

    mkdir -p music
    mkdir -p instance
    mkdir -p logs

    print_success "Directories created"
}

# Test installation
test_installation() {
    print_info "Testing installation..."

    # Test imports
    $PYTHON_CMD -c "
import torch
import torchaudio
import transformers
import flask
import librosa
import numpy
print('All imports successful!')

# Check PyTorch device
if torch.cuda.is_available():
    print(f'CUDA available: {torch.cuda.get_device_name(0)}')
elif torch.backends.mps.is_available():
    print('MPS (Metal Performance Shaders) available for Apple Silicon')
else:
    print('Using CPU for computation')
" || {
    print_error "Installation test failed. Some modules could not be imported."
    exit 1
}

    print_success "Installation test passed"
}

# Create start script
create_start_script() {
    print_info "Creating start script..."

    cat > start.sh << 'EOF'
#!/bin/bash

# MusicGen AI Start Script

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Starting MusicGen AI Application...${NC}"

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    echo "Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Start the application
echo -e "${GREEN}Starting Flask application on http://localhost:8080${NC}"
python app.py
EOF

    chmod +x start.sh
    print_success "Start script created (./start.sh)"
}

# Create stop script
create_stop_script() {
    print_info "Creating stop script..."

    cat > stop.sh << 'EOF'
#!/bin/bash

# MusicGen AI Stop Script

echo "Stopping MusicGen AI Application..."

# Find and kill the Flask process
if pgrep -f "python app.py" > /dev/null; then
    pkill -f "python app.py"
    echo "Application stopped successfully"
else
    echo "Application is not running"
fi
EOF

    chmod +x stop.sh
    print_success "Stop script created (./stop.sh)"
}

# Main installation flow
main() {
    echo ""
    echo "========================================="
    echo "    MusicGen AI Installation Script"
    echo "========================================="
    echo ""

    # Check if we're in the right directory
    if [ ! -f "app.py" ]; then
        print_error "app.py not found. Please run this script from the MusicGen project directory."
        exit 1
    fi

    detect_os
    check_python
    check_pip
    check_dependencies
    create_venv
    upgrade_pip
    install_pytorch
    install_dependencies
    create_directories
    init_database
    test_installation
    create_start_script
    create_stop_script

    echo ""
    echo "========================================="
    echo -e "${GREEN}    Installation Complete!${NC}"
    echo "========================================="
    echo ""
    print_info "To start the application, run:"
    echo "    ./start.sh"
    echo ""
    print_info "To stop the application, run:"
    echo "    ./stop.sh"
    echo ""
    print_info "Access the application at:"
    echo "    http://localhost:8080"
    echo ""
    print_warning "First music generation will download the model (~2GB)"
    echo ""
}

# Run main function
main