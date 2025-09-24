#!/usr/bin/env python3
"""
Hourly Microsoft Career Monitoring System
Checks every hour for new job postings and sends email notifications
"""

import schedule
import time
import os
import sys
from datetime import datetime
import json
from career_monitor import main as run_job_monitor, load_known_todays_jobs, save_todays_jobs

# Configuration
LOG_FILE = "monitor.log"
CHECK_INTERVAL_HOURS = 1  # Check every hour

def log_message(message):
    """Log message with timestamp to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    print(log_entry)
    
    # Write to log file
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def check_for_new_jobs():
    """Check for new jobs and send notifications if found"""
    log_message("🔄 Starting hourly job check...")
    
    try:
        # Load previous jobs
        previous_jobs = load_known_todays_jobs()
        previous_count = sum(len(jobs) for jobs in previous_jobs.values())
        
        log_message(f"📊 Previous jobs count: {previous_count}")
        
        # Run the job monitor
        log_message("🔍 Running job extraction...")
        success = run_job_monitor()
        
        if not success:
            log_message("❌ Job extraction failed")
            return
        
        # Load current jobs after extraction
        current_jobs = load_known_todays_jobs()
        current_count = sum(len(jobs) for jobs in current_jobs.values())
        
        log_message(f"📊 Current jobs count: {current_count}")
        
        # Check if there are new jobs
        if current_count > previous_count:
            new_jobs_count = current_count - previous_count
            log_message(f"🎉 Found {new_jobs_count} new job(s)! Email notification sent.")
        else:
            log_message("✅ No new jobs found this hour")
            
    except Exception as e:
        log_message(f"❌ Error during job check: {str(e)}")

def setup_email_config():
    """Check and display email configuration status"""
    log_message("📧 Checking email configuration...")
    
    required_vars = ['SENDER_EMAIL', 'SENDER_PASSWORD', 'RECIPIENT_EMAILS']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        log_message("⚠️  Email configuration incomplete. Missing:")
        for var in missing_vars:
            log_message(f"   • {var}")
        log_message("📝 To enable email notifications, set these environment variables:")
        log_message("   export SENDER_EMAIL='your-email@gmail.com'")
        log_message("   export SENDER_PASSWORD='your-app-password'")
        log_message("   export RECIPIENT_EMAILS='recipient1@email.com,recipient2@email.com'")
        return False
    else:
        log_message("✅ Email configuration complete")
        return True

def main():
    """Main function to run the hourly monitoring system"""
    log_message("🚀 Starting Microsoft Career Hourly Monitor")
    log_message(f"⏰ Will check every {CHECK_INTERVAL_HOURS} hour(s)")
    
    # Check email configuration
    email_configured = setup_email_config()
    
    if not email_configured:
        log_message("⚠️  Running without email notifications (jobs will still be tracked)")
    
    # Schedule the job check
    schedule.every(CHECK_INTERVAL_HOURS).hours.do(check_for_new_jobs)
    
    # Run initial check
    log_message("🔍 Running initial job check...")
    check_for_new_jobs()
    
    # Keep the script running
    log_message("⏳ Monitoring started. Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for scheduled tasks
    except KeyboardInterrupt:
        log_message("🛑 Monitoring stopped by user")
    except Exception as e:
        log_message(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
