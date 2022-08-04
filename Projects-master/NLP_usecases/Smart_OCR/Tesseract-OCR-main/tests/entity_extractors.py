import spacy
import re
nlp=spacy.load("en_core_web_lg")



def spacy_ner_extraction(text):

    entity_dict = {}
    ner_doc = nlp(text)

    if ner_doc:

        for token in ner_doc.ents:

            # if token.tag_ == "NN":

            #     entity_dict[token.ent_type] = token.text

            entity_dict[str(spacy.explain(token.label_))] = token

    return entity_dict


def Regex_NER_extraction(text):
    issuer = re.findall('(?<=\n\nIssuer ).*',text)
    print('Issuer: ',issuer,"\n")

    Type_of_instrument = re.findall('(?<=Type of Instrument ).*\.', text)
    print('Type_of_instrument: ', Type_of_instrument, "\n")

    Seniority = re.findall('(?<=Senlority ).*', text)
    print('Seniority: ', Seniority, "\n")

    Security = re.findall('(?<=Security Name ).*', text)
    print('Security: ', Security, "\n")

    Date_of_Maturity = re.findall('(?<=Deemed date of Allotment ).*', text)
    print('Date of Maturity: ', Date_of_Maturity, "\n")

    Deemed_Date_of_Allotment = re.findall('(?<=Date of Maturity : ~~ ).*', text)
    print('Deemed Date of Allotment: ', Deemed_Date_of_Allotment, "\n")

    coupon = re.findall('(?<=Coupon ).*',text)
    print('Coupon: ', coupon,"\n")

    Coupon_Payment_Frequency = re.findall('(?<=Coupon Payment frequency ).*', text)
    print('Coupon_Payment_Frequency: ', Coupon_Payment_Frequency, "\n")

    entity_dict = {'Type_of_instrument': Type_of_instrument, "Seniority": Seniority, "Security": Security,
                   "Issuer": issuer,"Date of Maturity": Date_of_Maturity, "Deemed Date of Allotment": Deemed_Date_of_Allotment,
                   "Coupon": coupon,"Coupon Payment Frequency": Coupon_Payment_Frequency}

    return entity_dict
