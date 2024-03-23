import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


class profit_loss:
    def __init__(self,df,timeslot=10):
        self.df=df
        self.timeslot=timeslot

    def profit_loss_chart(self):
        try:
            prof_loss_dict={}
            self.df = self.df[self.df['Realized P&L'].notna()]

            pnl_10 = self.df[self.df['Realized P&L'].notna()][:self.timeslot]
            colors = [1 if c >= 0 else 0 for c in pnl_10['Realized P&L'].tolist()]
            fig, ax = plt.subplots(figsize=(10, 10))
            a=[i for i in range(0,self.timeslot)]

            sns.barplot(x=a, y=pnl_10['Realized P&L'],
                        hue=colors,
                        ax=ax,
                        dodge=False
                        )

            st.pyplot(fig)
            profit = self.df[self.df['Realized P&L'] > 0]['Realized P&L']
            loss = self.df[self.df['Realized P&L'] < 0]['Realized P&L']

            prof_loss_dict['profit']=profit
            prof_loss_dict['loss'] = loss

        except Exception as e:
            st.write(e)
        return prof_loss_dict
