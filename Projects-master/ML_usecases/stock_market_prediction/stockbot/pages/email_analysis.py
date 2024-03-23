import os
import sys
import json
import pandas as pd
import imaplib
# import email
from email import message_from_bytes
from email import header
import getpass
import yaml
import streamlit as st

with open('cred.yml') as f:
     cred = f.read()

my_credentials = yaml.load(cred, Loader = yaml.FullLoader)
imap_url = 'imap.gmail.com'


class Email_extractor:
    def __init__(self,my_credentials):
        self.user=my_credentials["username"]
        self.password = my_credentials['password']
        self.data = []

    def get_login(self):
        print("\nPlease enter your Gmail login details below.")
        self.usr = input("Email: ")
        self.pwd = input("Password: ")


    def attempt_login(self):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.user, self.password)

    def select_mail(self):

        self.data=self.mail.select("inbox")

        # print(type(self.data[1]), len(self.data[0]))
        mail_ids = self.data[1]
        id_list = mail_ids[0].split()
        print('Ids extracted',id_list)

    def mail_extract(self):
        date_list = []
        from_list = []
        subject_text = []

        result, numbers = self.mail.uid('search', None, "ALL")
        uids = numbers[0].split()
        uids = [id.decode("utf-8") for id in uids]
        uids = uids[-1:-101:-1]
        # print("Latest mailids",uids)
        result, messages = self.mail.uid('fetch', ','.join(uids), '(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])')
        messages = [i for i in messages if isinstance(i, tuple)]
        st.write(messages[:2])

        for i, message in messages[::2]:
            try:
                msg = message_from_bytes(message)
                # print(msg)
                decode = header.decode_header(msg['Subject'])[0]
                # print('as', msg, decode)

                if isinstance(decode[0], bytes):
                    decoded = decode[0].decode()
                    subject_text.append(decoded)
                else:
                    subject_text.append(decode[0])
                date_list.append(msg.get('date'))
                fromlist = msg.get('From')
                fromlist = fromlist.split("<")[0].replace('"', '')
                from_list.append(fromlist)
            except Exception as e:
                st.write(e)
                pass

        date_list = pd.to_datetime(date_list,format='mixed')
        date_list1 = []
        for item in date_list:
            date_list1.append(item.isoformat(' ')[:-6])

        df = pd.DataFrame(data={'Date': date_list1, 'Sender': from_list, 'Subject': subject_text})
        st.write(df)
        return df

    def search(self,key, value):
        result, data = self.mail.search(None, key, '"{}"'.format(value))
        return data

    def get_email(self,result_bytes):

        date_list = []
        from_list = []
        subject_text = []

        uids = result_bytes[0].split()
        print('sdd ',result_bytes)
        uids = [id.decode("utf-8") for id in uids]
        uids = uids[-1:-201:-1]
        # print("Latest mailids",uids)
        # uids = uids[:100]

        result, messages = self.mail.uid('fetch', ','.join(uids), '(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])')
        messages = [i for i in messages if isinstance(i, tuple)]
        st.write(messages[:2])

        for i, message in messages[::2]:
            try:
                msg = message_from_bytes(message)
                # print(msg)
                decode = header.decode_header(msg['Subject'])[0]
                # print('as', msg, decode)

                if isinstance(decode[0], bytes):
                    decoded = decode[0].decode()
                    subject_text.append(decoded)
                else:
                    subject_text.append(decode[0])
                date_list.append(msg.get('date'))
                fromlist = msg.get('From')
                fromlist = fromlist.split("<")[0].replace('"', '')
                from_list.append(fromlist)
            except Exception as e:
                st.write(e)
                pass

        date_list = pd.to_datetime(date_list, format='mixed')
        date_list1 = []
        for item in date_list:
            date_list1.append(item.isoformat(' ')[:-6])

        df = pd.DataFrame(data={'Date': date_list1, 'Sender': from_list, 'Subject': subject_text})
        st.write(df)
        return df


    def parseEmails(self):
        jsonOutput = {}
        for anEmail in self.data[0].split():
            type, self.data = self.mail.fetch(anEmail, '(UID RFC822)')
            raw = self.data[0][1]
            raw_str = raw.decode("utf-8")
            msg = email.message_from_string(raw_str)
            jsonOutput['subject'] = msg['subject']
            jsonOutput['from'] = msg['from']
            jsonOutput['date'] = msg['date']

            raw = self.data[0][0]
            raw_str = raw.decode("utf-8")
            uid = raw_str.split()[2]
            # Body #
            if msg.is_multipart():
                for part in msg.walk():
                    partType = part.get_content_type()
                    ## Get Body ##
                    if partType == "text/plain" and "attachment" not in part:
                        jsonOutput['body'] = part.get_payload()
                    ## Get Attachments ##
                    if part.get('Content-Disposition') is None:
                        attchName = part.get_filename()
                        if bool(attchName):
                            attchFilePath = str(self.destFolder) + str(uid) + str("/") + str(attchName)
                        os.makedirs(os.path.dirname(attchFilePath), exist_ok=True)
                        with open(attchFilePath, "wb") as f:
                            f.write(part.get_payload(decode=True))
            else:
                jsonOutput['body'] = msg.get_payload(decode=True).decode(
                    "utf-8")  # Non-multipart email, perhaps no attachments or just text.
            outputDump = json.dumps(jsonOutput)
            emailInfoFilePath = str(self.destFolder) + str(uid) + str("/") + str(uid) + str(".json")
            os.makedirs(os.path.dirname(emailInfoFilePath), exist_ok=True)
            with open(emailInfoFilePath, "w") as f:
                f.write(outputDump)

if __name__ == "__main__":
    email=Email_extractor(my_credentials)
    email.attempt_login()
    email.select_mail()

    # email.mail_extract()

    res=email.search('FROM', '*@cummins.com')
    msgs = email.get_email(res)






