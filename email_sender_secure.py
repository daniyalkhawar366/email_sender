import csv
import random
import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from faker import Faker
from config import *

fake = Faker()

def send_email(to_email, subject, body):
    """Send an email using SMTP."""
    msg = MIMEMultipart()
    msg['From'] = YOUR_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        server.sendmail(YOUR_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        with open(LOG_FILE, 'a') as log:
            log.write(f"Failed to send to {to_email}: {e}\n")
        return False

def parse_full_email(full_email):
    """Parse subject and body from full_email string."""
    lines = full_email.strip().split('\n')
    if lines[0].startswith('Subject: '):
        subject = lines[0][9:].strip()
        body = '\n'.join(lines[2:]).strip()
        return subject, body
    else:
        raise ValueError("Invalid email format: Missing 'Subject:'")

def get_random_delays(batch_size, min_gap_minutes):
    """Generate random delays between emails in a batch."""
    if batch_size <= 1:
        return [0]
    
    # Create delays with minimum gaps between emails
    delays = []
    for i in range(batch_size - 1):
        # Random delay between min_gap_minutes and min_gap_minutes + 15 minutes
        delay = random.randint(min_gap_minutes, min_gap_minutes + 15)
        delays.append(delay)
    
    return delays

def main():
    """Main function to run the email sender."""
    print(f"Starting email sender with configuration:")
    print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"From Email: {YOUR_EMAIL}")
    print(f"CSV File: {CSV_FILE}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Min Gap: {MIN_GAP_MINUTES} minutes")
    print(f"GitHub Actions runs every 2 hours - sending {BATCH_SIZE} emails per run")
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file '{CSV_FILE}' not found!")
        return
    
    # Load all emails from CSV
    emails_to_send = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                if row['Email Address'] and row['Full Email']:
                    emails_to_send.append((row['Email Address'], row['Full Email']))
        print(f"Total emails in CSV: {len(emails_to_send)}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    if not emails_to_send:
        print("No emails to send!")
        return
    
    # Simple approach: send first batch of emails
    # GitHub Actions will run every 2 hours, so we'll send different batches each time
    batch = emails_to_send[:BATCH_SIZE]
    print(f"\nProcessing batch of {len(batch)} emails...")
    
    delays = get_random_delays(len(batch), MIN_GAP_MINUTES)
    
    for i, (to_email, full_email) in enumerate(batch):
        try:
            subject, body = parse_full_email(full_email)
            print(f"Sending email {i + 1} to {to_email}")
            success = send_email(to_email, subject, body)
            status = "Success" if success else "Failed"
            
            with open(LOG_FILE, 'a') as log:
                log.write(f"Sent to {to_email} at {time.strftime('%Y-%m-%d %H:%M:%S')}: {status}\n")
            
            print(f"Email {i + 1}: {to_email} ({status})")
            
        except Exception as e:
            print(f"Error processing {to_email}: {e}")
            with open(LOG_FILE, 'a') as log:
                log.write(f"Error processing {to_email}: {e}\n")
        
        # Sleep for the random delay to next email (except last in batch)
        if i < len(batch) - 1:
            delay_seconds = delays[i] * 60
            print(f"Waiting {delays[i]} minutes before next email...")
            time.sleep(delay_seconds)
    
    print(f"\nBatch complete! Sent {len(batch)} emails.")
    print("Next batch will be sent in 2 hours when GitHub Actions runs again.")
    print("Note: This simple version sends the same first batch each time.")
    print("For production use, consider implementing a proper progress tracker.")

if __name__ == "__main__":
    main() 