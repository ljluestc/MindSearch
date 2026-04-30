#!/bin/bash
# Test script for TencentSearch version check fix (Issue #288)

set -e

echo "========================================="
echo "Testing TencentSearch Version Check Fix"
echo "========================================="
echo ""

# Test 1: Old version should fail with clear message
echo "Test 1: Testing with old lagent version (should fail gracefully)"
echo "-------------------------------------------------------------------"
pip install lagent==0.2.4 --quiet
echo "Installed lagent version: $(pip show lagent | grep Version)"
echo ""

echo "Attempting to start MindSearch with TencentSearch..."
python -m mindsearch.app --lang cn --model_format internlm_silicon --search_engine TencentSearch 2>&1 | head -20 || true

echo ""
echo "✓ If you saw 'RuntimeError: TencentSearch requires lagent >= 0.5.0rc2', the fix works!"
echo ""

# Test 2: Correct version should work
echo "========================================="
echo "Test 2: Testing with correct lagent version"
echo "-------------------------------------------------------------------"
pip install lagent==0.5.0rc2 --quiet
echo "Installed lagent version: $(pip show lagent | grep Version)"
echo ""

echo "Checking if TencentSearch is available in lagent..."
python -c "from lagent.actions.bing_browser import TencentSearch; print('✓ TencentSearch class found!')" 2>&1 || echo "✗ TencentSearch not found"

echo ""
echo "Test 3: Testing other search engines (should work with any version)"
echo "-------------------------------------------------------------------"
echo "Testing with DuckDuckGo (should work regardless of lagent version)..."
python -c "
import sys
sys.path.insert(0, '.')
from mindsearch.agent import init_agent
try:
    agent = init_agent(lang='cn', model_format='internlm_silicon', search_engine='DuckDuckGoSearch')
    print('✓ DuckDuckGoSearch initialized successfully')
except Exception as e:
    print(f'✗ Error: {e}')
" 2>&1 || true

echo ""
echo "========================================="
echo "Testing Complete!"
echo "========================================="
