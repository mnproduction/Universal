# views/ui.py

import json
from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags_sidebar

from core.scraper import crawler, converter, raw_processor, json_processor, formatter
from core.model import DynamicListingContainerModel, DynamicListingModel

def initialize_sidebar():
    """Инициализирует боковую панель и возвращает пользовательские данные"""
    st.sidebar.title("Web Scraper Settings")
    model_selection = st.sidebar.selectbox("Select Model", options=["gpt-4o-mini", "gpt-4o-2024-08-06"], index=0)
    url_input = st.sidebar.text_input("Enter URL")

    # Tags input in the sidebar
    tags = st_tags_sidebar(
        label='Enter Fields to Extract:',
        text='Press enter to add a tag',
        value=[],  # Default values if any
        suggestions=[],  # You can still offer suggestions
        maxtags=-1,  # Set to -1 for unlimited tags
        key='tags_input'
    )

    st.sidebar.markdown("---")
    
    return model_selection, url_input, tags

def perform_scrape_and_display(url_input, fields, model_selection, show_download_buttons=False):
    """Выполняет скрапинг и отображает результаты"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    raw_html = crawler.get_html(url_input)
    markdown = converter.convert(raw_html)
    raw_processor.write(markdown, timestamp)

    DynamicListingModelInstance = DynamicListingModel.create(fields)
    DynamicListingsContainer = DynamicListingContainerModel.create(DynamicListingModelInstance)
    formatted_data = formatter.format_data(markdown, DynamicListingsContainer)
    formatted_data_text = formatter.get_text(formatted_data)
    input_tokens, output_tokens, total_cost = formatter.calculate_cost(markdown, formatted_data_text, model=model_selection)
    df = json_processor.write(formatted_data, timestamp)

    # Display results in Streamlit
    st.write("Scraped Data:", df)
    st.sidebar.markdown("## Token Usage")
    st.sidebar.markdown(f"**Input Tokens:** {input_tokens}")
    st.sidebar.markdown(f"**Output Tokens:** {output_tokens}")
    st.sidebar.markdown(f"**Total Cost:** :green-background[***${total_cost:.4f}***]")

    if show_download_buttons:
        display_download_buttons(df, formatted_data, markdown, timestamp)

    return df, formatted_data, markdown, input_tokens, output_tokens, total_cost, timestamp

def display_download_buttons(df, formatted_data, markdown, timestamp):
    """Отображает кнопки загрузки данных в Streamlit"""
    # Create columns for download buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("Download JSON", data=json.dumps(formatted_data.dict(), indent=4), file_name=f"{timestamp}_data.json")
    with col2:
        # Convert formatted data to a dictionary if it's not already (assuming it has a .dict() method)
        data_dict = formatted_data.dict() if hasattr(formatted_data, 'dict') else formatted_data

        # Access the data under the dynamic key
        first_key = next(iter(data_dict))  # Safely get the first key
        main_data = data_dict[first_key]   # Access data using this key

        # Create DataFrame from the data
        df = pd.DataFrame(main_data)

        st.download_button("Download CSV", data=df.to_csv(index=False), file_name=f"{timestamp}_data.csv")
    with col3:
        st.download_button("Download Markdown", data=markdown, file_name=f"{timestamp}_data.md")
