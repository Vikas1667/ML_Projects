import pytesseract
import cv2
from pdf2image import convert_from_path
import spacy
nlp=spacy.load("en_core_web_lg")


def paragraph_parser(text):
    paragraph_list=''
    return paragraph_list



def pdf_page_box(image, show_boxes=1):

    '''
    :param image:
    :param show_boxex:
    :return:
    '''
    boxes = {}
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, ksize=(9, 9), sigmaX=0)
    # _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)
    contours, _ = cv2.findContours(dilate, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    temp = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # print(x, y, w, h)
        if cv2.contourArea(contour) < 10000:
            continue
        temp.append([x, y, w, h])
        if show_boxes:
            cv2.rectangle(img, (x, y), (x + w, y + h), color=(255, 0, 255), thickness=3)
    if show_boxes:
        img = cv2.resize(img, (500, 700), interpolation=cv2.INTER_AREA)
        # st.image(image=img, caption=image)
        # cv2.imshow(curr_img, img)
        # cv2.waitKey(0)
    boxes[image] = temp
    return boxes


# text is extracted from each contours stored
def extract_text(boxes) -> object:
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    tessdata_dir_config = "--tessdata-dir 'C:/Program Files/Tesseract-OCR/tessdata'"

    text = ''
    for key in boxes:
        img = cv2.imread(key)
        for x, y, w, h in boxes[key]:
            cropped_image = img[y:y + h, x:x + w]
            _, thresh = cv2.threshold(cropped_image, 127, 255, cv2.THRESH_BINARY)
            text += str(pytesseract.image_to_string(thresh, config=tessdata_dir_config))
    print('Text Extraction Completed!')
    return text


#     ## save extracted
#     ## if re.match([issuer,types],text)
#
#     ## Message extracted text from page 12 is matched above 50 first
#     entity_extracted_dict=spacy_ner_extraction(text)
#     print(entity_extracted_dict)
#     break

