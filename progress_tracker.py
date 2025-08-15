import json
import os

PROGRESS_FILE = 'email_progress.json'

def load_progress():
    """Load progress from file."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'sent_count': 0, 'last_batch': []}

def save_progress(progress):
    """Save progress to file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f)

def get_next_batch(emails_to_send, batch_size, progress):
    """Get the next batch of emails to send."""
    sent_count = progress['sent_count']
    
    # Calculate start index for next batch
    start_index = sent_count
    
    # Get next batch
    batch = emails_to_send[start_index:start_index + batch_size]
    
    return batch, start_index

def update_progress(progress, batch, start_index):
    """Update progress after sending batch."""
    progress['sent_count'] = start_index + len(batch)
    progress['last_batch'] = [email[0] for email in batch]  # Store email addresses
    save_progress(progress) 