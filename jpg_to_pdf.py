import utilit
from PIL import Image
import img2pdf
import cv2
from fpdf import FPDF
def save_pdf(n):
    im1 = Image.open("Received/"+str(n)+".jpg")

    pdf1_filename = "Received/pdf_"+str(n)+".pdf"

    im1.save(pdf1_filename, "PDF", resolution=100.0)

def make_pdf_photos(imagelist):
    from fpdf import FPDF
    pdf = FPDF()
    # imagelist is the list with all image filenames
    for image in imagelist:
        pdf.add_page()
        pdf.image(image, 0, 0)
    pdf.output("yourfile.pdf", "F")

def several_photos(listPages):
    from fpdf import FPDF
    from PIL import Image

    cover = Image.open(listPages[0])
    width, height = cover.size

    pdf = FPDF(unit="pt", format=[width, height])

    for page in listPages:
        pdf.add_page()
        pdf.image(page, 0, 0)

    pdf.output("PDF/my.pdf", "F")
