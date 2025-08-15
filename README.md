# Email Sender - GitHub Actions Hosted

This repository contains a secure email sender script that runs automatically via GitHub Actions for 24/7 cold emailing operations.

## ⚠️ SECURITY WARNING

**NEVER commit sensitive information to this repository!**
- Email credentials
- CSV files with lead data
- Log files

## Setup Instructions

### 1. Repository Setup

1. Clone this repository to your local machine
2. **IMPORTANT**: Delete or move these sensitive files locally:
   - `Email_sender.py` (contains hardcoded credentials)
   - `smykm_emails.csv` (contains lead data)
   - `email_log.txt` (contains logs)

### 2. GitHub Secrets Configuration

Go to your repository → Settings → Secrets and variables → Actions, then add these secrets:

#### Required Secrets:
- `YOUR_EMAIL`: Your Gmail address (e.g., albytechco2@gmail.com)
- `YOUR_PASSWORD`: Your Gmail app password (vpeejiebbybobczg)
- `SMTP_SERVER`: smtp.gmail.com
- `SMTP_PORT`: 587
- `CSV_DATA`: The entire content of your smykm_emails.csv file (copy-paste the whole file content)

#### Optional Secrets (with defaults):
- `BATCH_SIZE`: 3 (emails per batch)
- `WINDOW_MINUTES`: 120 (2 hours between batches)
- `MIN_GAP_MINUTES`: 30 (minimum gap between emails in a batch)

### 3. CSV Data Setup

1. Open your `smykm_emails.csv` file
2. Select all content (Ctrl+A)
3. Copy (Ctrl+C)
4. In GitHub Secrets, paste this entire content as the `CSV_DATA` secret

### 4. How It Works

- **GitHub Actions** runs the script every 2 hours automatically
- **Environment variables** securely load your credentials
- **CSV data** is reconstructed from GitHub secrets
- **Logs** are uploaded as artifacts for monitoring
- **Manual triggering** available via GitHub Actions tab

## File Structure

```
├── .github/workflows/email_sender.yml  # GitHub Actions workflow
├── email_sender_secure.py              # Secure email sender script
├── config.py                           # Configuration loader
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Prevents sensitive files from being committed
└── README.md                          # This file
```

## Monitoring

- Check the **Actions** tab in your GitHub repository
- View logs and execution status
- Download log artifacts for detailed monitoring
- Manual trigger available for testing

## Security Features

✅ **No hardcoded credentials**  
✅ **Environment variables for sensitive data**  
✅ **CSV data stored in GitHub secrets**  
✅ **Automatic log cleanup**  
✅ **Secure file exclusions**  

## Troubleshooting

### Common Issues:

1. **Authentication failed**: Check your Gmail app password
2. **CSV not found**: Ensure CSV_DATA secret is properly set
3. **Workflow not running**: Check Actions tab and cron schedule
4. **Rate limiting**: Gmail has daily sending limits

### Gmail Setup:

1. Enable 2-factor authentication
2. Generate an app password
3. Use app password (not regular password)

## Support

For issues or questions, check the GitHub Actions logs or create an issue in the repository.

---

**Remember**: This setup keeps your sensitive data secure while enabling 24/7 email automation through GitHub's free hosting. 