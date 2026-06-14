#!/bin/bash
set -e

# Define project root
PROJECT_ROOT="/home/prata/leads"

echo "=== Lead Pipeline End-to-End Run ==="
echo "Date: $(date)"

# Navigate to project directory and activate virtual environment
cd "$PROJECT_ROOT"
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Warning: .venv directory not found!"
fi

# 1. Scrape fresh leads
echo "Step 1: Scraping fresh leads..."
python scripts/daily_run.py

# 2 & 3. Build demo sites and send WhatsApp messages
echo "Step 2 & 3: Building demo sites and sending WhatsApp messages..."
python scripts/build_and_send.py

echo "=== Pipeline Completed Successfully ==="
