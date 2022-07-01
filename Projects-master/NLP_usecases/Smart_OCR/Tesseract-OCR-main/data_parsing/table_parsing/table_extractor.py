import tabula
from tabula import read_pdf
from tabulate import tabulate
import pandas as pd



def pdf_extract(pdf_path):
    # reads table from pdf file
    df = read_pdf(r"../../input_pdf/EB-51-Quality-of-Indian-Wheat.pdf", pages="all")  # address of pdf file

    for i, v in enumerate(df):
        f = pd.DataFrame(v)

        # f.to_csv('./out_tables/table' + str(i) + '.csv', encoding="utf8")


#reads table from pdf file
df = read_pdf(r"../../input_pdf/EB-51-Quality-of-Indian-Wheat.pdf", pages="all") #address of pdf file
print(type(df))


for i,v in enumerate(df):
    f=pd.DataFrame(v)
    f.to_csv('./out_tables/table'+str(i)+'.csv',encoding="utf8")
    print(f)


# print(tabulate(df))
# table=tabulate(df)
# print(type(table))
# with open('./out_tables/table.txt','w',encoding='utf8') as f:
#     f.write(table)
# table_df=pd.read_csv('./out_tables/table.txt',sep='\s+',encoding='utf-8')
# print(df)
# df.to_csv('./out_tables/tables.csv',encoding='utf8')
