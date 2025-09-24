# Microsoft Career Hourly Monitoring System

🚀 **Automated Microsoft job monitoring with hourly email notifications**

This system monitors Microsoft's career page every hour for new job postings and sends instant email alerts when new jobs are found.

## ✨ Features

- ⏰ **Hourly monitoring** - Checks for new jobs every hour
- 📧 **Email notifications** - Instant alerts for new job postings
- 🔍 **Smart extraction** - Finds jobs updated "Today" with duplicate detection
- 📊 **Data tracking** - Remembers previously seen jobs to avoid spam
- 🎯 **Targeted search** - Focuses on Data Engineering, Science, Analytics roles
- 🖥️ **Multiple deployment options** - Cron jobs, systemd service, or manual execution

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 2. Configure Email (Required for notifications)
```bash
# Set your email credentials
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"  # Use Gmail App Password
export RECIPIENT_EMAILS="recipient1@email.com,recipient2@email.com"
```

📧 **See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed email configuration**

### 3. Test the System
```bash
# Test job extraction
python career_monitor.py

# Test hourly monitoring (runs once)
python hourly_monitor.py
```

## 🔧 Deployment Options

### Option A: Cron Job (Recommended for macOS/Linux)
```bash
# Set up hourly cron job
./setup_cron.sh

# View logs
tail -f monitor.log
```

### Option B: Systemd Service (Linux)
```bash
# Set up as system service
./setup_systemd.sh

# Manage service
sudo systemctl start microsoft-career-monitor
sudo systemctl status microsoft-career-monitor
```

### Option C: Manual Execution
```bash
# Run once
python career_monitor.py

# Run continuously (hourly)
python hourly_monitor.py
```

## 📊 What It Monitors

**Job Categories:**
- Data Engineering
- Data Science  
- Data Analytics
- Business Analytics

**Job Filters:**
- Individual Contributor roles
- Full-time positions
- Jobs updated "Today"
- United States locations

## 📁 Project Structure

```
├── career_monitor.py          # Main job extraction script
├── hourly_monitor.py          # Hourly scheduler
├── show_top_jobs.py           # Display extracted jobs
├── setup_cron.sh              # Cron job setup
├── setup_systemd.sh           # Systemd service setup
├── microsoft-career-monitor.service  # Systemd service file
├── EMAIL_SETUP.md             # Email configuration guide
├── requirements.txt           # Python dependencies
├── known_todays_jobs.json     # Job tracking database
└── monitor.log                # System logs
```

## 🔍 How It Works

1. **Hourly Check** - Runs every hour automatically
2. **Job Extraction** - Scrapes Microsoft careers page for "Today" jobs
3. **Duplicate Detection** - Avoids counting the same job multiple times
4. **Change Detection** - Compares with previous runs to find new jobs
5. **Email Alerts** - Sends notifications only when new jobs are found
6. **Data Persistence** - Saves job data for comparison

## 📧 Email Notifications

When new jobs are found, you'll receive emails like:

```
🚨 Microsoft: 2 new jobs updated today!

🎯 Microsoft Careers - Jobs Updated Today Alert
==================================================

⏰ Time: 2025-09-23 14:30:00
📋 Microsoft Data Jobs (Engineering, Science, Analytics)
📅 Updated: September 23, 2025

🎉 2 new job(s) updated today!

   1. Senior Data Engineer
      📅 Updated: Today
      📍 Location: Redmond, WA
      🏢 Work: Hybrid

   2. Data Engineer II
      📅 Updated: Today
      📍 Location: Remote
      🏢 Work: Remote

🔗 View all jobs: https://jobs.careers.microsoft.com/...
```

## 🛠️ Troubleshooting

### No Jobs Found
- Check `career_page_screenshot.png` to see what the scraper sees
- Verify the Microsoft careers page structure hasn't changed
- Check logs: `tail -f monitor.log`

### Email Not Working
- Verify email configuration: `echo $SENDER_EMAIL`
- Test email setup: See EMAIL_SETUP.md
- Check Gmail app password is correct

### Cron Job Not Running
- Check cron status: `crontab -l`
- Verify file paths in cron job
- Check logs: `tail -f monitor.log`

### Systemd Service Issues
- Check service status: `sudo systemctl status microsoft-career-monitor`
- View logs: `sudo journalctl -u microsoft-career-monitor -f`
- Verify service file paths and permissions

## 🔒 Security Notes

- Email passwords are stored in environment variables
- Never commit `.env` files or credentials to version control
- Use app passwords instead of main account passwords
- Consider using a dedicated email account for notifications

## 📈 Monitoring & Logs

**Log Files:**
- `monitor.log` - System activity and job detection logs
- `known_todays_jobs.json` - Database of tracked jobs

**Key Log Messages:**
- `🔄 Starting hourly job check...` - System starting
- `🎉 Found X new job(s)!` - New jobs detected
- `✅ No new jobs found this hour` - No changes detected
- `📧 Email alert sent!` - Notification sent successfully

## 🎯 Success Metrics

The system successfully:
- ✅ Extracts job titles with duplicate detection
- ✅ Tracks job changes between runs  
- ✅ Sends email notifications for new jobs
- ✅ Runs automatically every hour
- ✅ Handles errors gracefully
- ✅ Logs all activity for debugging

---

**Ready to get notified about new Microsoft jobs? Set up your email and run `./setup_cron.sh`!** 🚀