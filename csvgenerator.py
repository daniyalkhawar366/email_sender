import pandas as pd

# Final contact data
final_data = [
    {"Full Name": "", "Company Name": "Reyes Perfect Remodeling", "Instagram URL": "", "Email Address": "", "Phone Number": "8328330158"},
    {"Full Name": "", "Company Name": "Gr Remodeling", "Instagram URL": "", "Email Address": "lilidimples26@gmail.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "", "Instagram URL": "", "Email Address": "jt3ti@aol.com", "Phone Number": "2108453083"},
    {"Full Name": "", "Company Name": "", "Instagram URL": "", "Email Address": "carringtonrealestate2024@gmail.com", "Phone Number": "346352XXXX"},  # Redact or correct if unknown
    {"Full Name": "", "Company Name": "Reborn Remodeling", "Instagram URL": "", "Email Address": "reborn.remodeling@gmail.com", "Phone Number": "7139247389"},
    {"Full Name": "", "Company Name": "Urban Remodeling Services Inc", "Instagram URL": "", "Email Address": "morrisarrevalo@yahoo.com", "Phone Number": "2817488610"},
    {"Full Name": "", "Company Name": "Garcia Construction and Remodeling", "Instagram URL": "", "Email Address": "sagarcia2021me@gmail.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "Advanced Solutions Home Improvement & Remodeling", "Instagram URL": "", "Email Address": "ashir.llc@icloud.com", "Phone Number": "3463149278"},
    {"Full Name": "", "Company Name": "HG Luxury Homes", "Instagram URL": "", "Email Address": "hgluxuryhomes@gmail.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "Handyman Houston Remodeling", "Instagram URL": "", "Email Address": "handymanhoustonremodeling@gmail.com", "Phone Number": ""},
    {"Full Name": "Jackie Venters", "Company Name": "True Remodeling & Renovations", "Instagram URL": "", "Email Address": "jackieventers.realtor@gmail.com", "Phone Number": "8322356240"},
    {"Full Name": "", "Company Name": "Houston1 Remodeling LLC", "Instagram URL": "", "Email Address": "nevresudinhaskic@yahoo.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "", "Instagram URL": "", "Email Address": "jasonbpenberthy@gmail.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "David's Construction & Homes Remodeling LLC", "Instagram URL": "", "Email Address": "", "Phone Number": ""},
    {"Full Name": "Hector Rodriguez", "Company Name": "HR Remodeling", "Instagram URL": "", "Email Address": "hector.s.rodriguez1@gmail.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "TH Construction & Remodeling", "Instagram URL": "", "Email Address": "thremodelinghouston@gmail.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "David Remodeling", "Instagram URL": "", "Email Address": "dconstructionandremodeling@gmail.com", "Phone Number": "8408412569"},
    {"Full Name": "", "Company Name": "Apka Ghar", "Instagram URL": "", "Email Address": "apka-ghar@outlook.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "Adolfo & Son's Remodeling", "Instagram URL": "", "Email Address": "", "Phone Number": "2817162907"},
    {"Full Name": "Jeremy Howard", "Company Name": "Lake Point Remodeling", "Instagram URL": "", "Email Address": "", "Phone Number": ""},
    {"Full Name": "", "Company Name": "McCarson Homes LLC", "Instagram URL": "", "Email Address": "mccarsonhomes281@gmail.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "Torres Remodeling & Painting", "Instagram URL": "", "Email Address": "", "Phone Number": ""},
    {"Full Name": "", "Company Name": "Flores Drywall & Painting", "Instagram URL": "", "Email Address": "floresdrywallpainting@gmail.com", "Phone Number": ""},
    {"Full Name": "", "Company Name": "YOA Remodeling", "Instagram URL": "", "Email Address": "yoaremodeling@gmail.com", "Phone Number": "8326141672"},
    {"Full Name": "Jacob Guzman", "Company Name": "J. Guzman General Remodeling Services", "Instagram URL": "", "Email Address": "jacoboguzman49@gmail.com", "Phone Number": "2819030420"},
    {"Full Name": "Carlos Guerrero", "Company Name": "", "Instagram URL": "", "Email Address": "guerrero.saint@yahoo.com", "Phone Number": "8322350283"},
    {"Full Name": "", "Company Name": "Global Deco USA Corp.", "Instagram URL": "", "Email Address": "globaldecousa@yahoo.com", "Phone Number": "8326777828"},
]

# Convert to DataFrame
final_df = pd.DataFrame(final_data)

# File path
csv_path = "houston_remodeling_contacts.csv"

# Append or create CSV
try:
    existing_df = pd.read_csv(csv_path)
    combined_df = pd.concat([existing_df, final_df], ignore_index=True)
except FileNotFoundError:
    combined_df = final_df

# Save updated file
combined_df.to_csv(csv_path, index=False)

print("Final contacts appended successfully.")
