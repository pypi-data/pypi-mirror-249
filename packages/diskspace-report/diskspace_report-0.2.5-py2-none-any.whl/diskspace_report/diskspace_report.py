#!/usr/bin/python3

# Import libraries that are needed
import locale
import shutil
from csv import DictWriter
import sys, os
import smtplib
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

def error_log():
	logging.basicConfig(filename='diskspace_report.log', level=logging.DEBUG,
						format='%(asctime)s %(levelname)s %(name)s %(message)s')
	logger=logging.getLogger(__name__)
	return logger

try:
	from  diskspace_report.pkg_helpers import config_report
except ImportError:
	error_log()
try:
	from pkg_helpers import config_report
except ImportError:
	error_log()

# Main function that controls what should be done
def main():
	total_space, used_space,percent_usedspace, free_space, percent_freespace = calculate_space()

	# Check the printing parameter
	if config_report.booL_print == True:
		show_values(total_space, used_space,percent_usedspace, free_space, percent_freespace)

	# Check the export parameter
	if config_report.bool_export == True:
		write_csv(total_space, used_space,percent_usedspace, free_space, percent_freespace)

	# Check the email parameter
	if config_report.bool_email == True:
		mail_results()

# Calculate the values of the disk (free, used, total + percentage)
def calculate_space():
	total, used, free = shutil.disk_usage("/")

	total_space = total // config_report.disk_factor
	free_space = free // config_report.disk_factor
	used_space = total_space - free_space
	percent_freespace = round(((free_space / total_space) * 100), ndigits=2)
	percent_usedspace = round(((used_space / total_space) * 100), ndigits=2)
		
	return total_space, used_space, percent_usedspace, free_space, percent_freespace

# Set the number format for the exported values. Settings in the header
def int_num(number, digits=2):
    if number is None:
        return ''
    if not isinstance(number, int) and not isinstance(number, float):
        return ''
    else:
        format = '%.'+str(digits)+'f'
        return locale.format_string(format, number, 1)

# Export the calculates values to a csv-file. Pathsettings above
def write_csv(total_space, used_space, percent_usedspace, free_space,  percent_freespace):
	# Format the sequence of the rows in the exported csv-file
	field_names = ['Date','Space Abs (GB)','Space Free (GB)','Percent Free', 'Space Used (GB)', 'Percent Used' ]
	dict = {'Date': config_report.actualtime, 'Space Abs (GB)': int_num(total_space), 'Space Free (GB)': int_num(free_space),
			'Percent Free': int_num(percent_freespace), 'Space Used (GB)': int_num(used_space),
			'Percent Used': int_num(percent_usedspace)}
	
	# Check, if the file exists. Only write the header once
	if not os.path.exists(config_report.csvfile):
		with open(config_report.csvfile, 'w') as f_object:
			dictwriter_object = DictWriter(f_object, fieldnames=field_names, delimiter=';')
			dictwriter_object.writeheader()
			f_object.close()
	# Append new entries, at each run of the script
	with open(config_report.csvfile, 'a') as f_object:
		dictwriter_object = DictWriter(f_object, fieldnames=field_names, delimiter=';')
		dictwriter_object.writerow(dict)
		f_object.close()

# Print the calculated values to screen,
def show_values(total_space, used_space, percent_usedspace,free_space, percent_freespace):
	print("Disk Space Report from: " + str(config_report.actualtime))
	print("Total: %d GB" % total_space, " / 100 Percent")
	print("Used: %d GB" % used_space, " / %d Percent" % percent_usedspace)
	print("Free: %d GB" % free_space, " / %d Percent" % percent_freespace)


# Email the results
def mail_results():

	msg = MIMEMultipart('mixed')
	msg['From'] = config_report.sender
	msg['To'] = config_report.recipient
	msg['Subject'] = config_report.SUBJECT

	body = MIMEText(config_report.body)
	msg.attach(body)

	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(config_report.csvfile, "rb", ).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % config_report.csvfile)
	msg.attach(part)

	smtpObj = smtplib.SMTP(config_report.SMTP_SERVER, config_report.SMTP_PORT)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(config_report.MY_USER, config_report.MY_PASSWORD)
	smtpObj.sendmail(config_report.sender, config_report.recipient, msg.as_string())
	smtpObj.quit()

# Start the  programm
if __name__ == "__main__":
	main()