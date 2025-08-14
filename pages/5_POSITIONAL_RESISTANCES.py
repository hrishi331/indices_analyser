# import packages
import yfinance as yf
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st 
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Header
st.header("% Change after 'n' days".upper(),divider='gray')

# Take inputs
    # Select script
st.subheader("Select script")
symbol = st.radio(label='Indices',options=['NIFTY 50','NIFTY BANK'],
         horizontal=True)

symbol_dict = {'NIFTY 50':'^NSEI','NIFTY BANK':'^NSEBANK'}

script = symbol_dict[symbol]

# Select date window 
st.subheader("Select data window")
col1,col2 = st.columns(spec=2)
start = col1.date_input("From : ")
end = col2.date_input("To : ")

st.info("*Data window should be <= 90 calender days")


if st.button(label='SUBMIT'):
    # Load data 

    df = yf.download(tickers=script,
                        start=start.strftime("%Y-%m-%d"),
                        end=end.strftime("%Y-%m-%d"))
    trading_days = df.shape[0]
    calender_days = end - start
    st.info(f"Calender days selected : {calender_days.days}")
    st.info(f"Bars selected : {trading_days}")

    df.columns = ['CLOSE','HIGH','LOW','OPEN','Volume']
    df.drop('Volume',axis=1,inplace=True)

    # Fix column data type
    for i in df:
        df[i] = df[i].astype(float)

    data = round(df['HIGH']/100)*100
    resistance_table = data.value_counts().reset_index().sort_values(by='count')
    today_price = df['CLOSE'].iloc[-1]

    resistance_table = resistance_table[resistance_table['HIGH']>today_price]
    l1 = np.percentile(resistance_table['count'],33.33)
    l2 = np.percentile(resistance_table['count'],66.66)

    def classify(i,l1,l2):
        if i<=l1:
            return 'WEAK'
        elif i>l1 and i<=l2:
            return "MODERATE"
        else:
            return 'STRONG'
        
    resistance_table['CLASS'] = resistance_table['count'].apply(lambda i : classify(i,l1,l2))

    st.write(resistance_table.set_index('HIGH'))
    # resistance_table = resistance_table[['HIGH','CLASS']]
    # resistance_table.columns = ['RESISTANCE_LEVELS','CLASS']
    # st.write(resistance_table.set_index('RESISTANCE_LEVELS'))