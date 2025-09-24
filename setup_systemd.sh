#!/bin/bash
# Setup script for systemd service (Linux/macOS with systemd)

echo "🚀 Setting up Microsoft Career Monitor as systemd service"

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/microsoft-career-monitor.service"

echo "📁 Script directory: $SCRIPT_DIR"

# Copy service file to systemd directory
sudo cp "$SERVICE_FILE" /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable the service
sudo systemctl enable microsoft-career-monitor.service

echo "✅ Systemd service installed and enabled!"
echo ""
echo "🔧 Service management commands:"
echo "   Start:   sudo systemctl start microsoft-career-monitor"
echo "   Stop:    sudo systemctl stop microsoft-career-monitor"
echo "   Status:  sudo systemctl status microsoft-career-monitor"
echo "   Logs:    sudo journalctl -u microsoft-career-monitor -f"
echo ""
echo "📧 Don't forget to configure email settings in the service file:"
echo "   sudo nano /etc/systemd/system/microsoft-career-monitor.service"
echo "   Then restart: sudo systemctl restart microsoft-career-monitor"
