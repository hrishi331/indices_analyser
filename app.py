# import packages
import yfinance as yf
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st 
import datetime

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


if st.button(label='SUBMIT'):

    st.subheader("RESULTS")

    # Load data 
    df = yf.download(tickers=script,
                        start=start.strftime("%Y-%m-%d"),
                        end=end.strftime("%Y-%m-%d"))

    df.columns = ['CLOSE','HIGH','LOW','OPEN','Volume']
    df.drop('Volume',axis=1,inplace=True)

    trading_days = df.shape[0]
    calender_days = end - start
    st.info(f"Calender days selected : {calender_days.days}")
    st.info(f"Trading days selected : {trading_days}")

    # Fix column data type
    for i in df:
        df[i] = df[i].astype(float)

    lv = round(df['LOW'].min()/100)*100
    uv = round(df['HIGH'].max()/100)*100

    data = pd.DataFrame()

    levels = [i for i in range(lv,uv+1,100)]


    vals = []

    for i in levels:
        c = 0 
        for l,u in zip(df['LOW'],df['HIGH']):
            if (i>=l) & (i<u):
                c = c+1
            else:
                pass
        vals.append(c)

    data['PRICE_LEVEL'] = levels
    data['CANDLE_TOUCHES'] = vals


    l1 = np.percentile(data['CANDLE_TOUCHES'],25)
    l2 = np.percentile(data['CANDLE_TOUCHES'],50)
    l3 = np.percentile(data['CANDLE_TOUCHES'],75)

    
    def level_strength(i,l1,l2,l3):
        if i <= l1:
            return 'Weak'.upper()
        elif (i > l1) and (i <= l2):
            return 'Moderate'.upper()
        elif (i > l2) and (i <= l3):
            return 'Strong'.upper()
        else:
            return 'Powerful'.upper()
        
    data['LEVEL_STRENGTH'] = data['CANDLE_TOUCHES'].apply(lambda i : level_strength(i,l1,l2,l3))

    st.write("Level strengths")
    st.write(data.sort_values(by='CANDLE_TOUCHES',ascending=False))







    