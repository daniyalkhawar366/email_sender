import csv
import random
from openai import OpenAI

# IMPORTANT: Add your OpenAI API key here
client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")

# Houston-specific references for remodeling companies
HOUSTON_REFERENCES = [
    "Houston's infamous humidity and home maintenance",
    "surviving another Houston hurricane season",
    "Memorial Drive flooding aftermath",
    "Energy Corridor office renovations",
    "Galleria-area luxury home updates",
    "Heights historic home preservation",
    "Sugar Land custom kitchen trends",
    "Katy suburb bathroom makeovers",
    "NASA's precision engineering mindset",
    "Houston Rodeo organization skills",
    "Astros World Series attention to detail",
    "Texas heat and HVAC efficiency",
    "Houston traffic delays and project timelines",
    "Buffalo Bayou trail maintenance"
]

QUIRKY_SUBJECT_TEMPLATES = [
    "Why {} is exactly like your invoice workflow",
    "The strange connection between {} and construction billing",
    "How {} taught me about remodeling paperwork",
    "What {} and your accounting system have in common",
    "The weird parallel between {} and project invoices",
    "{} vs. your email-to-spreadsheet process",
    "Random thought: {} reminds me of your billing",
    "Odd observation about {} and invoice management"
]

def extract_company_specialty(about_text, company_name):
    """Extract what the company specializes in from about text"""
    if not about_text:
        return "remodeling and construction services"
    
    about_lower = about_text.lower()
    name_lower = company_name.lower()
    combined_text = f"{about_lower} {name_lower}"
    
    # Remodeling specialties
    specialties = {
        'kitchen remodeling': ['kitchen', 'cabinet', 'countertop', 'appliance'],
        'bathroom renovation': ['bathroom', 'bath', 'shower', 'vanity', 'tile'],
        'flooring services': ['floor', 'flooring', 'hardwood', 'tile', 'carpet', 'vinyl'],
        'roofing and exterior': ['roof', 'roofing', 'exterior', 'siding', 'gutter'],
        'painting services': ['paint', 'painting', 'interior', 'exterior'],
        'whole home renovation': ['whole home', 'complete', 'full renovation', 'addition'],
        'commercial remodeling': ['commercial', 'office', 'retail', 'business'],
        'custom home building': ['custom home', 'new construction', 'builder', 'luxury']
    }
    
    for specialty, keywords in specialties.items():
        if any(keyword in combined_text for keyword in keywords):
            return specialty
    
    return "home remodeling and construction"

