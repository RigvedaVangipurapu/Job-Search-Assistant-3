# Email Configuration Setup

To enable email notifications for new Microsoft job postings, you need to configure your email settings.

## Gmail Setup (Recommended)

### 1. Enable 2-Factor Authentication
- Go to your Google Account settings
- Enable 2-Factor Authentication if not already enabled

### 2. Generate App Password
- Go to Google Account → Security → 2-Step Verification
- Scroll down to "App passwords"
- Generate a new app password for "Mail"
- Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### 3. Set Environment Variables

#### Option A: Export in Terminal (Temporary)
```bash
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-16-char-app-password"
export RECIPIENT_EMAILS="recipient1@email.com,recipient2@email.com"
```

#### Option B: Create .env file (Recommended)
Create a `.env` file in the project directory:
```bash
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-char-app-password
RECIPIENT_EMAILS=recipient1@email.com,recipient2@email.com
```

#### Option C: Add to ~/.zshrc or ~/.bashrc (Permanent)
```bash
echo 'export SENDER_EMAIL="your-email@gmail.com"' >> ~/.zshrc
echo 'export SENDER_PASSWORD="your-16-char-app-password"' >> ~/.zshrc
echo 'export RECIPIENT_EMAILS="recipient1@email.com,recipient2@email.com"' >> ~/.zshrc
source ~/.zshrc
```

## Other Email Providers

### Outlook/Hotmail
- Use your regular password (no app password needed)
- SMTP Server: `smtp-mail.outlook.com`
- Port: `587`

### Yahoo Mail
- Enable 2FA and generate app password
- SMTP Server: `smtp.mail.yahoo.com`
- Port: `587`

## Testing Email Configuration

Run this command to test your email setup:
```bash
python -c "
import os
from career_monitor import send_email_alert

# Test email
test_jobs = [{'job_title': 'Test Job', 'updated_date': 'Today', 'location': 'Test Location', 'work_arrangement': 'Remote'}]
success = send_email_alert(test_jobs, 'Test Source', 'https://test.com')
print('Email test:', 'SUCCESS' if success else 'FAILED')
"
```

## Security Notes

- Never commit your `.env` file to version control
- Use app passwords instead of your main account password
- Consider using a dedicated email account for notifications
- The `.env` file is already in `.gitignore` to prevent accidental commits

## Troubleshooting

### "Authentication failed" error
- Double-check your app password
- Ensure 2FA is enabled
- Try generating a new app password

### "Connection refused" error
- Check your internet connection
- Verify SMTP server and port settings
- Some networks block SMTP ports

### "Recipient email invalid" error
- Check email format (must include @ and valid domain)
- Ensure no extra spaces in email addresses
- Separate multiple emails with commas only
