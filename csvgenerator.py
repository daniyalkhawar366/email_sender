import pandas as pd

# More scraped leads with emails
new_contacts = [
    {"Full Name": "Jenni Edwards", "Company Name": "Braden Real Estate Group", "Instagram URL": "https://www.instagram.com/jenniedwards_", "Email Address": "", "Phone Number": ""},  # Skipped (email not visible)
    {"Full Name": "", "Company Name": "Renee Realty Group", "Instagram URL": "https://www.instagram.com/d_.w", "Email Address": "", "Phone Number": "281-815-0945"},  # Skipped (email not shown)
    {"Full Name": "Sonsire Gonzalez", "Company Name": "Sunshine Realtors", "Instagram URL": "https://www.instagram.com/sonsire_florida_realtor", "Email Address": "sonsiregonzalez@gmail.com", "Phone Number": "772-200-9112"},
    {"Full Name": "Kimberly Mata", "Company Name": "", "Instagram URL": "https://www.instagram.com/kimberlymata_realtor", "Email Address": "", "Phone Number": ""},  # Skipped (no email)
    {"Full Name": "Property Fix Houston LLC", "Company Name": "Property Fix Houston", "Instagram URL": "https://www.instagram.com/propertyfixhoustonllc", "Email Address": "propertyfixhouston@gmail.com", "Phone Number": "832-629-8292"},
    {"Full Name": "Carnisha Emanuel", "Company Name": "", "Instagram URL": "https://www.instagram.com/carnishajoi", "Email Address": "", "Phone Number": ""},  # Skipped (no email)
    {"Full Name": "Kia Nichol", "Company Name": "", "Instagram URL": "https://www.instagram.com/kianichol", "Email Address": "", "Phone Number": ""},  # Skipped (no email)
]

# Filter only those with emails
new_contacts = [entry for entry in new_contacts if entry["Email Address"].strip() != ""]

# Convert to DataFrame
new_df = pd.DataFrame(new_contacts)

# CSV path
csv_path = "houston_construction_leads.csv"

# Append or create the CSV
try:
    existing_df = pd.read_csv(csv_path)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
except FileNotFoundError:
    combined_df = new_df

# Save updated list
combined_df.to_csv(csv_path, index=False)

print("✅ New leads with email addresses added to 'houston_construction_leads.csv'")
