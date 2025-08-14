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


# LEVEL Finders
with st.expander(label="LEVEL FINDER"):

    col1,col2 = st.columns(spec=2)

    if col1.button(label='INTRADAY LEVELS >>'):
        st.switch_page('pages/1_INTRADAY_LEVELS.py')
    if col2.button(label='POSITIONAL LEVELS >>'):
        st.switch_page('pages/2_POSITIONAL_LEVELS.py')


# Resistance Finders
with st.expander(label="RESISTANCE FINDER"):

    col1,col2 = st.columns(spec=2)

    if col1.button(label='INTRADAY RESISTANCES >>'):
        st.switch_page('pages/4_INTRADAY_RESISTANCES.py')
    if col2.button(label='POSITIONAL RESISTANCES >>'):
        st.switch_page('pages/5_POSITIONAL_RESISTANCES.py')

# Support Finders
with st.expander(label="SUPPORTS FINDER"):

    col1,col2 = st.columns(spec=2)

    if col1.button(label='INTRADAY SUPPORTS >>'):
        st.switch_page('pages/6_INTRADAY_SUPPORTS.py')
    if col2.button(label='POSITIONAL SUPPORTS >>'):
        st.switch_page('pages/7_POSITIONAL_SUPPORTS.py')


