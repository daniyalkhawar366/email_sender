import csv
import random
from faker import Faker

fake = Faker()

# Expanded template components for more uniqueness
WEIRD_SUBJECTS = [
    "Why your invoices belong in the Houston Zoo",
    "Paperwork alligators spotted in your accounting department",
    "Your stapler just unionized - here's why",
    "NASA's secret weapon for construction paperwork",
    "Houston humidity + your invoices = this disaster",
    "Your filing cabinet called - it's quitting",
    "3 raccoons stole your last invoice (true story)",
    "The hidden cost of manual invoicing in Texas heat",
    "Why your email inbox needs a superhero cape",
    "Invoice chaos: The Houston builder's silent killer",
    "From Bayou City blues to automated bliss",
    "Your paperwork is plotting a rebellion - act now",
    "Houston, we have an invoice problem",
    "Tame your wild invoices before they bite back"
]

ANIMALS = [
    "Bengal", "Siamese", "Persian", "Labrador", "Golden Retriever", "Alligator", "Raccoon", "Panda", "Koala", "Eagle",
    "Tiger", "Lion", "Elephant", "Giraffe", "Zebra", "Monkey", "Parrot", "Dolphin", "Shark", "Octopus",
    "Flamingo", "Penguin", "Bear", "Wolf", "Fox", "Deer", "Rabbit", "Squirrel", "Hedgehog", "Owl"
]

TRIVIA = [
    {"q": "What animal is rumored to secretly control Houston's construction cranes?", "a": "A mischievous raccoon"},
    {"q": "Which bizarre creature is said to hide blueprints under Houston skyscrapers?", "a": "A mutant armadillo"},
    {"q": "What odd entity is believed to rewrite invoices with invisible ink in Houston?", "a": "A ghost accountant"},
    {"q": "Which peculiar being is thought to guard the oldest nail in Houston buildings?", "a": "A one-eyed owl"},
    {"q": "What strange creature is rumored to chew through paperwork in Houston offices?", "a": "A paper-eating possum"},
    {"q": "Which weird figure is said to dance on rooftops during Houston rainstorms?", "a": "A tap-dancing turtle"},
    {"q": "What bizarre object is believed to power Houston's weirdest construction tools?", "a": "A cursed coffee mug"},
    {"q": "Which odd critter is rumored to approve building permits in secret?", "a": "A sneaky catfish"},
    {"q": "What peculiar spirit is thought to haunt Houston's unfinished projects?", "a": "A poltergeist plumber"},
    {"q": "Which strange entity is said to mix concrete with moonshine in Houston?", "a": "A drunken goblin"}
]

OPENING_VARIATIONS = [
    "We haven't met yet, but I'm Daniyal and I run AlbyTech. When I saw {company}'s impressive projects around Houston, I had to drop you a line of some fun trivia.",
    "I'm Daniyal and I run AlbyTech. While researching top construction firms in Houston, your company {company} stood out, so here's some interesting trivia.",
    "I'm Daniyal and I run AlbyTech. I came across {company} and couldn't resist sharing this bit of trivia with you.",
    "I'm Daniyal and I run AlbyTech. Your {company} projects in Houston caught my eye, prompting me to share this trivia.",
    "I'm Daniyal and I run AlbyTech. Spotting {company}'s work in the Houston area made me think you'd enjoy this trivia.",
    "I'm Daniyal and I run AlbyTech. After seeing {company}'s contributions to Houston's skyline, I wanted to share some trivia.",
    "I'm Daniyal and I run AlbyTech. Your {company} caught my attention in Houston searches, so here's a trivia tidbit.",
    "I'm Daniyal and I run AlbyTech. Impressed by {company}'s Houston projects, I thought I'd kick off with some trivia.",
    "I'm Daniyal and I run AlbyTech. Discovering {company} inspired me to reach out with this fun trivia.",
    "I'm Daniyal and I run AlbyTech. {company}'s presence in Houston made me want to share this intriguing trivia."
]

VALUE_PROP_VARIATIONS = [
    "While that percolates, the real reason I'm reaching out is to chat about AlbyTech. Our automation intelligently scans incoming emails for invoices, extracts key data with 95% accuracy, and automatically populates your Google Sheets—saving up to 15 hours per week, boosting per-project revenue by 20%, though scaling manually is tough.",
    "As that trivia sinks in, here's why I'm emailing: At AlbyTech, we specialize in pulling invoices directly from your email inbox, parsing details automatically, and syncing them seamlessly to Google Sheets with 95% precision, freeing up 15 hours weekly and increasing efficiency by 20% or more—challenging at your scale without help.",
    "While you ponder that, the main point is AlbyTech's solution: It monitors emails for invoices, uses AI to extract and validate data at 95% accuracy, then writes everything to customized Google Sheets, saving 15+ hours per week and lifting revenue per transaction by 20%, though hard to implement at scale.",
    "As that settles, let's get to it: AlbyTech automates by detecting invoice attachments or bodies in emails, accurately extracting fields like amounts and dates (95% rate), and auto-updating Google Sheets, which saves teams 15 hours weekly and boosts project revenue 20%—tough to achieve alone at scale.",
    "While that trivia brews, here's the scoop: Our AlbyTech tool scans emails for incoming invoices, pulls out critical info with 95% accuracy via smart parsing, and directly inputs it into your Google Sheets setup, cutting 15 hours of manual work per week and raising efficiency by 20% or more, despite scaling challenges.",
    "As you think on that, the reason for this email is AlbyTech: It automatically identifies invoices in emails, extracts data precisely (95% accuracy), and populates Google Sheets in real-time, delivering 15 hours of weekly savings and 20% revenue uplift per project—complex to scale without expertise.",
    "While that question lingers, I'm here about AlbyTech: Our system fetches invoices from emails, employs advanced extraction for 95% accurate data capture, and auto-fills Google Sheets, saving up to 15 hours a week and enhancing per-transaction revenue by 20%, though scaling poses hurdles.",
    "As that percolates, the core message is AlbyTech's automation: Scanning emails for invoices, pulling details with 95% precision, and seamlessly adding to Google Sheets to save 15 hours weekly, increase project revenue 20%, but difficult to scale independently.",
    "While you mull over the trivia, here's why I reached out: AlbyTech grabs invoices from your email stream, accurately extracts (95%) and transfers data to Google Sheets automatically, freeing 15 hours per week and boosting revenue by 20% per project—scaling is the tricky part.",
    "As that trivia takes hold, let's discuss AlbyTech: It detects and processes invoices in emails, achieves 95% accuracy in data extraction, and updates Google Sheets effortlessly, resulting in 15-hour weekly savings and 20% efficiency gains, though tough at larger scales."
]

