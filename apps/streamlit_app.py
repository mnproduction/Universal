# views/streamlit_app.py

import streamlit as st
from views.ui import initialize_sidebar, perform_scrape_and_display

# Initialize Streamlit app
st.set_page_config(page_title="Universal Web Scraper")
st.title("Universal Web Scraper 🦀")

# Initialize sidebar and get user inputs
model_selection, url_input, fields = initialize_sidebar()

# Handling button press for scraping
if 'perform_scrape' not in st.session_state:
    st.session_state['perform_scrape'] = False

if st.sidebar.button("Scrape"):
    with st.spinner('Please wait... Data is being scraped.'):
        st.session_state['results'] = perform_scrape_and_display(url_input, fields, model_selection)
        st.session_state['perform_scrape'] = True

if st.session_state.get('perform_scrape'):
    perform_scrape_and_display(*st.session_state['results'], show_download_buttons=True)
