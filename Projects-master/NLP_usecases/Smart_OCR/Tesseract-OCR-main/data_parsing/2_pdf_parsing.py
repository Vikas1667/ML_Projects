import concurrent.futures
from multiprocessing import freeze_support
from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter
import base64


def pdf_extract(pdf, segments):
    """
    pdf: str | Path
    segments: [(start, end), {'start': int, 'end': int}]
    """
    with open(pdf, 'rb') as read_stream:
        pdf_reader = PdfFileReader(read_stream)
        for segment in segments:
            pdf_writer = PdfFileWriter()
            # support {'start': 3, 'end': 3} or (start, end)
            try:
                start_page, end_page = segment['start'], segment['end']
            except TypeError:
                start_page, end_page = segment
            for page_num in range(start_page - 1, end_page):
                pdf_writer.addPage(pdf_reader.getPage(page_num))
            p = Path(pdf)

            # ouput = p.parent / p.with_stem(f'{p.stem}_pages_{start_page}-{end_page}')
            # with open(ouput, 'wb') as out:
            #     pdf_writer.write(out)


def __pdf_extract(pair):
    return pdf_extract(*pair)


def pdf_extract_batch(pdfs, workers=20):
    """
    pdfs = {pdf_name: [(1, 1), ...], ...}
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(__pdf_extract, pdfs.items())


def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

    return pdf_display