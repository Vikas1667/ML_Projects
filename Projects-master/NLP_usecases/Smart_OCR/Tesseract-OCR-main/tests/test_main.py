# from tests.ocr_single_page import *
# from tests.entity_extractors import *
from entity_extractors import *
from ocr_single_page import *
import subprocess
import PyPDF2
from PyPDF2 import PdfFileReader
import PyPDF2
from PyPDF2 import PdfFileReader,PdfFileWriter


import os




# path = r'V:\ML_projects\github_proj\project\Projects-master\NLP_usecases\Smart_OCR\Tesseract-OCR-main\input_pdf\EB-51-Quality-of-Indian-Wheat.pdf'
# print('current',os.getcwd())
scan_pdf_path = r'V:\ML_projects\github_proj\project\Projects-master\NLP_usecases\Smart_OCR\Tesseract-OCR-main\input_pdf\Final IM.pdf'
print('current',os.getcwd())


entity_dict={}

def ocr_pdf_extractor(pdf_path):
    print("Pdf_to_image_initiated")
    pages = convert_from_path(pdf_path,dpi=350, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
    print("No of Pages", pages)

    page_no = 1


    for page in pages:
        print('Extracting Initiated')
        entity_dict['page_no'] = page_no

        img_str = 'page' + str(page_no) + '.jpg'
        page.save('page' + str(page_no) + '.jpg', 'JPEG')
        boxes = pdf_page_box(img_str, show_boxes=1)

        print('Pdf_box is completed for single page')

        text = extract_text(boxes)
        print(text)
        with open(r'extracted_pages_text/pdf_text.txt','w',encoding='utf8') as f:
            f.write(text)

        ## save extracted
        ## if re.match([issuer,types],text)

        ## Message extracted text from page 12 is matched above 50 first
        entity_extracted_dict=spacy_ner_extraction(text)
        print(entity_extracted_dict)

        regex_entity_dict=Regex_NER_extraction(text)
        print(regex_entity_dict)

        break



def pdf_parser(pdf_path):
    pdfObject = open(pdf_path, 'rb')    # creating a pdf file object
    pdfReader = PdfFileReader(pdfObject)    # creating a pdf reader object

    # Extract and concatenate each page's content
    text=''
    for page_no in range(0,pdfReader.numPages):
        pageObject = pdfReader.getPage(page_no) # creating a page object
        text += pageObject.extractText()
        page_text=pageObject.extractText()
        print('page_text',page_text)
        if page_text =='':
            img_str = 'page' + str(page_no) + '.jpg'
            print('pdf_pages',img_str)

            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pageObject)

            with open(r'./pdf_pages/page.pdf','w') as pdf_output:
                 pdf_writer.write(pdf_output)

            # pageObject.('./pdf_pages/page' + str(page_no) + '.jpg', 'JPEG')

            # boxes = pdf_page_box(img_str, show_boxes=1)



    # print("PYPDF2 TEXT", text)
    return text

text=pdf_parser(scan_pdf_path)
