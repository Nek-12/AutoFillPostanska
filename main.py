
from util import *
from datetime import datetime


# FILL THESE IN
city = "Novi Sad"
pdf_path = './files/priliv_sample.pdf'
output_path = './files/priliv_sample_filled.pdf'
payment_code_value = '302'
signature_path = "./files/signature.png"
payment_purpose_value = 'Uplata za usluge izrade računarskih programa'
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

input_fields = extract_pdf_fields(pdf_path)
incoming_sum = input_fields['Iznos']
gross_incoming_sum = input_fields['InicijalniIznos']
payment_id_value = input_fields['Svrha']

# for (name, value) in input_fields.items():
    # print(f'{name}: {value}')

current_date = datetime.now()
current_date_value = format_date(current_date)
invoice_number = extract_invoice_number(invoice_regex, payment_id_value)

output_fields = {
    outgoing_code_field: payment_code_value,
    payment_purpose_field: payment_purpose_value,
    payment_year_field: str(current_date.year),
    payment_amount_field: gross_incoming_sum,
    invoice_number_field: invoice_number,
    current_date_field: current_date_value,
    total_sum_field: incoming_sum
}

fill_pdf_form(pdf_path, output_path, output_fields, signature_path)

print(f"Filled out forms, signing...")

signature_path = create_temp_signature_pdf(signature_path, './files/signature.pdf')

stamp_pdf(output_path, signature_path, output_path)

print(f"Successfully signed and saved to {output_path}")
