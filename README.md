# CEU Certificate Generator

**Production-ready system for bulk-generating branded PDF CEU certificates from CSV attendee data.**

Perfect for healthcare organizations, training providers, and continuing education programs. Generates professional certificates with consistent branding and proper naming conventions.

## Features

- **Bulk Generation** - Process hundreds of certificates in minutes
- **Professional Templates** - Healthcare-grade branded certificates  
- **Smart Organization** - Auto-creates folders by event name/date
- **Easy Customization** - Simple HTML/CSS template editing
- **CSV Integration** - Works with Salesforce exports and standard CSV
- **Error Handling** - Validates data and reports issues clearly
- **Cross Platform** - Windows, Mac, Linux support

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/cert-automation.git
cd cert-automation

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Install wkhtmltopdf
**Windows:**
```bash
winget install wkhtmltopdf.wkhtmltox
```

**Mac:**
```bash
brew install wkhtmltopdf
```

**Linux:**
```bash
sudo apt-get install wkhtmltopdf
```

### 3. Generate Certificates
```bash
# Use the sample data
python generate_certs.py --csv attendees_salesforce_format.csv

# Or your own CSV file
python generate_certs.py --csv your_event.csv
```

## 📊 CSV Format

Your CSV must include these columns (Salesforce export format supported):

| Column | Description |
|---------------------|
| `SubscriberKey` | Optional | Duplicate of EmailAddress (Salesforce format) |
| `EmailAddress` | Attendee email address |
| `FirstName` | Attendee first name |
| `LastName` | Attendee last name |
| `Credentials` | Optional | Professional credentials (LCSW, PhD, etc.) |
| `EventTitle` | Name of the event/training |
| `EventDate` | Date of the event |

### Example CSV:
```csv
SubscriberKey,EmailAddress,FirstName,LastName,Credentials,EventTitle,EventDate
jane.doe@email.com,jane.doe@email.com,Jane,Doe,LCSW,"Mental Health Training","January 17 2025"
```

## Output Structure

```
output/
└── EventName_EventDate/
    ├── Doe-Jane-Mental_Health_Training-January_17_2025.pdf
    ├── Smith-John-Mental_Health_Training-January_17_2025.pdf
    └── ...
```

## Customizing Templates

1. Edit `cert_template.html` to modify the certificate design
2. Uses Jinja2 templating:
   - `{{ FirstName }}` - Attendee's first name
   - `{{ LastName }}` - Attendee's last name  
   - `{{ Credentials }}` - Professional credentials
   - `{{ EventTitle }}` - Event name
   - `{{ EventDate }}` - Event date
   - `{% if Credentials %}...{% endif %}` - Conditional display

## 🔧 Advanced Usage

### Command Line Options
```bash
# Custom CSV file
python generate_certs.py --csv my_event.csv

# Custom template
python generate_certs.py --template my_template.html

# Custom output folder
python generate_certs.py --output /path/to/output

# Combine options
python generate_certs.py --csv event.csv --template special.html --output event_certs
```

### Batch Processing Multiple Events
```bash
# Event 1
python generate_certs.py --csv jan_event.csv

# Event 2  
python generate_certs.py --csv feb_event.csv

# Each gets its own output folder automatically
```

##  Development

### Project Structure
```
cert-automation/
├── generate_certs.py           # Main script
├── cert_template.html          # Certificate template
├── requirements.txt            # Python dependencies
├── attendees_salesforce_format.csv  # Example Salesforce format
├── attendees_test.csv          # Example standard format
├── generate_certificates.bat   # Windows batch script
├── generate_certificates.sh    # Unix shell script
└── output/                     # Generated PDFs (auto-created)
```

### Requirements
- Python 3.8+
- wkhtmltopdf
- pandas, jinja2, pdfkit (installed via requirements.txt)

## Troubleshooting

**"wkhtmltopdf not found"**
- Ensure wkhtmltopdf is installed and in PATH
- Windows: Restart terminal after installation

**"No columns to parse from file"**
- Check CSV file format and encoding
- Ensure file has proper headers and data

**PDF generation fails**
- Verify template HTML syntax
- Check that all template variables exist in CSV

**Virtual environment issues**
- Always activate venv before running: `.\.venv\Scripts\Activate.ps1`

## For Regular Use

### Every New Event:
1. **Activate environment:** `.\.venv\Scripts\Activate.ps1`
2. **Add your CSV file** with attendee data
3. **Run:** `python generate_certs.py --csv your_file.csv`
4. **Find PDFs** in `output/[EventName]/`

### Tips:
- Test with 2-3 attendees first
- Keep event titles in quotes if they contain commas
- Each event gets its own folder automatically
- Backup your templates before major changes

## License

MIT License - see LICENSE file for details

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

**Made for healthcare professionals who need reliable, professional certificate generation.** 🏥✨ 
