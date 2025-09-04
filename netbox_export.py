import os
import smtplib
import zipfile
from datetime import date
from email.message import EmailMessage

import requests
from dotenv import load_dotenv

templates = {'Devices': '/api/dcim/devices/', 
             'IP Addresses': '/api/ipam/ip-addresses/',
             'Prefixes': '/api/ipam/prefixes/',
             'Virtual Machines': '/api/virtualization/virtual-machines/',
             'VLANs': '/api/ipam/vlans/'}

def netbox_get(template, path):
    url = netbox_base_url + path
    params = {'export': template}
    response = requests.get(url, params=params, headers=netbox_headers, verify=False)
    response.raise_for_status()
    return response.content

def send_email():
    mail_server = os.environ.get('mail_server')
    email_filename = 'netbox_export_' + str(date.today()) + '.zip'
    msg = EmailMessage()
    msg['Subject'] = 'Netbox Export ' + str(date.today())
    msg['From'] = os.environ.get('email_from')
    msg['To'] = os.environ.get('email_to')
    if os.path.exists(zip_filename):
        with open(zip_filename, 'rb') as fp:
            zip_data = fp.read()
        msg.add_attachment(zip_data, maintype='application', subtype='zip', filename=email_filename)
    else:
        msg.set_content('No .zip file created, verify export templates configuration')
    with smtplib.SMTP(mail_server) as smtp:
        smtp.send_message(msg)

load_dotenv()
netbox_base_url = os.environ.get('netbox_url')
local_path = os.path.dirname(__file__)
zip_filename = os.path.join(local_path, 'netbox_export.zip')
netbox_headers = {'Authorization': f'Token {os.environ.get('netbox_token')}'}

try:
    os.remove(zip_filename)
except FileNotFoundError:
    pass

for template, path in templates.items():
    try:
        export_file = netbox_get(template, path)
        save_file_path = os.path.join(local_path, f'{template}.csv')
        with open(save_file_path, 'wb') as csvfile:
            csvfile.write(export_file)
        with zipfile.ZipFile(zip_filename, 'a', compression=zipfile.ZIP_DEFLATED) as zip:
            zip.write(save_file_path, arcname=f'{template}.csv')
    except:
        continue

send_email()