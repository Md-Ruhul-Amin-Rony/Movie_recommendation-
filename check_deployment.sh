#!/bin/bash
# Deployment Checklist Script
# Run this before pushing to GitHub

echo "🔍 Checking deployment readiness..."
echo ""

# Check if files exist
echo "📋 Checking required files:"
files=("app.py" "requirements.txt" ".env.example" "df.pkl" "tfidf.pkl" "tfidf_matrix.pkl" ".streamlit/config.toml")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - MISSING"
    fi
done

echo ""
echo "🔒 Checking security:"

# Check if .env is in .gitignore
if grep -q "^\.env$" .gitignore; then
    echo "✅ .env is in .gitignore"
else
    echo "❌ .env should be in .gitignore"
fi

# Check if .env exists and shouldn't be committed
if [ -f ".env" ]; then
    if git ls-files --error-unmatch .env 2>/dev/null; then
        echo "⚠️  WARNING: .env is tracked by git - should not be committed!"
    else
        echo "✅ .env exists but not tracked by git (good)"
    fi
fi

echo ""
echo "📦 Checking dependencies:"
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt exists"
    echo "   Dependencies listed:"
    grep -v "^#" requirements.txt | grep -v "^$" | head -5
    echo "   ... (showing first 5)"
else
    echo "❌ requirements.txt missing"
fi

echo ""
echo "✨ All checks complete!"
echo ""
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m 'Prepare for Streamlit Cloud deployment'"
echo "3. git push origin main"
echo "4. Go to https://share.streamlit.io and deploy!"
