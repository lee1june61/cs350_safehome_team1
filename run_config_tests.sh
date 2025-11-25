#!/bin/bash
# SafeHome Configuration Module Test Runner
# This script activates the virtual environment and runs configuration tests

set -e  # Exit on error

echo "🏠 SafeHome Configuration Module Test Runner"
echo "============================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
    echo ""
    echo "Installing dependencies..."
    source .venv/bin/activate
    pip install pytest pytest-cov pytest-mock
    echo "✅ Dependencies installed"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Set PYTHONPATH to include project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run tests
echo "🧪 Running configuration module tests..."
echo ""

python -m pytest tests/test_configuration_module.py -v \
    --cov=src/configuration \
    --cov-report=term-missing:skip-covered \
    --cov-report=html

echo ""
echo "============================================="
echo "✅ Tests completed!"
echo ""
echo "📊 Coverage report saved to: htmlcov/index.html"
echo "   Open with: open htmlcov/index.html"
echo ""

