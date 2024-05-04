
import requests
import streamlit as st
from bardapi import Bard, SESSION_HEADERS

session = requests.Session()
token = "cAh5K-1ML8c1DlK0oxAqpqGjMFhb76Gyl4IV1I3hlMCcDCi7S0GMNS0320S5j23qJ5hReA."
session.cookies.set("__Secure-1PSID", "cAh5K-1ML8c1DlK0oxAqpqGjMFhb76Gyl4IV1I3hlMCcDCi7S0GMNS0320S5j23qJ5hReA.")
session.cookies.set( "__Secure-1PSIDCC", "ACA-OxM7cfT2WiiTj71SUvvbHsLTH7wz_th4zxdeYQ3g2TAv1qMJsJuKMo4URo1CpSl28E-ltdEo")
session.cookies.set("__Secure-1PSIDTS", "sidts-CjEBNiGH7uxSjWiw8erBjRMZZ_FRkZiaVssM6Bu8LWiOuD8EbwSSOd6HG3KsEQ1a7qyxEAA")
session.headers = SESSION_HEADERS

bard = Bard(token=token, session=session)

st.write("BARD Bot")
ques=st.text_input("Input your question")

if ques:
    ans=bard.get_answer(ques)["content"]
    print(ans)
    st.write("Answer",ans)

