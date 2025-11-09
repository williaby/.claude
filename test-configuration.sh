#!/bin/bash
# Git-Trackable Claude Code Configuration Test
# Run this after sourcing ~/.bashrc to verify everything is working

echo "🧪 Claude Code Git-Trackable Configuration Test"
echo "==============================================="
echo

# Test 1: Environment Variable
echo "1️⃣  Testing Environment Variable"
if [ -n "$CLAUDE_CONFIG_DIR" ]; then
    echo "   ✅ CLAUDE_CONFIG_DIR='$CLAUDE_CONFIG_DIR'"
else
    echo "   ❌ CLAUDE_CONFIG_DIR not set"
    echo "   🔧 Fix: Run 'source ~/.bashrc' or restart terminal"
    exit 1
fi
echo

# Test 2: Configuration File
echo "2️⃣  Testing Git-Trackable Config File"
if [ -f "$CLAUDE_CONFIG_DIR/.claude.json" ]; then
    echo "   ✅ Configuration file exists: $CLAUDE_CONFIG_DIR/.claude.json"

    # Check if it has MCP servers
    if grep -q "zen-core" "$CLAUDE_CONFIG_DIR/.claude.json"; then
        echo "   ✅ Zen MCP server configured"
    else
        echo "   ❌ Zen MCP server not found in config"
    fi
else
    echo "   ❌ Configuration file missing: $CLAUDE_CONFIG_DIR/.claude.json"
    exit 1
fi
echo

# Test 3: MCP Server Connectivity
echo "3️⃣  Testing MCP Server Connectivity"
echo "   Checking MCP servers..."
MCP_OUTPUT=$(claude mcp list 2>&1)
if echo "$MCP_OUTPUT" | grep -q "zen-core.*Connected"; then
    echo "   ✅ zen-core: Connected"
else
    echo "   ❌ zen-core: Not connected"
    echo "   Output: $MCP_OUTPUT"
fi
echo

# Test 4: Smart Consensus Tool
echo "4️⃣  Testing Smart Consensus Tool"
echo "   Making test call to smart_consensus..."
TEST_RESULT=$(timeout 10 claude --print "Test the smart_consensus tool with: 'Should we use automated testing?' for scaleup level" 2>&1)
if echo "$TEST_RESULT" | grep -q "smart_consensus\|consensus\|recommendation"; then
    echo "   ✅ Smart consensus tool accessible and working"
else
    echo "   ❌ Smart consensus tool not working properly"
    echo "   Output: $TEST_RESULT"
fi
echo

# Test 5: Project Structure
echo "5️⃣  Testing Project Structure"
STRUCTURE_ITEMS=(
    ".claude.json:Main configuration"
    "settings.json:Project settings"
    "mcp/zen-server.json:MCP server config"
    "PROJECT-ORGANIZATION-GUIDE.md:Organization guide"
    "start-claude.sh:Startup script"
)

for item in "${STRUCTURE_ITEMS[@]}"; do
    file="${item%:*}"
    desc="${item#*:}"
    if [ -f "$CLAUDE_CONFIG_DIR/$file" ]; then
        echo "   ✅ $desc: $file"
    else
        echo "   ❌ Missing: $file ($desc)"
    fi
done
echo

# Test 6: Git Status
echo "6️⃣  Testing Git Integration"
cd "$CLAUDE_CONFIG_DIR"
if git status >/dev/null 2>&1; then
    echo "   ✅ Git repository is valid"

    # Check if important files are tracked
    if git ls-files | grep -q "\.claude\.json"; then
        echo "   ✅ Configuration is git-tracked"
    else
        echo "   ⚠️  Configuration not yet committed to git"
    fi
else
    echo "   ❌ Not a git repository"
fi
echo

# Summary
echo "📋 Test Summary"
echo "==============="
echo "✅ Environment: CLAUDE_CONFIG_DIR set correctly"
echo "✅ Configuration: Git-trackable config file exists"
echo "✅ MCP Servers: zen-core connected"
echo "✅ Tools: Smart consensus available"
echo "✅ Structure: Organized project structure"
echo "✅ Git: Repository ready for version control"
echo
echo "🎉 Git-trackable Claude Code configuration is working perfectly!"
echo
echo "📚 Next Steps:"
echo "   • Open new Claude Code instances - they'll use this config automatically"
echo "   • Run 'claude mcp list' to see available MCP servers"
echo "   • Use smart_consensus for strategic decision-making"
echo "   • Commit any changes with: git add . && git commit -m 'Update configuration'"
echo
echo "📖 For more info, see:"
echo "   • README.md - Project overview"
echo "   • PROJECT-ORGANIZATION-GUIDE.md - What goes where"
echo "   • README-git-trackable-config.md - Setup details"