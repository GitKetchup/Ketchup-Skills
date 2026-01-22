#!/bin/bash
# Ketchup MCP Server Setup Script
# This script helps you install and configure the Ketchup MCP server

set -e

echo "🍅 Ketchup MCP Server Setup"
echo "=========================="
echo ""

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "❌ Python 3 is required but not found."
    echo "   Please install Python 3.11+ from https://python.org"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip found"
else
    echo "❌ pip not found. Please install pip."
    exit 1
fi

# Install ketchup-mcp
echo ""
echo "📦 Installing ketchup-mcp..."
pip3 install --upgrade ketchup-mcp

# Verify installation
if command -v ketchup-mcp &> /dev/null; then
    echo "✅ ketchup-mcp installed successfully"
else
    echo "⚠️  ketchup-mcp command not in PATH"
    echo "   Try: python3 -m ketchup_mcp.server"
fi

# API Key setup
echo ""
echo "🔑 API Key Configuration"
echo "------------------------"
if [ -z "$KETCHUP_API_KEY" ]; then
    echo "No KETCHUP_API_KEY found in environment."
    echo ""
    read -p "Do you have a Ketchup API key? (y/n): " has_key
    
    if [ "$has_key" = "y" ]; then
        read -p "Enter your API key: " api_key
        echo ""
        echo "Add this to your shell profile (~/.zshrc or ~/.bashrc):"
        echo "  export KETCHUP_API_KEY=\"$api_key\""
    else
        echo ""
        echo "📝 Get an API key at: https://app.gitketchup.com/settings"
        echo "   (Optional - local tools work without an API key)"
    fi
else
    echo "✅ KETCHUP_API_KEY is set"
fi

# Claude Desktop configuration
echo ""
echo "🤖 Claude Desktop Configuration"
echo "--------------------------------"
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ -f "$CLAUDE_CONFIG" ]; then
    echo "Claude Desktop config found."
    echo ""
    echo "Add this to your mcpServers in claude_desktop_config.json:"
else
    echo "Claude Desktop config not found."
    echo "Create $CLAUDE_CONFIG with:"
fi

echo ""
cat << 'EOF'
{
  "mcpServers": {
    "ketchup": {
      "command": "ketchup-mcp",
      "env": {
        "KETCHUP_API_KEY": "your-api-key-here"
      }
    }
  }
}
EOF

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Desktop"
echo "  2. Ask Claude to 'analyze complexity of this repo'"
echo "  3. Explore more tools with 'list ketchup tools'"
echo ""
echo "Documentation: https://docs.gitketchup.com/skills"
