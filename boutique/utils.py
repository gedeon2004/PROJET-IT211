# boutique/utils.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse

def generate_pdf(data):
    """
    Generates a PDF with the provided data and returns it as an HTTP response.
    """
    # Create a bytes buffer for storing the PDF
    buffer = BytesIO()

    # Create a PDF canvas
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add content to the PDF (this is just an example)
    c.drawString(100, height - 100, "Generated PDF Example")
    c.drawString(100, height - 120, f"Data: {data}")

    # Save the PDF
    c.showPage()
    c.save()

    # Get the PDF from the buffer
    buffer.seek(0)

    # Return the PDF as an HTTP response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="generated_pdf.pdf"'
    return response
    