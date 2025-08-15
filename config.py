import os

# Configuration - Load from environment variables for security
YOUR_EMAIL = os.getenv('YOUR_EMAIL', 'albytechco2@gmail.com')
YOUR_PASSWORD = os.getenv('YOUR_PASSWORD', 'vpeejiebbybobczg')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
CSV_FILE = os.getenv('CSV_FILE', 'smykm_emails.csv')
LOG_FILE = os.getenv('LOG_FILE', 'email_log.txt')

# Email sending configuration
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '3'))
MIN_GAP_MINUTES = int(os.getenv('MIN_GAP_MINUTES', '30')) 