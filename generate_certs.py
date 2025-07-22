import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
import re
import argparse
import sys
from datetime import datetime

def clean_filename(s):
    """Make a safe, readable filename segment."""
    return re.sub(r'[^a-zA-Z0-9]+', '_', str(s).strip())

def validate_csv(csv_file):
    """Validate that CSV has required columns."""
    required_columns = ['FirstName', 'LastName', 'EmailAddress', 'EventTitle', 'EventDate']
    # SubscriberKey is optional but commonly present
    try:
        df = pd.read_csv(csv_file)
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Error: Missing required columns in CSV: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return False
        
        # Check if we have data
        if len(df) == 0:
            print("Error: CSV file is empty (no data rows)")
            return False
            
        print(f"✓ CSV validated: {len(df)} attendees found")
        return True
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False

def main(csv_file, template_file, output_folder):
    # Validate inputs
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return False
    
    if not os.path.exists(template_file):
        print(f"Error: Template file '{template_file}' not found.")
        return False
    
    if not validate_csv(csv_file):
        return False

    # Setup
    print(f"Reading attendee data from: {csv_file}")
    print(f"Using template: {template_file}")
    
    try:
        env = Environment(loader=FileSystemLoader('.'))
        df = pd.read_csv(csv_file).fillna('')
        template = env.get_template(template_file)
    except Exception as e:
        print(f"Error setting up template or reading CSV: {e}")
        return False

    # Create output folder
    if output_folder == 'output':
        # Auto-create folder based on event name from first row
        event_name = clean_filename(df.iloc[0]['EventTitle']) if 'EventTitle' in df.columns else 'Event'
        event_date = clean_filename(df.iloc[0]['EventDate']) if 'EventDate' in df.columns else datetime.now().strftime('%Y%m%d')
        output_folder_event = f"output/{event_name}_{event_date}"
    else:
        output_folder_event = output_folder
    
    os.makedirs(output_folder_event, exist_ok=True)
    print(f"Output directory: {output_folder_event}")

    # Generate certificates
    success_count = 0
    total_count = len(df)
    
    for idx, row in df.iterrows():
        try:
            context = row.to_dict()
            html = template.render(**context)

            # Create filename
            last = clean_filename(row['LastName'])
            first = clean_filename(row['FirstName'])
            event = clean_filename(row['EventTitle'])
            date = clean_filename(row['EventDate'])
            safe_name = f"{last}-{first}-{event}-{date}.pdf"
            pdf_path = os.path.join(output_folder_event, safe_name)

            # Generate PDF with Windows wkhtmltopdf path
            config = None
            wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            if os.path.exists(wkhtmltopdf_path):
                config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            
            pdfkit.from_string(html, pdf_path, options={
                'page-size': 'Letter',
                'margin-top': '0in',
                'margin-right': '0in',
                'margin-bottom': '0in',
                'margin-left': '0in',
                'encoding': "UTF-8",
                'enable-local-file-access': None
            }, configuration=config)

            print(f"✓ Created: {safe_name}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error creating certificate for {row.get('FirstName', '')} {row.get('LastName', '')}: {e}")

    print(f"\nCompleted! Generated {success_count}/{total_count} certificates")
    print(f"All certificates saved in: {output_folder_event}/")
    return success_count > 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bulk-generate CEU certificates as PDFs.')
    parser.add_argument('--csv', default='attendees.csv', help='Path to attendee CSV file (default: attendees.csv)')
    parser.add_argument('--template', default='cert_template.html', help='Path to HTML template file (default: cert_template.html)')
    parser.add_argument('--output', default='output', help='Output folder (default: auto-creates folder based on event)')
    
    args = parser.parse_args()
    
    print("=== CEU Certificate Generator ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = main(args.csv, args.template, args.output)
    
    if not success:
        sys.exit(1) 