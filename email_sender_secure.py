import csv
import random
import time
import smtplib
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from faker import Faker
from config import *

fake = Faker()

def load_progress():
    """Load progress from file."""
    progress_file = 'email_progress.json'
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                progress = json.load(f)
                
            # Ensure all required keys exist (backward compatibility)
            if 'all_sent_emails' not in progress:
                progress['all_sent_emails'] = []
            if 'last_batch' not in progress:
                progress['last_batch'] = []
            if 'sent_count' not in progress:
                progress['sent_count'] = 0
                
            # If we have old progress data, populate all_sent_emails
            if progress['last_batch'] and not progress['all_sent_emails']:
                progress['all_sent_emails'] = progress['last_batch'].copy()
                
            return progress
        except Exception as e:
            print(f"Warning: Error loading progress file: {e}")
            print("Creating new progress file...")
    
    return {'sent_count': 0, 'last_batch': [], 'all_sent_emails': []}

def save_progress(progress):
    """Save progress to file."""
    try:
        with open('email_progress.json', 'w') as f:
            json.dump(progress, f, indent=2)
        print(f"✅ Progress saved: {progress['sent_count']} emails sent")
    except Exception as e:
        print(f"❌ Error saving progress: {e}")

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
        server.quit()
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
    
    # Load progress
    progress = load_progress()
    print(f"Previous emails sent: {progress['sent_count']}")
    print(f"Total unique emails sent: {len(progress['all_sent_emails'])}")
    
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
    
    # Check if we've sent all emails
    if progress['sent_count'] >= len(emails_to_send):
        print("All emails have been sent! Consider updating your CSV with new leads.")
        return
    
    # Get next batch of emails
    start_index = progress['sent_count']
    batch = emails_to_send[start_index:start_index + BATCH_SIZE]
    
    if not batch:
        print("No more emails to send in this batch.")
        return
    
    print(f"\nProcessing batch {start_index//BATCH_SIZE + 1}: emails {start_index + 1} to {start_index + len(batch)}")
    
    delays = get_random_delays(len(batch), MIN_GAP_MINUTES)
    
    # Track emails sent in this batch
    batch_emails = []
    
    for i, (to_email, full_email) in enumerate(batch):
        try:
            subject, body = parse_full_email(full_email)
            print(f"Sending email {i + 1} to {to_email}")
            success = send_email(to_email, subject, body)
            status = "Success" if success else "Failed"
            
            with open(LOG_FILE, 'a') as log:
                log.write(f"Sent to {to_email} at {time.strftime('%Y-%m-%d %H:%M:%S')}: {status}\n")
            
            print(f"Email {i + 1}: {to_email} ({status})")
            
            # Track successful emails
            if success:
                batch_emails.append(to_email)
            
        except Exception as e:
            print(f"Error processing {to_email}: {e}")
            with open(LOG_FILE, 'a') as log:
                log.write(f"Error processing {to_email}: {e}\n")
        
        # Sleep for the random delay to next email (except last in batch)
        if i < len(batch) - 1:
            delay_seconds = delays[i] * 60
            print(f"Waiting {delays[i]} minutes before next email...")
            time.sleep(delay_seconds)
    
    # Update progress with new emails
    if batch_emails:
        progress['sent_count'] = start_index + len(batch)
        progress['last_batch'] = batch_emails
        progress['all_sent_emails'].extend(batch_emails)
        
        # Remove duplicates from all_sent_emails
        progress['all_sent_emails'] = list(set(progress['all_sent_emails']))
        
        # Save progress
        save_progress(progress)
    
    print(f"\nBatch complete! Sent {len(batch)} emails.")
    print(f"Total emails sent so far: {progress['sent_count']}")
    print(f"Total unique emails sent: {len(progress['all_sent_emails'])}")
    print(f"Remaining emails: {len(emails_to_send) - progress['sent_count']}")
    print("Next batch will be sent in 2 hours when GitHub Actions runs again.")

if __name__ == "__main__":
    main() 