CHALLENGE_VARIATIONS = [
    "That's exactly what we do at AlbyTech. Building on your current processes, our tool provides seamless Google Sheets integration with real-time analytics, slashes manual errors by 90%, and offers customizable reporting to supercharge your financial workflow.",
    "AlbyTech excels here: We integrate directly with Google Sheets for instant updates, reduce errors by 90% through smart validation, and include tailored dashboards for better oversight—all while handling the email-to-sheet pipeline effortlessly.",
    "With AlbyTech, you'll get full Google Sheets compatibility, 90% error reduction via automated checks, real-time analytics, and flexible reporting options designed specifically to optimize invoice management and save time.",
    "Our AlbyTech difference: Seamless syncing to Google Sheets, cutting errors 90% with AI verification, providing live analytics, and custom reports to streamline your entire invoicing process from email to insights.",
    "AlbyTech delivers: Direct Google Sheets integration, 90% fewer mistakes through precise extraction, real-time data visualization, and personalized reporting to enhance decision-making and efficiency.",
    "What sets AlbyTech apart: Effortless Google Sheets linkage, 90% error minimization with advanced parsing, on-the-fly analytics, and bespoke reports tailored to your construction invoicing needs.",
    "AlbyTech's edge: Integrates smoothly with Google Sheets, drops errors by 90% using intelligent automation, offers real-time monitoring, and customizable reports for superior financial control.",
    "Experience AlbyTech: Google Sheets auto-population, 90% accuracy boost reducing errors, live analytics feeds, and report customization to transform your invoice handling.",
    "AlbyTech shines with: Complete Google Sheets support, 90% error cut via robust checks, real-time analytic tools, and flexible reporting to elevate your workflow.",
    "Choose AlbyTech for: Seamless Sheets integration, 90% less errors through smart tech, instant analytics, and tailored reporting to maximize your time savings."
]

def generate_email(name, company, email):
    """Generate unique SMYKM-style email body and subject for auto-emailing"""
    pet_name = fake.first_name()
    animal = random.choice(ANIMALS)
    subject = f"Subject: {pet_name} the {animal}'s Favorite {company}"
    
    trivia = random.choice(TRIVIA)
    opening = random.choice(OPENING_VARIATIONS).format(name=name.split()[0] if name and ' ' in name else name or 'Friend', company=company)
    value_prop = random.choice(VALUE_PROP_VARIATIONS)
    challenge = random.choice(CHALLENGE_VARIATIONS)
    
    email_body = f"Hi {name.split()[0] if name and ' ' in name else name or 'Friend'},\n\n{opening}\n\nHere it is: {trivia['q']}\n\n{value_prop}\n\n{challenge}\n\nIf you're up for a chat about this, I'd be thrilled to find a time whenever is convenient for you.\n\nCheers,\nDaniyal\n\n(P.S. the answer is... {trivia['a']}!!)"
    
    return subject, email_body

def process_leads(input_csv, output_csv):
    """Process leads with unique emails including company, email, and full email content"""
    with open(input_csv, mode='r', encoding='utf-8', errors='replace') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['Company', 'Email Address', 'Full Email'])
        writer.writeheader()

        row_count = 0
        for row in reader:
            row_count += 1
            email_address = row.get('Email Address')
            if not email_address:
                print(f"Row {row_count}: Skipping due to missing email: {row}")
                continue
            
            full_name = row.get('Full Name', '')
            company_name = row.get('Company Name', 'Your Company')
            name = full_name if full_name else company_name.split()[0] if company_name and ' ' in company_name else company_name or 'Friend'
            
            print(f"Processing row {row_count}: Company={company_name}, Name={name}, Email={email_address}")  # Debug print
            
            subject, body = generate_email(
                name=name,
                company=company_name,
                email=email_address
            )
            
            writer.writerow({
                'Company': company_name,
                'Email Address': email_address,
                'Full Email': f"{subject}\n\n{body}"
            })

if __name__ == "__main__":
    try:
        process_leads("houston_remodeling_contacts.csv", "smykm_emails.csv")
    except Exception as e:
        print(f"An error occurred: {e}")