import imaplib
import email
import yaml
import pandas as pd
import streamlit as st


import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback
import streamlit as st



with open('V:\ML_projects\StockMarket_Analysis\stockbot\pages\cred_data\gmail_cred.yml') as f:
     content = f.read()

my_credentials = yaml.load(content, Loader = yaml.FullLoader)
user, password = my_credentials["user"], my_credentials['password']
imap_url = 'imap.gmail.com'
my_mail = imaplib.IMAP4_SSL(imap_url)
my_mail.login(user, password)
my_mail.select('Inbox')

data = my_mail.search(None, 'ALL')
mail_ids = data[1]


def email_extractor():
    id_list = mail_ids[0].split()
    len(id_list)#This should be equal to the total number of emails you have seen above
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])


    email_df = pd.DataFrame(columns=['Date','From', 'Subject','Status'], index=range(100000,first_email_id,-1))

    for i in range(100000, first_email_id, -1):
        data = my_mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'ISO-8859–1'))
                print('msg',i)  # This will let you know what row is being appended
                new_row = pd.Series({"Date": msg['Date'], "From": msg['from'], "Subject": msg['subject'],
                                     "Status": msg['X-Antivirus-Status']})
    email_df = email_df.append(new_row, ignore_index=True)
    st.Dataframe(email_df)


################# NEws EXtractor


def item_search(item, limit, page):
    stocknews = f"https://www.thestar.com.my/search/?q={item}&qsort=oldest&qrec={limit}&qstockcode=&pgno={page}"

    html = requests.get(stocknews).text
    # print(html)
    # st.write(html)

    soup = BeautifulSoup(html, 'html.parser')
    st.write(soup)
    return soup


def get_details(url):
    html = requests.get(url).text
    st.write(html)
    soup = BeautifulSoup(html, 'html.parser')
    st.write(soup)
    content = soup.find('div', {'id': 'story-body'})
    st.write(content)
    if content:
        content.get_text(strip=True)
        return content
    else:
        return ""


def read_data(stck_path):
    nse_list=pd.read_csv(stck_path)
    st.table(nse_list)
def star_new_crawler(page, search_query, limit):
    df=pd.DataFrame()
    title = []
    links = []
    premium = []
    new_type = []
    contents = []
    publishedDate = []
    while True:
        print(page)
        try:
            result = item_search(search_query, limit, page)
            title += [x.get_text(strip=True) for x in result.find_all("h2", {"class": "f18"})]
            links += [x.find('a', {"data-content-type": "Article"})['href'] for x in
                      result.find_all("h2", {"class": "f18"})]
            premium += [x.get_text(strip=True) for x in result.find_all("span", {"class": "biz-icon"})]
            new_type += [x.get_text(strip=True) for x in result.find_all("a", {"class": "kicker"})]
            contents += [get_details(x) for x in links]
            publishedDate += [x.get_text(strip=True) for x in result.find_all("span", {"class": "timestamp"})]

            if len(title) == 0:
                break
        except Exception as e:
            print(e)
            traceback.print_exc()

        page += 1

    df=pd.DataFrame({'new_type': new_type, 'title': title, 'premium': premium, 'links': links, 'published_data': publishedDate,
         'contents': contents})

    df.to_excel(f'../data/{search_query}.xlsx', index=False)

    # if len(df)>0:
    #     df.to_csv('../data/'+str(search_query) +'news.csv')

    return df
# if __name__ == '__main__':
#     page = 1
#     search_query = 'TCS'
#     limit = 30
#     star_new_crawler(page, search_query, limit)

###