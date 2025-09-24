#!/bin/bash
# Setup script for hourly Microsoft job monitoring

echo "🚀 Setting up Microsoft Career Hourly Monitor"

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH=$(which python3)

echo "📁 Script directory: $SCRIPT_DIR"
echo "🐍 Python path: $PYTHON_PATH"

# Create the cron job
CRON_JOB="0 * * * * cd $SCRIPT_DIR && $PYTHON_PATH hourly_monitor.py >> monitor.log 2>&1"

echo "⏰ Adding cron job: $CRON_JOB"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job added successfully!"
echo ""
echo "📋 Current crontab:"
crontab -l
echo ""
echo "🔍 To view logs: tail -f $SCRIPT_DIR/monitor.log"
echo "🛑 To remove cron job: crontab -e (then delete the line)"
echo ""
echo "📧 Don't forget to set up email configuration:"
echo "   export SENDER_EMAIL='your-email@gmail.com'"
echo "   export SENDER_PASSWORD='your-app-password'"
echo "   export RECIPIENT_EMAILS='recipient1@email.com,recipient2@email.com'"
