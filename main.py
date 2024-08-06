
import os
from pathlib import Path
import sys
from util import extract_pdf_fields, fill_pdf_form, format_date, extract_invoice_number, create_temp_signature_pdf, stamp_pdf
from datetime import datetime


# FILL THESE IN
payment_code_value = '302'
signature_path = "./signature.png"
invoice_regex = r'EINV(\d+)'

# Constants, modify if the script does not work. Take the output from the
#  print when a pdf is opened.
outgoing_code_field = 'Text30'
payment_purpose_field = 'Text15'
payment_year_field = 'Text45'
payment_amount_field = 'Text61'
invoice_number_field = 'Text12'
current_date_field = 'Text5'
total_sum_field = 'Text76'
incoming_sum_field = 'Iznos'
gross_incoming_sum_field = 'InicijalniIznos'
payment_id_field = 'Svrha'
city_field = 'MestoKorisnika'

# ---------------------------

signature_pdf_path = './signature.pdf'

if len(sys.argv) < 2:
    input_path = input("Please enter the path to the input PDF file: ").strip().removeprefix('\'').removesuffix('\'')
else:
    input_path = sys.argv[1]

if not os.path.exists(input_path):
    print(
        f"Please drag the file into the terminal window or use an argument with the correct file path, you entered: {input_path}"
    )
    sys.exit(1)

input_fields = extract_pdf_fields(input_path)
incoming_sum = input_fields[incoming_sum_field]
gross_incoming_sum = input_fields[gross_incoming_sum_field]
payment_id_value = input_fields[payment_id_field]
city_value = input_fields[city_field]

# for (name, value) in input_fields.items():
#   print(f'{name}: {value}')

current_date = datetime.now()
current_date_value = format_date(current_date)
invoice_number = extract_invoice_number(invoice_regex, payment_id_value)
output_path = Path(input_path).parent / \
    f"Devizni Priliv {current_date_value}.pdf"

output_fields = {
    outgoing_code_field: payment_code_value,
    payment_purpose_field: f"Uplata po fakturi {invoice_number}",
    payment_year_field: str(current_date.year),
    payment_amount_field: gross_incoming_sum,
    invoice_number_field: invoice_number,
    current_date_field: f"{city_value.title()}, {current_date_value}",
    total_sum_field: incoming_sum
}

fill_pdf_form(input_path, str(output_path.absolute()), output_fields)

print(f"Filled out forms, signing...")

signature_path = create_temp_signature_pdf(signature_path, signature_pdf_path)

stamp_pdf(str(output_path), signature_path, str(output_path))

print("Cleaning up")

os.remove(signature_pdf_path)

print(f"Successfully signed and saved to {output_path}")
