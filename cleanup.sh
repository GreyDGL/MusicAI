#!/bin/bash

# MusicAI Cleanup Script - Prepares folder for distribution
# Removes models, temp files, and generated content

echo "========================================="
echo "     MusicAI Project Cleanup Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Stop any running Flask instances
echo -e "${YELLOW}Stopping any running instances...${NC}"
pkill -f "python app.py" 2>/dev/null

# Remove virtual environment
if [ -d ".venv" ]; then
    echo -e "${YELLOW}Removing virtual environment...${NC}"
    rm -rf .venv
    echo -e "${GREEN}✓ Virtual environment removed${NC}"
fi

# Remove Python cache files
echo -e "${YELLOW}Removing Python cache files...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null
find . -type f -name "*.pyd" -delete 2>/dev/null
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
echo -e "${GREEN}✓ Python cache cleaned${NC}"

# Remove database (but keep instance folder)
if [ -f "instance/database.db" ]; then
    echo -e "${YELLOW}Removing database...${NC}"
    rm -f instance/database.db
    echo -e "${GREEN}✓ Database removed${NC}"
fi

# Remove generated music files (but keep the music folder)
if [ -d "music" ]; then
    echo -e "${YELLOW}Removing generated music files...${NC}"
    rm -f music/*.wav 2>/dev/null
    rm -f music/*.mp3 2>/dev/null
    rm -f music/*.flac 2>/dev/null
    rm -f music/*.m4a 2>/dev/null
    echo -e "${GREEN}✓ Music files removed${NC}"
fi

# Remove Jupyter notebook checkpoints
if [ -d ".ipynb_checkpoints" ]; then
    echo -e "${YELLOW}Removing Jupyter checkpoints...${NC}"
    rm -rf .ipynb_checkpoints
    echo -e "${GREEN}✓ Jupyter checkpoints removed${NC}"
fi

# Remove logs if they exist
if [ -d "logs" ]; then
    echo -e "${YELLOW}Removing log files...${NC}"
    rm -rf logs
    echo -e "${GREEN}✓ Logs removed${NC}"
fi

# Remove any .DS_Store files (macOS)
find . -name ".DS_Store" -delete 2>/dev/null

# Remove IDE files (optional - comment out if you want to keep them)
echo -e "${YELLOW}Removing IDE configuration files...${NC}"
rm -rf .idea 2>/dev/null
rm -rf .vscode 2>/dev/null
rm -rf .claude 2>/dev/null
echo -e "${GREEN}✓ IDE files removed${NC}"

# Remove the large Jupyter notebook (optional - it's 2.2MB)
if [ -f "Working_Version_MusicGen.ipynb" ]; then
    echo -e "${YELLOW}Removing large Jupyter notebook...${NC}"
    rm -f Working_Version_MusicGen.ipynb
    echo -e "${GREEN}✓ Jupyter notebook removed${NC}"
fi

# Remove start/stop scripts created by installer (will be recreated on install)
if [ -f "start.sh" ]; then
    rm -f start.sh
    echo -e "${GREEN}✓ start.sh removed${NC}"
fi

if [ -f "stop.sh" ]; then
    rm -f stop.sh
    echo -e "${GREEN}✓ stop.sh removed${NC}"
fi

# Remove any model cache (in case models were downloaded to project directory)
rm -rf models_cache 2>/dev/null
rm -rf .cache 2>/dev/null

# Display folder size after cleanup
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}          Cleanup Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# Show final folder size
FOLDER_SIZE=$(du -sh . | cut -f1)
echo -e "Folder size after cleanup: ${GREEN}${FOLDER_SIZE}${NC}"
echo ""

# Count remaining files
FILE_COUNT=$(find . -type f ! -path "./.git/*" | wc -l | tr -d ' ')
echo -e "Total files remaining: ${GREEN}${FILE_COUNT}${NC}"
echo ""

echo "The project is now ready to be zipped and shared!"
echo ""
echo "To create a zip file, run:"
echo -e "${YELLOW}cd .. && zip -r musicAI-clean.zip musicAI/${NC}"
echo ""
echo "Your friend can then run './install.sh' after extracting."