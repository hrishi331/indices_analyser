import streamlit as st

st.set_page_config("HOME")

st.header("Positional/Intraday Analysis Of Price Level And Strength for Indices",width='content')

text1 = """
1. This application gives analysis for NIFTY 50 and BANK NIFTY index.
2. This gives positional and intraday analysis.
3. For intraday timeframe used is 60m [hourly] and for positional 1d [daily].
4. It finds price levels in given data window and then classifies them into 4 categories
weak,moderate, strong and powerfull.
5. These classification is based on number of times candles or bars touching that price level. 
"""
st.write(text1)

col1,col2 = st.columns(spec=2)

if col1.button(label='INTRADAY >>'):
    st.switch_page('pages/INTRADAY.py')
if col2.button(label='POSITIONAL >>'):
    st.switch_page('pages/POSITIONAL.py')