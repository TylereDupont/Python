import os
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import Color
import io
import concurrent.futures
from reportlab.lib.units import inch
from PIL import Image as PILImage

# Define default settings
HEX_COLOR = "#333799"
TEXT_OPACITY = 0.15
LOGO_OPACITY = 0.01
FONT = "IBM Plex Mono"
FONT_SIZE = 10
WATERMARK_SIZE = 8 * inch  # Size of the watermark image (width and height are the same)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def adjust_image_opacity(image_path, output_path, opacity):
    with PILImage.open(image_path).convert("RGBA") as img:
        # Extract alpha channel
        r, g, b, a = img.split()
        
        # Apply opacity to alpha channel
        a = a.point(lambda p: int(p * opacity))
        img.putalpha(a)
        
        # Save the image with adjusted opacity
        img.save(output_path, format="PNG")

def create_watermark(name, hex_color=HEX_COLOR, text_opacity=TEXT_OPACITY, logo_opacity=LOGO_OPACITY, font=FONT, font_size=FONT_SIZE):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Register fonts
    try:
        pdfmetrics.registerFont(TTFont('IBM Plex Mono', 'IBMPlexMono-Regular.ttf'))
        can.setFont(font, font_size)
    except Exception as e:
        print(f"Failed to register IBM Plex Mono: {e}")
        can.setFont("Courier", font_size)  # Fallback to Courier if custom font registration fails
    
    # Set the color for text
    r, g, b = hex_to_rgb(hex_color)
    color = Color(r, g, b, alpha=text_opacity)
    can.setStrokeColor(color)
    can.setFillColor(color)
    
    # Draw the watermark text (rotated)
    can.saveState()
    can.translate(letter[0] / 2, letter[1] / 3)  # Translate to bottom two-thirds of the page
    can.rotate(45)
    
    # Draw the watermark text as vector graphics
    watermark_text = f"APT - 0 | Confidential | {name}"
    text_object = can.beginText(0, 0)
    text_object.setTextOrigin(-can.stringWidth(watermark_text) / 2, 0)
    text_object.setFont(font, font_size)
    text_object.textLines(watermark_text)
    can.drawText(text_object)
    can.restoreState()
    
    # Draw the image watermark (centered, not rotated)
    image_path = "logo.png"  # Keep the image file name as 'logo.png'
    temp_logo_path = "logo_transparent.png"  # Temporary file for the adjusted image
    if os.path.exists(image_path):
        adjust_image_opacity(image_path, temp_logo_path, logo_opacity)
        center_x = letter[0] / 2 - WATERMARK_SIZE / 2
        center_y = letter[1] / 2 - WATERMARK_SIZE / 2
        can.drawImage(temp_logo_path, center_x, center_y, width=WATERMARK_SIZE, height=WATERMARK_SIZE, mask='auto')
    else:
        print(f"Warning: The image file '{image_path}' was not found.")

    can.save()
    
    packet.seek(0)
    return PdfReader(packet)

def add_watermark(input_pdf_path, output_pdf_path, name, hex_color=HEX_COLOR, text_opacity=TEXT_OPACITY, logo_opacity=LOGO_OPACITY, font=FONT, font_size=FONT_SIZE):
    input_pdf = PdfReader(input_pdf_path)
    
    # Create watermark with adjusted logo opacity
    watermark_pdf = create_watermark(name, hex_color, text_opacity, logo_opacity, font, font_size)
    watermark_page = watermark_pdf.pages[0]
    
    pdf_writer = PdfWriter()

    for page_number in range(len(input_pdf.pages)):
        original_page = input_pdf.pages[page_number]

        # Create a new page to add the watermark to
        new_page = PageObject.create_blank_page(
            width=original_page.mediabox.width,
            height=original_page.mediabox.height
        )

        # Merge the watermark with the new blank page
        new_page.merge_page(watermark_page)

        # Merge the original page content on top of the new page with the watermark
        new_page.merge_page(original_page)
        
        # Add the new page with the watermark underneath the original content to the writer
        pdf_writer.add_page(new_page)
    
    # Write out the new PDF with watermarks
    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

def process_pdf_for_name(pdf_path, name, output_folder, hex_color=HEX_COLOR, text_opacity=TEXT_OPACITY, logo_opacity=LOGO_OPACITY, font=FONT, font_size=FONT_SIZE):
    # Determine relative path for output
    relative_path = os.path.relpath(pdf_path, 'input')
    output_dir = os.path.join(output_folder, name, os.path.dirname(relative_path))
    os.makedirs(output_dir, exist_ok=True)
    
    output_pdf_path = os.path.join(output_dir, os.path.basename(pdf_path))
    print(f"Processing {pdf_path} for {name}...")
    add_watermark(pdf_path, output_pdf_path, name, hex_color, text_opacity, logo_opacity, font, font_size)

def process_pdfs(names_file, input_folder, output_folder, hex_color=HEX_COLOR, text_opacity=TEXT_OPACITY, logo_opacity=LOGO_OPACITY, font=FONT, font_size=FONT_SIZE):
    with open(names_file, 'r') as f:
        names = [line.strip() for line in f]

    pdf_paths = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_paths.append(os.path.join(root, file))

    # Use parallel processing to speed up the watermarking
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for name in names:
            for pdf_path in pdf_paths:
                executor.submit(process_pdf_for_name, pdf_path, name, output_folder, hex_color, text_opacity, logo_opacity, font, font_size)

if __name__ == "__main__":
    names_file = "names.txt"  # File containing names
    input_folder = "input"  # Folder containing PDFs
    output_folder = "output"  # Folder where watermarked PDFs will be saved
    
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Example of setting custom values
    custom_hex_color = "#6E72D4"
    custom_text_opacity = 0.15
    custom_logo_opacity = 0.2
    custom_font = "IBM Plex Mono"
    custom_font_size = 8
    
    process_pdfs(names_file, input_folder, output_folder, hex_color=custom_hex_color, text_opacity=custom_text_opacity, logo_opacity=custom_logo_opacity, font=custom_font, font_size=custom_font_size)
