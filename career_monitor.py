#!/usr/bin/env python3
"""
Automated Microsoft Career Page Notification System
Monitors Microsoft Careers for jobs updated today and sends email alerts
"""

from playwright.sync_api import sync_playwright
import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, date
import re

# Configuration variables - Microsoft URLs to monitor
TARGET_URLS = {
    "microsoft_data_jobs": {
        "url": "https://jobs.careers.microsoft.com/global/en/search?lc=United%20States&d=Data%20Engineering&d=Data%20Science&d=Data%20Analytics&d=Business%20Analytics&rt=Individual%20Contributor&et=Full-Time&et=Full-time&l=en_us&pg=1&pgSz=20&o=Recent&flt=true",
        "name": "Microsoft Data Jobs (Engineering, Science, Analytics)"
    }
}

SCREENSHOT_PATH = "career_page_screenshot.png"
KNOWN_TODAYS_JOBS_FILE = "known_todays_jobs.json"  # Track jobs updated today

# Email configuration (will be set via environment variables in GitHub Actions)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')
RECIPIENT_EMAILS = os.getenv('RECIPIENT_EMAILS', '')  # Comma-separated list of emails

def extract_todays_jobs(page):
    """Extract jobs that were updated today from the Microsoft career page"""
    print("Extracting jobs updated today...")
    
    try:
        # Wait for the page to load completely
        page.wait_for_load_state("domcontentloaded")
        
        # Get today's date in the format used by Microsoft (Today, Yesterday, etc.)
        today = date.today()
        print(f"Looking for jobs updated today: {today.strftime('%Y-%m-%d')}")
        
        # Find all job elements using the specific structure provided
        # Looking for the ms-Stack css-490 div that contains job information
        job_containers = page.query_selector_all('div.ms-Stack.css-490')
        print(f"Found {len(job_containers)} job containers with ms-Stack css-490")
        
        todays_jobs = []
        seen_jobs = set()  # Track unique jobs to avoid duplicates
        
        for i, container in enumerate(job_containers):
            try:
                container_text = container.inner_text()
                print(f"Container {i} text: {container_text[:200]}...")
                
                # Check if this container has "Today" in it
                if "Today" in container_text:
                    print(f"Found job container {i} with 'Today'")
                    
                    # Look for job title in h2 element with class MZGzlrn8gfgSs8TZHhv2
                    title_element = container.query_selector('h2.MZGzlrn8gfgSs8TZHhv2')
                    if title_element:
                        job_title = title_element.inner_text().strip()
                        # Clean up the title (remove &nbsp; and extra whitespace)
                        job_title = re.sub(r'&nbsp;', ' ', job_title)
                        job_title = re.sub(r'\s+', ' ', job_title).strip()
                        
                        if job_title and len(job_title) > 5:
                            # Check for duplicates
                            if job_title in seen_jobs:
                                print(f"Duplicate job found, skipping: {job_title}")
                                continue
                            
                            seen_jobs.add(job_title)
                            
                            # Extract location and work arrangement info
                            location = "Unknown"
                            work_arrangement = "Unknown"
                            
                            # Look for location info
                            location_elements = container.query_selector_all('span')
                            for span in location_elements:
                                span_text = span.inner_text().strip()
                                if any(city in span_text for city in ['Redmond', 'Seattle', 'Washington', 'United States', 'Remote', 'Hybrid']):
                                    location = span_text
                                    break
                            
                            # Look for work arrangement info
                            for span in location_elements:
                                span_text = span.inner_text().strip()
                                if any(arrangement in span_text for arrangement in ['days / week', 'in-office', 'remote', 'hybrid']):
                                    work_arrangement = span_text
                                    break
                            
                            job_info = {
                                'title': job_title,
                                'updated_date': 'Today',
                                'location': location,
                                'work_arrangement': work_arrangement,
                                'element_text': f"Found in container {i}"
                            }
                            todays_jobs.append(job_info)
                            print(f"Found job updated today: {job_title} - {location} - {work_arrangement}")
                        else:
                            print(f"Job title too short or empty in container {i}")
                    else:
                        print(f"Could not find h2.MZGzlrn8gfgSs8TZHhv2 element in container {i}")
                        
                        # Try alternative selectors for job title
                        alt_title_selectors = [
                            'h2[class*="MZGzlrn8gfgSs8TZHhv2"]',
                            'h2',
                            'h1',
                            'h3',
                            '[class*="title"]',
                            'a[href*="/jobs/"]'
                        ]
                        
                        for selector in alt_title_selectors:
                            title_element = container.query_selector(selector)
                            if title_element:
                                job_title = title_element.inner_text().strip()
                                job_title = re.sub(r'&nbsp;', ' ', job_title)
                                job_title = re.sub(r'\s+', ' ', job_title).strip()
                                
                                if job_title and len(job_title) > 5 and len(job_title) < 200:
                                    # Filter out common non-job elements
                                    if not any(skip in job_title.lower() for skip in ['search', 'filter', 'sort', 'apply', 'browse', 'view all', 'microsoft', 'careers']):
                                        # Check for duplicates
                                        if job_title in seen_jobs:
                                            print(f"Duplicate job found (alt selector), skipping: {job_title}")
                                            break
                                        
                                        seen_jobs.add(job_title)
                                        
                                        job_info = {
                                            'title': job_title,
                                            'updated_date': 'Today',
                                            'location': 'Unknown',
                                            'work_arrangement': 'Unknown',
                                            'element_text': f"Found in container {i} with selector {selector}"
                                        }
                                        todays_jobs.append(job_info)
                                        print(f"Found job updated today (alt selector): {job_title}")
                                        break
                        
            except Exception as e:
                print(f"Error processing container {i}: {str(e)}")
                continue
        
        # If we didn't find any jobs with the specific structure, try a broader search
        if not todays_jobs:
            print("Specific structure not found, trying broader search...")
            
            # Look for any elements containing "Today"
            today_elements = page.query_selector_all('*')
            for element in today_elements:
                try:
                    text = element.inner_text().strip()
                    if "Today" in text and len(text) < 1000:  # Avoid very large text blocks
                        # Look for job title in nearby elements
                        parent = element
                        for level in range(10):
                            if parent is None:
                                break
                            
                            # Look for job title in current element and descendants
                            title_selectors = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a[href*="/jobs/"]']
                            
                            for selector in title_selectors:
                                title_element = parent.query_selector(selector)
                                if title_element:
                                    job_title = title_element.inner_text().strip()
                                    job_title = re.sub(r'&nbsp;', ' ', job_title)
                                    job_title = re.sub(r'\s+', ' ', job_title).strip()
                                    
                                    if job_title and len(job_title) > 5 and len(job_title) < 200:
                                        if not any(skip in job_title.lower() for skip in ['search', 'filter', 'sort', 'apply', 'browse', 'view all', 'microsoft', 'careers', 'today', 'yesterday']):
                                            # Check for duplicates
                                            if job_title in seen_jobs:
                                                print(f"Duplicate job found (broader search), skipping: {job_title}")
                                                break
                                            
                                            seen_jobs.add(job_title)
                                            
                                            job_info = {
                                                'title': job_title,
                                                'updated_date': 'Today',
                                                'location': 'Unknown',
                                                'work_arrangement': 'Unknown',
                                                'element_text': f"Found via broader search at level {level}"
                                            }
                                            todays_jobs.append(job_info)
                                            print(f"Found job via broader search: {job_title}")
                                            break
                            
                            if job_title:
                                break
                                
                            parent = parent.evaluate('el => el.parentElement')
                            
                except Exception as e:
                    continue
        
        print(f"Found {len(todays_jobs)} jobs updated today")
        return todays_jobs
        
    except Exception as e:
        print(f"Error extracting today's jobs: {str(e)}")
        return []

