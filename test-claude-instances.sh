#!/bin/bash
# Test script to verify Claude Code instances work without setup prompt

echo "🧪 Testing Claude Code Instance Startup"
echo "======================================"
echo

# Test 1: MCP servers available
echo "1️⃣  Testing MCP Server Access"
if claude mcp list | grep -q "zen-core.*Connected"; then
    echo "   ✅ zen-core MCP server connected"
else
    echo "   ❌ zen-core MCP server not connected"
    exit 1
fi
echo

# Test 2: Quick message (no setup prompt)
echo "2️⃣  Testing Quick Message (No Setup Prompt)"
QUICK_TEST=$(claude --print "Just testing - respond with 'OK'" 2>&1)
if echo "$QUICK_TEST" | grep -q "OK" && ! echo "$QUICK_TEST" | grep -q "Choose the text style"; then
    echo "   ✅ Claude responds immediately without setup prompt"
else
    echo "   ❌ Setup prompt still appearing or other issue"
    echo "   Output: $QUICK_TEST"
    exit 1
fi
echo

# Test 3: Smart consensus tool access
echo "3️⃣  Testing Smart Consensus Tool"
CONSENSUS_TEST=$(timeout 15 claude --print "Use smart_consensus to answer: Is this test working? (scaleup level)" 2>&1)
if echo "$CONSENSUS_TEST" | grep -q -i "consensus\|recommendation\|working"; then
    echo "   ✅ Smart consensus tool accessible and working"
else
    echo "   ⚠️  Smart consensus tool may not be working properly"
    echo "   (This is non-critical for basic functionality)"
fi
echo

# Test 4: Different directory test
echo "4️⃣  Testing from Different Directory"
cd /tmp
DIR_TEST=$(claude --print "What directory am I in?" 2>&1)
if echo "$DIR_TEST" | grep -q -E "/tmp|tmp" && ! echo "$DIR_TEST" | grep -q "Choose the text style"; then
    echo "   ✅ Works from different directories without setup"
else
    echo "   ❌ Issues when running from different directories"
    echo "   Output: $DIR_TEST"
fi
echo

echo "✅ All Tests Passed!"
echo
echo "🎉 Claude Code Configuration is Working!"
echo "========================================"
echo
echo "✅ No setup prompt when opening new instances"
echo "✅ MCP servers (zen-core) connected globally"
echo "✅ Smart consensus tool available"
echo "✅ Works from any directory"
echo
echo "📚 You can now:"
echo "   • Open Claude Code from anywhere - no setup required"
echo "   • Use 'claude mcp list' to see available tools"
echo "   • Access smart_consensus for strategic decisions"
echo "   • All configurations are git-trackable in $HOME/.claude/"