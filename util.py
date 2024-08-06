
from pathlib import Path
import re
from typing import Union
import pypdf
from PIL import Image


def format_date(date):
    months_sr = ["januar", "februar", "mart", "april", "maj", "jun",
                 "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"]
    return f"{date.day} {months_sr[date.month - 1]} {date.year}"


def check_pdf_file(pdf_path: str):
    if not Path(pdf_path).exists():
        raise FileNotFoundError(
            f"Error: Please place a valid PDF file at '{pdf_path}' and try again.")
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError(f"Error: File '{pdf_path}' is not a PDF file.")


def extract_pdf_fields(pdf_path):
    check_pdf_file(pdf_path)
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = pypdf.PdfReader(pdf_file)
        fields = pdf_reader.get_form_text_fields()
    return fields


def extract_invoice_number(regex: str, transaction_id: str):
    match = re.search(regex, transaction_id)
    if match:
        invoice_number = match.group(1)
        print(f"Extracted invoice number: {invoice_number}")
        return invoice_number
    else:
        invoice_number = input(
            "Invoice number not found in the transaction ID. Modify the 'invoice_regex' to fix. Please enter the invoice number: "
            )
        return invoice_number


def fill_pdf_form(input_pdf_path: str, output_pdf_path: str, data: dict):
    check_pdf_file(input_pdf_path)
    pdf_writer = pypdf.PdfWriter(clone_from=input_pdf_path)
    pdf_writer.update_page_form_field_values(page=None, fields=data)
    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)


def create_temp_signature_pdf(signature_path: str, output_path: str):
    if Path(output_path).exists():
        return output_path

    if not Path(signature_path).exists():
        raise FileNotFoundError(
            f"Please put your signature as a PNG image with transparency at '{
                signature_path}' and try again."
        )

    signature_image = Image.open(signature_path)
    signature_image.save(output_path, 'PDF', resolution=100.0)
    return output_path


def stamp_pdf(
    content_pdf: Union[Path, str],
    stamp_pdf: Union[Path, str],
    pdf_result: Union[Path, str],
    signature_fraction: float = 0.15,
    signature_offset_x: float = 0.15,
    signature_offset_y: float = 0.05,
):
    check_pdf_file(content_pdf)
    check_pdf_file(stamp_pdf)
    stamp_page = pypdf.PdfReader(stamp_pdf).pages[0]
    stamp_intrinsic_size = max(
        stamp_page.mediabox.height, stamp_page.mediabox.width)

    reader = pypdf.PdfReader(content_pdf)
    writer = pypdf.PdfWriter(clone_from=reader)

    for content_page in writer.pages:
        height = content_page.mediabox.height
        width = content_page.mediabox.width
        stamp_w = width * signature_fraction
        stamp_h = height * signature_fraction
        stamp_scale = min(stamp_w, stamp_h) / stamp_intrinsic_size
        print(f"Stamping page with scale {
              stamp_scale} and intrinsic size {stamp_intrinsic_size}")
        content_page.merge_transformed_page(
            stamp_page,
            pypdf.Transformation()
            .scale(stamp_scale)
            # 0,0 is pdf's bottom left corner
            .translate(
                tx=width - width * signature_offset_x - stamp_w,
                ty=height*signature_offset_y
            )
        )

    writer.write(pdf_result)