def generate_personalized_email(name, email, about, website=""):
    """Generate SMYKM-style personalized email for remodeling companies"""
    
    # Extract company specialty
    specialty = extract_company_specialty(about, name)
    
    # Select Houston reference and subject line
    houston_ref = random.choice(HOUSTON_REFERENCES)
    subject_template = random.choice(QUIRKY_SUBJECT_TEMPLATES)
    subject_line = subject_template.format(houston_ref)
    
    prompt = f"""
Write a cold email in the EXACT SMYKM style from the example. This is for a remodeling/construction company in Houston.

COMPANY INFO:
- Name: {name}
- Email: {email}
- About: {about}
- Specialty: {specialty}
- Website: {website}

REQUIRED EMAIL STRUCTURE (follow this exactly):

1. SUBJECT LINE: "{subject_line}"

2. EMAIL BODY:
   - Casual opener: "Hi [Name]," followed by a non-salesy first sentence (like "We haven't met yet, but I'm [Your name]...")
   - Houston connection: Naturally mention something about Houston remodeling/construction scene
   - Transition question: Ask something quirky related to "{houston_ref}" (like the "closest Pilot/Flying J" style question)
   - Challenge: Identify their specific pain point (invoice processing from suppliers, managing project billing, tracking payments across multiple jobs)
   - Value proposition: Explain email-to-Google Sheets automation benefits for remodeling companies
   - Social proof: Reference other remodeling/construction companies who benefit from this
   - Casual close: Friendly request for a chat
   - Sign off with "Cheers!" and your name
   - P.S.: Answer to the quirky question

SPECIFIC REQUIREMENTS:
- Sound like you actually know the remodeling industry in Houston
- Reference specific pain points remodeling companies face:
  * Managing invoices from multiple suppliers (lumber, tile, fixtures, etc.)
  * Tracking costs across different job sites  
  * Dealing with change orders and additional materials
  * Organizing receipts for client billing
  * Managing subcontractor invoices

- Tone: Conversational, slightly quirky, professional but not corporate
- Include Houston-specific knowledge naturally
- Make it feel researched and personal to their business

- Your service: Automatically converts invoices from emails into organized Google Sheets for easy tracking and billing

OUTPUT FORMAT:
SUBJECT: [subject line]

BODY:
[complete email body]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error generating email for {name}: {str(e)}"

def process_all_companies(input_csv, output_csv, test_count=None):
    """Generate emails for all companies in the CSV"""
    
    print(f"🚀 Starting email generation from {input_csv}")
    
    try:
        # Read input CSV
        with open(input_csv, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            companies = list(reader)
        
        # Limit for testing
        if test_count:
            companies = companies[:test_count]
            print(f"🧪 TEST MODE: Processing first {test_count} companies")
        else:
            print(f"📊 Processing all {len(companies)} companies")
        
        # Process each company
        results = []
        successful_generations = 0
        
        for i, company in enumerate(companies, 1):
            name = company.get('Name', 'Unknown Company')
            email = company.get('Email', '')
            about = company.get('About', '')
            website = company.get('Website', '')
            
            print(f"\n{i}/{len(companies)}: Generating email for {name}")
            print(f"  📧 Email: {email}")
            print(f"  ℹ️  About: {about[:100]}..." if about else "  ⚠️  No about info")
            
            # Generate personalized email
            email_content = generate_personalized_email(
                name=name,
                email=email, 
                about=about,
                website=website
            )
            
            if not email_content.startswith("Error"):
                successful_generations += 1
                print(f"  ✅ Email generated successfully")
            else:
                print(f"  ❌ {email_content}")
            
            # Add to results
            result_row = company.copy()  # Keep all original columns
            result_row['GeneratedEmail'] = email_content
            results.append(result_row)
            
            # Small delay to respect API limits
            import time
            time.sleep(1)
        
        # Save results
        print(f"\n💾 Saving results to {output_csv}")
        with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
            if results:
                fieldnames = list(results[0].keys())
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
        
        # Summary
        print(f"\n🎉 EMAIL GENERATION COMPLETE!")
        print(f"📊 Total processed: {len(companies)}")
        print(f"✅ Successful generations: {successful_generations}")
        print(f"💾 Results saved to: {output_csv}")
        
        # Show first email as sample
        if results and successful_generations > 0:
            print(f"\n📧 SAMPLE EMAIL (for {results[0]['Name']}):")
            print("=" * 60)
            print(results[0]['GeneratedEmail'])
            print("=" * 60)
            
    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_csv}")
        print("Run the company info scraper first to create this file!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def preview_single_email(name, about, email="test@company.com"):
    """Generate and preview a single email for testing"""
    print(f"\n🔍 PREVIEW EMAIL for {name}")
    print("=" * 60)
    
    email_content = generate_personalized_email(
        name=name,
        email=email,
        about=about
    )
    
    print(email_content)
    print("=" * 60)

if __name__ == "__main__":
    # Configuration
    input_filename = "houston_remodeling_contacts_with_info.csv"  # Output from scraper
    output_filename = "houston_remodeling_with_emails.csv"        # Final output
    
    print("📧 Houston Remodeling Email Generator")
    print("=" * 50)
    
    # Test with sample first
    print("Testing with sample company...")
    preview_single_email(
        name="Premier Kitchen Remodeling",
        about="Premier Kitchen Remodeling specializes in high-end kitchen renovations in Houston's Memorial and River Oaks areas. We work with luxury homeowners to create custom kitchen spaces with premium materials and appliances. Our team handles everything from design to installation.",
        email="info@premierkitchens.com"
    )
    
    # Ask user what they want to do
    print("\nOptions:")
    print("1. Test with first 3 companies")
    print("2. Test with first 10 companies") 
    print("3. Generate emails for ALL companies")
    print("4. Custom test amount")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        process_all_companies(input_filename, "test_3_companies.csv", test_count=3)
    elif choice == "2":
        process_all_companies(input_filename, "test_10_companies.csv", test_count=10)
    elif choice == "3":
        estimated_cost = len(open(input_filename).readlines()) * 0.15  # Rough estimate
        confirm = input(f"Generate emails for ALL companies? Estimated cost: ${estimated_cost:.2f} (y/n): ")
        if confirm.lower() == 'y':
            process_all_companies(input_filename, output_filename)
    elif choice == "4":
        test_amount = int(input("How many companies to test?: "))
        process_all_companies(input_filename, f"test_{test_amount}_companies.csv", test_count=test_amount)
    
    print("\n🎯 Next step: Review the generated emails and use them for your outreach campaign!")