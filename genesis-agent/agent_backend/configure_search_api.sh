#!/bin/bash
# Quick configuration script for Web Search API

echo "🔧 Configuring Web Search API..."
echo ""

# Prompt for Search Engine ID
echo "Please paste your Google Search Engine ID:"
echo "(Get it from: https://programmablesearchengine.google.com/controlpanel/all)"
read -p "Search Engine ID: " SEARCH_ENGINE_ID

# Create the .env.search file
cat > .env.search << EOF
# Google Custom Search API Configuration
# ✅ Configured on $(date)

export GOOGLE_SEARCH_API_KEY="AIzaSyCFbSXSYMdyViQfeQQwcJ3lVrm54kysnFE"
export GOOGLE_SEARCH_ENGINE_ID="$SEARCH_ENGINE_ID"

# Usage: source .env.search before starting JAi
EOF

echo ""
echo "✅ Configuration saved to .env.search"
echo ""
echo "📝 Your settings:"
echo "   API Key: AIzaSyCF...kysnFE (configured)"
echo "   Search Engine ID: $SEARCH_ENGINE_ID"
echo ""
echo "🚀 Ready to start JAi with Web Power-Up!"
echo ""
echo "Run: ./setup_web_search.sh"

