#!/usr/bin/env python3
"""
Improved Email Generator with Better Reply Rate Strategies
Incorporates: Weirder trivia, urgency, conversational tone, social proof, specific CTAs
"""

import csv
import random

# Weird Houston construction trivia (much weirder than before)
WEIRD_TRIVIA = [
    "What Houston construction worker is rumored to have a pet armadillo that approves building permits?",
    "Which Houston contractor allegedly keeps a ghost accountant in their filing cabinet?",
    "What strange creature is said to mix concrete with moonshine in Houston's underground tunnels?",
    "Which Houston construction site is rumored to be haunted by a poltergeist plumber?",
    "What mutant armadillo is believed to hide blueprints under Houston skyscrapers?",
    "Which Houston builder allegedly has a cursed coffee mug that powers their weirdest construction tools?",
    "What tap-dancing turtle is said to dance on rooftops during Houston rainstorms?",
    "Which Houston contractor is rumored to have a paper-eating possum that chews through paperwork?",
    "What sneaky catfish allegedly approves building permits in secret?",
    "Which Houston construction worker has a drunken goblin that mixes their concrete?"
]

TRIVIA_ANSWERS = [
    "A construction worker named Bob with a pet armadillo named Permit Pete!",
    "The ghost accountant named Numbers McGee!",
    "A drunken goblin named Concrete Carl!",
    "A poltergeist plumber named Pipe Phantom!",
    "A mutant armadillo named Blueprint Barry!",
    "A cursed coffee mug named Java Jinx!",
    "A tap-dancing turtle named Raindance Rex!",
    "A paper-eating possum named Document Devourer!",
    "A sneaky catfish named Permit Percy!",
    "A drunken goblin named Moonshine Mike!"
]

# Urgency and curiosity hooks
URGENCY_HOOKS = [
    "I've got a theory about why 73% of Houston contractors lose money on invoicing...",
    "Listen, I know this sounds crazy, but I just discovered why Houston builders waste 15+ hours weekly...",
    "Here's something wild: 8 out of 10 Houston contractors I talk to have the same invoicing nightmare...",
    "I've been studying Houston construction companies and found a pattern that's costing them millions...",
    "This might sound insane, but I think I know why Houston contractors can't scale past 10 employees...",
    "Listen, I've got a confession: I've been stalking Houston construction companies (not in a creepy way)...",
    "Here's what's keeping me up at night: Why do Houston contractors love losing money on invoicing?",
    "I've got a theory that's either brilliant or completely bonkers about Houston construction invoicing...",
    "Listen, I know this is random, but I've been obsessed with Houston contractors' invoicing problems...",
    "Here's something that's been bugging me: Why do Houston builders love manual data entry so much?"
]

# Social proof statements
SOCIAL_PROOF = [
    "We just helped a Houston contractor save 22 hours last week alone",
    "Last month, we saved a Houston builder 87 hours on invoice processing",
    "A Houston contractor we helped went from 15 hours of invoicing to 2 hours weekly",
    "We just onboarded a Houston company that's saving $12,000 monthly on invoicing",
    "A Houston builder we helped increased their project efficiency by 35%",
    "Last week, we helped a Houston contractor process 200 invoices in 3 hours instead of 15",
    "A Houston company we helped went from 90% manual work to 90% automated",
    "We just saved a Houston contractor from hiring 2 additional admin staff",
    "A Houston builder we helped went from 3 days to 3 hours for monthly invoicing",
    "We just helped a Houston contractor recover $45,000 in lost invoice data"
]

# Specific CTAs
SPECIFIC_CTAS = [
    "Want to see how we do it? I can show you in 3 minutes",
    "Curious how this works? I can demo it in under 5 minutes",
    "Want to see the magic? I can walk you through it in 3 minutes",
    "Interested in seeing this in action? I can show you in 4 minutes",
    "Want to see how it works? I can demo it in 3 minutes",
    "Curious about the process? I can walk you through it in 5 minutes",
    "Want to see the system? I can show you in 3 minutes",
    "Interested in a demo? I can walk you through it in 4 minutes",
    "Want to see it work? I can show you in 3 minutes",
    "Curious about the solution? I can demo it in 5 minutes"
]

def generate_improved_email(company_name, contact_name=""):
    """Generate an improved email with better reply rate strategies."""
    
    # Select random elements
    trivia = random.choice(WEIRD_TRIVIA)
    trivia_answer = TRIVIA_ANSWERS[WEIRD_TRIVIA.index(trivia)]
    urgency_hook = random.choice(URGENCY_HOOKS)
    social_proof = random.choice(SOCIAL_PROOF)
    cta = random.choice(SPECIFIC_CTAS)
    
    # Generate personalized subject
    animal_names = ["Armadillo", "Goblin", "Catfish", "Possum", "Turtle", "Phantom", "Ghost", "Mutant", "Cursed", "Weird"]
    animal = random.choice(animal_names)
    subject = f"{animal} {contact_name if contact_name else 'Friend'}'s Favorite {company_name}"
    
    # Generate email body
    email_body = f"""Subject: {subject}

Hi {contact_name if contact_name else company_name.split()[0]},

{urgency_hook}

Here it is: {trivia}

While you ponder that, here's why I'm reaching out: AlbyTech automatically scans your emails for invoices, extracts data with 95% accuracy, and populates Google Sheets in real-time. This saves contractors 15+ hours weekly and boosts revenue by 20% per project.

{social_proof}

AlbyTech's edge: Seamless Google Sheets integration, 90% error reduction through AI validation, real-time analytics, and customizable reporting for superior financial control.

{cta}

Cheers,
Daniyal

(P.S. the answer is... {trivia_answer})"""

    return subject, email_body

def generate_csv_with_improved_emails(input_csv, output_csv):
    """Generate a new CSV with improved emails."""
    
    with open(input_csv, mode='r', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        
        # Determine field names based on input CSV
        if 'Company' in reader.fieldnames:
            fieldnames = ['Company', 'Email Address', 'Full Email']
        elif 'Name' in reader.fieldnames:
            fieldnames = ['Name', 'Email Address', 'Full Email']
        else:
            fieldnames = ['Company', 'Email Address', 'Full Email']
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            company_name = row.get('Company', row.get('Name', 'Unknown Company'))
            contact_name = row.get('Contact', row.get('Name', ''))
            email_address = row.get('Email Address', row.get('Email', ''))
            
            if company_name and email_address:
                subject, body = generate_improved_email(company_name, contact_name)
                
                writer.writerow({
                    'Company': company_name,
                    'Email Address': email_address,
                    'Full Email': body
                })
                
                print(f"Generated email for: {company_name}")

if __name__ == "__main__":
    # Example usage
    input_file = "houston_construction_leads.csv"  # Your input file
    output_file = "smykm_emails_account2.csv"     # Output for second account
    
    print("Generating improved emails with better reply rate strategies...")
    generate_csv_with_improved_emails(input_file, output_file)
    print(f"✅ Improved emails saved to: {output_file}")
    print("📧 These emails include:")
    print("   - Weirder, more memorable trivia")
    print("   - Urgency and curiosity hooks")
    print("   - Conversational, casual tone")
    print("   - Specific social proof")
    print("   - Clear, specific CTAs")
