
# Netbox CSV Export

This script is meant to export information from Netbox into CSV files and email them as a ZIP archive. It is intended to provide a backup source of information if the Netbox server is unaccessible.

## Prerequisites

- Export templates are used to specify what information is included and must be created in advance.
- Template names are case-sensitive and must match the names listed in the templates dictionary at the top of the script.

## Usage

1. Clone repository into a chosen directory.
```
git clone https://github.com/b-sheedy/Netbox-Export.git .
```

2. Create new virtual environment in chosen directory.
```
python3 -m venv .venv
```

3. Activate virtual environment.
```
source .venv/bin/activate
```

4. Install requests and python-dotenv libraries, then deactivate the virtual environment.
```
pip install requests python-dotenv
deactivate
```

5. Create .env file based on below template.
```Dotenv
netbox_token = API token for Netbox
netbox_url = Netbox URL
mail_server = SMTP server for emailing ZIP file
email_from = From email address
email_to = To email address(es)
```

6. Modify .env permissions to restrict access to root.
```
chmod 600 .env
```

7. Create export templates within Netbox. Five examples are included in the templates folder. The template name should match the file name and the file contents should be entered into the template code field. If creating your own templates, make sure to add the name and API path to the templates dictionary in the script as shown.

8. Add script to crontab if desired. Example below will run every Sunday at 5:00 AM.
```
crontab -e
00 05 * * 0    /<your path here>/.venv/bin/python    /<your path here>/netbox_export.py
```