def load_known_todays_jobs():
    """Load previously known today's jobs from JSON file"""
    try:
        if os.path.exists(KNOWN_TODAYS_JOBS_FILE):
            with open(KNOWN_TODAYS_JOBS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading known today's jobs: {str(e)}")
        return {}

def save_todays_jobs(todays_jobs):
    """Save today's jobs to JSON file"""
    try:
        with open(KNOWN_TODAYS_JOBS_FILE, 'w') as f:
            json.dump(todays_jobs, f, indent=2)
        print(f"Saved today's jobs to {KNOWN_TODAYS_JOBS_FILE}")
    except Exception as e:
        print(f"Error saving today's jobs: {str(e)}")

def compare_todays_jobs(current_jobs, previous_jobs, source_name):
    """Compare current and previous today's jobs and return new jobs"""
    new_jobs = []
    
    if not previous_jobs:
        # First run - all jobs are new
        for job in current_jobs:
            new_jobs.append({
                'action': 'new',
                'job_title': job['title'],
                'updated_date': job['updated_date'],
                'location': job.get('location', 'Unknown'),
                'work_arrangement': job.get('work_arrangement', 'Unknown')
            })
        return new_jobs
    
    # Get previous job titles for comparison
    previous_titles = [job['title'] for job in previous_jobs]
    
    # Check for new jobs
    for job in current_jobs:
        if job['title'] not in previous_titles:
            new_jobs.append({
                'action': 'new',
                'job_title': job['title'],
                'updated_date': job['updated_date'],
                'location': job.get('location', 'Unknown'),
                'work_arrangement': job.get('work_arrangement', 'Unknown')
            })
    
    return new_jobs

def send_email_alert(new_jobs, source_name, source_url):
    """Send email alert when new jobs updated today are found"""
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAILS]):
        print("Email configuration incomplete. Skipping email alert.")
        return False
    
    # Parse recipient emails (comma-separated)
    recipient_list = [email.strip() for email in RECIPIENT_EMAILS.split(',') if email.strip()]
    if not recipient_list:
        print("No valid recipient emails found. Skipping email alert.")
        return False
    
    if not new_jobs:
        print("No new jobs found. Skipping email alert.")
        return False
    
    try:
        # Create personalized subject
        job_count = len(new_jobs)
        if job_count == 1:
            subject = f"🚨 Microsoft: 1 new job updated today!"
        else:
            subject = f"🚨 Microsoft: {job_count} new jobs updated today!"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ', '.join(recipient_list)
        msg['Subject'] = subject
        
        # Build personalized email body
        body = "🎯 Microsoft Careers - Jobs Updated Today Alert\n"
        body += "=" * 50 + "\n\n"
        body += f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        body += f"📋 {source_name}\n"
        body += f"📅 Updated: {date.today().strftime('%B %d, %Y')}\n\n"
        
        body += f"🎉 {job_count} new job(s) updated today!\n\n"
        
        # List the new jobs
        for i, job in enumerate(new_jobs, 1):
            body += f"   {i}. {job['job_title']}\n"
            body += f"      📅 Updated: {job['updated_date']}\n"
            if job.get('location') != 'Unknown':
                body += f"      📍 Location: {job['location']}\n"
            if job.get('work_arrangement') != 'Unknown':
                body += f"      🏢 Work: {job['work_arrangement']}\n"
            body += "\n"
        
        body += f"🔗 View all jobs: {source_url}\n\n"
        body += "🤖 This is an automated alert from your Microsoft career monitoring system.\n"
        body += "💡 Set up job alerts on Microsoft Careers for instant notifications!"
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email to all recipients
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, recipient_list, text)
        server.quit()
        
        print(f"📧 Email alert sent to {len(recipient_list)} recipient(s)! {job_count} new job(s) found.")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def main():
    """Main function to monitor Microsoft job sources and send alerts"""
    print("Starting Microsoft career monitoring system...")
    print(f"Monitoring {len(TARGET_URLS)} job sources:")
    for key, config in TARGET_URLS.items():
        print(f"  • {config['name']}")
    
    try:
        with sync_playwright() as p:
            # Launch browser
            print("\nLaunching browser...")
            browser = p.chromium.launch(headless=True)  # Headless for GitHub Actions
            page = browser.new_page()
            
            # Load previous today's jobs
            known_todays_jobs = load_known_todays_jobs()
            current_todays_jobs = {}
            all_new_jobs = []
            
            # Monitor each URL
            for source_key, config in TARGET_URLS.items():
                print(f"\n--- Monitoring {config['name']} ---")
                print(f"URL: {config['url']}")
                
                try:
                    # Navigate to the URL with longer timeout and different wait strategy
                    print("Navigating to Microsoft careers page...")
                    page.goto(config['url'], timeout=60000, wait_until="domcontentloaded")
                    
                    # Wait a bit more for dynamic content
                    page.wait_for_timeout(5000)
                    
                    # Take a screenshot for debugging
                    page.screenshot(path=SCREENSHOT_PATH)
                    print(f"Screenshot saved as {SCREENSHOT_PATH}")
                    
                    # Extract jobs updated today
                    current_jobs = extract_todays_jobs(page)
                    current_todays_jobs[source_key] = current_jobs
                    
                    print(f"Found {len(current_jobs)} jobs updated today")
                    
                    # Compare with previous today's jobs
                    previous_jobs = known_todays_jobs.get(source_key, [])
                    new_jobs = compare_todays_jobs(current_jobs, previous_jobs, config['name'])
                    
                    if new_jobs:
                        all_new_jobs.extend(new_jobs)
                        print(f"New jobs detected: {len(new_jobs)} new jobs")
                        for job in new_jobs:
                            print(f"  🆕 New: {job['job_title']}")
                    else:
                        print("No new jobs updated today")
                
                except Exception as e:
                    print(f"Error monitoring {config['name']}: {str(e)}")
                    continue
            
            # Close browser
            browser.close()
            
            # Send email if there were new jobs
            if all_new_jobs:
                print(f"\n📧 Sending email alert...")
                print(f"  • {len(all_new_jobs)} new job(s) found")
                
                # Send alert for the first source (assuming single source for now)
                source_key = list(TARGET_URLS.keys())[0]
                source_config = TARGET_URLS[source_key]
                
                if send_email_alert(all_new_jobs, source_config['name'], source_config['url']):
                    print("Email alert sent successfully!")
                else:
                    print("Failed to send email alert.")
            else:
                print("\n✅ No new jobs updated today.")
            
            # Update stored today's jobs
            save_todays_jobs(current_todays_jobs)
            
            print("\n🎯 Microsoft career monitoring completed successfully!")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("Script completed successfully!")
    else:
        print("Script failed!")
