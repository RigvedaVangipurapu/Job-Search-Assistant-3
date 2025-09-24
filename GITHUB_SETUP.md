# GitHub Secrets Setup for Email Notifications

This guide will help you configure email notifications using GitHub Secrets, which is the most secure way to store sensitive information.

## 🔐 Setting Up GitHub Secrets

### Step 1: Navigate to Repository Settings
1. Go to your repository: https://github.com/RigvedaVangipurapu/Job-Search-Assistant-3
2. Click on **Settings** tab (top navigation)
3. In the left sidebar, click **Secrets and variables** → **Actions**

### Step 2: Add Required Secrets
Click **New repository secret** for each of these:

#### 1. SENDER_EMAIL
- **Name**: `SENDER_EMAIL`
- **Value**: `your-email@gmail.com` (your Gmail address)

#### 2. SENDER_PASSWORD
- **Name**: `SENDER_PASSWORD`
- **Value**: `your-16-character-app-password` (Gmail App Password)

#### 3. RECIPIENT_EMAILS
- **Name**: `RECIPIENT_EMAILS`
- **Value**: `recipient1@email.com,recipient2@email.com` (comma-separated)

#### 4. SMTP_SERVER (Optional - defaults to Gmail)
- **Name**: `SMTP_SERVER`
- **Value**: `smtp.gmail.com`

#### 5. SMTP_PORT (Optional - defaults to 587)
- **Name**: `SMTP_PORT`
- **Value**: `587`

## 📧 Gmail App Password Setup

If you haven't set up Gmail App Password yet:

1. **Enable 2-Factor Authentication** on your Google Account
2. Go to **Google Account** → **Security** → **2-Step Verification**
3. Scroll down to **App passwords**
4. Select **Mail** and **Other (Custom name)**
5. Enter "Microsoft Job Monitor" as the name
6. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)
7. Use this password as your `SENDER_PASSWORD` secret

## 🔄 GitHub Actions Workflow

The repository includes a GitHub Actions workflow that will:
- Run every hour automatically
- Use your configured secrets for email notifications
- Monitor Microsoft careers for new job postings
- Send email alerts when new jobs are found

### Workflow File Location
`.github/workflows/monitor.yml`

### Manual Trigger
You can also trigger the workflow manually:
1. Go to **Actions** tab in your repository
2. Select **Microsoft Job Monitor** workflow
3. Click **Run workflow** button

## 🧪 Testing Your Setup

### Test Email Configuration
Once you've set up the secrets, you can test by:

1. **Manual workflow run**:
   - Go to Actions → Microsoft Job Monitor
   - Click "Run workflow"
   - Check the logs for email sending status

2. **Check workflow logs**:
   - Look for messages like "📧 Email alert sent successfully!"
   - If there are errors, they'll be shown in the logs

## 🔒 Security Benefits

Using GitHub Secrets provides:
- ✅ **Encrypted storage** - Secrets are encrypted at rest
- ✅ **Access control** - Only repository collaborators can see/use secrets
- ✅ **Audit trail** - GitHub tracks when secrets are accessed
- ✅ **No local storage** - No sensitive data in your local files
- ✅ **Easy rotation** - Update secrets without code changes

## 📋 Required Secrets Summary

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `SENDER_EMAIL` | Your Gmail address | `your-email@gmail.com` |
| `SENDER_PASSWORD` | Gmail App Password | `abcd efgh ijkl mnop` |
| `RECIPIENT_EMAILS` | Comma-separated recipients | `user1@email.com,user2@email.com` |
| `SMTP_SERVER` | SMTP server (optional) | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port (optional) | `587` |

## 🚀 Next Steps

1. **Set up all secrets** in GitHub repository settings
2. **Enable GitHub Actions** (if not already enabled)
3. **Test the workflow** with a manual run
4. **Monitor the logs** to ensure everything works
5. **Wait for hourly runs** to get job notifications!

## 🛠️ Troubleshooting

### "Secrets not found" error
- Verify secret names match exactly (case-sensitive)
- Check that secrets are in the correct repository
- Ensure you're using the right branch

### "Authentication failed" error
- Double-check your Gmail App Password
- Verify 2FA is enabled on your Google Account
- Try generating a new App Password

### "Workflow not running" error
- Check that GitHub Actions is enabled
- Verify the workflow file is in `.github/workflows/`
- Check the workflow syntax in the Actions tab

---

**Once configured, you'll receive hourly email notifications about new Microsoft job postings!** 🎉
