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
st.header("Intraday Levels".upper(),divider='gray')

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

timeframe = st.radio(label='Select Timeframe',options=['60m','15m','5m'])

st.info("*for 1h : date range <= 45 calender days") 
st.info("*for 15m and 5m : date range <= 7 calender days")


if st.button(label='SUBMIT'):
    # Load data 

    df = yf.download(tickers=script,
                        start=start.strftime("%Y-%m-%d"),
                        end=end.strftime("%Y-%m-%d"),
                        interval=timeframe,
                        ignore_tz=True)
    trading_days = df.shape[0]
    calender_days = end - start
    st.info(f"Calender days selected : {calender_days.days}")
    st.info(f"Bars selected : {trading_days}")

    df.columns = ['CLOSE','HIGH','LOW','OPEN','Volume']
    df.drop('Volume',axis=1,inplace=True)

    # Fix column data type
    for i in df:
        df[i] = df[i].astype(float)

    data = df['CLOSE']

    n = {'60m':50,'15m':25,'5m':10}

    lv = round(data.min()/n[timeframe])*n[timeframe]
    uv = round(data.max()/n[timeframe])*n[timeframe]

    table = pd.DataFrame()

    # Adjust granularity of levels according to timeframe
    table['PRICE_LEVELS'] = range(lv,uv,n[timeframe])

    tl = []
    for i in table['PRICE_LEVELS']:
        c = 0
        for l,u in zip(df['LOW'],df['HIGH']):
            if i>=l and i<=u:
                c = c+1
            else:
                pass
        tl.append(c)
    table['CANDLE_TOUCHES'] = tl

    l1 = np.percentile(table['CANDLE_TOUCHES'],25)
    l2 = np.percentile(table['CANDLE_TOUCHES'],50)
    l3 = np.percentile(table['CANDLE_TOUCHES'],75)


    def level_strength(i,l1,l2,l3):
        if i <= l1:
            return 'Weak'.upper()
        elif (i > l1) and (i <= l2):
            return 'Moderate'.upper()
        elif (i > l2) and (i <= l3):
            return 'Strong'.upper()
        else:
            return 'Powerful'.upper()
        
    table['LEVEL_STRENGTH'] = table['CANDLE_TOUCHES'].apply(lambda i : level_strength(i,l1,l2,l3))

    st.subheader('RESULTS')
    st.write(table.sort_values(by='CANDLE_TOUCHES',ascending=False))