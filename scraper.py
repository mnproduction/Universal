import os
import time
import re
import json
from datetime import datetime
from typing import List, Dict, Type

import pandas as pd
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, create_model
import html2text
import tiktoken

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from openai import OpenAI

load_dotenv()


def setup_selenium():
    options = Options()

    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(r"./webdriver/chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)

    return driver


def fetch_html_selenium(url: str) -> str:
    driver = setup_selenium()
    try:
        driver.get(url)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error fetching HTML: {e}")
        return ""
    finally:
        driver.quit()

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    
    for element in soup.find_all('header', 'footer', 'nav', 'aside'):
        element.decompose()

    return str(soup)

def html_to_markdown_with_readability(html: str) -> str:
    cleaned_html = clean_html(html)
    markdown_converter = html2text.HTML2Text()
    markdown_converter.ignore_links = False
    markdown = markdown_converter.handle(cleaned_html)
    return markdown

pricing = {
    "gpt-4o-mini": {
        "input": 0.150 / 1_000_000,
        "output": 0.600 / 1_000_000
    },
    "gpt-4o": {
        "input": 2.5 / 1_000_000,
        "output": 10 / 1_000_000
    },
    # other models
}

model_used="gpt-4o-mini"

def save_raw_data(data: str, timestamp: datetime, output_folder: str = "./output/raw_data") -> str:
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, f"raw_data_{timestamp}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)
    print(f"Raw data saved to {file_path}")
    return file_path

def remove_urls(file_path: str) -> str:
    url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    base, ext = os.path.splitext(file_path)
    new_file_path = f"{base}_cleaned{ext}"

    with open(file_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    cleaned_text = re.sub(url_pattern, "", markdown)
    
    with open(new_file_path, "w", encoding="utf-8") as file:
        file.write(cleaned_text)

    print(f"URLs removed and saved to {new_file_path}")
    return cleaned_text


def create_dynamic_listing_model(field_names: List[str]) -> Type[BaseModel]:
    field_definitions = {field: (str, ...) for field in field_names}
    return create_model("DynamicListingModel", **field_definitions)


def create_listing_container_model(listing_model: Type[BaseModel]) -> Type[BaseModel]:
    return create_model("DynamicListingContainerModel", listings=(List[listing_model], ...))


def trim_to_token_limit(text: str, model: str = "gpt-4o-mini", token_limit: int = 200_000) -> str:
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)
    if len(tokens) > token_limit:
        trimmed_text = encoder.decode(tokens[:token_limit])
        return trimmed_text
    return text


def format_data(data, DynamicListingsContainer):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    system_message = """You are an intelligent text extraction and conversion assistant. Your task is to extract structured information 
                        from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text, 
                        with no additional commentary, explanations, or extraneous information. 
                        You could encounter cases where you can't find the data of the fields you have to extract or the data will be in a foreign language.
                        Please process the following text and provide the output in pure JSON format with no words before or after the JSON:"""

    user_message = f"Extract the following information from the provided text:\nPage content:\n\n{data}"

    completion = client.beta.chat.completions.parse(
        model=model_used,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        response_format=DynamicListingsContainer
    )
    return completion.choices[0].message.parsed

def save_formatted_data(formatted_data, timestamp, output_folder='output'):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Prepare formatted data as a dictionary
    formatted_data_dict = formatted_data.dict() if hasattr(formatted_data, 'dict') else formatted_data

    # Save the formatted data as JSON with timestamp in filename
    json_output_path = os.path.join(output_folder, f'sorted_data_{timestamp}.json')
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_data_dict, f, indent=4)
    print(f"Formatted data saved to JSON at {json_output_path}")

    # Prepare data for DataFrame
    if isinstance(formatted_data_dict, dict):
        # If the data is a dictionary containing lists, assume these lists are records
        data_for_df = next(iter(formatted_data_dict.values())) if len(formatted_data_dict) == 1 else formatted_data_dict
    elif isinstance(formatted_data_dict, list):
        data_for_df = formatted_data_dict
    else:
        raise ValueError("Formatted data is neither a dictionary nor a list, cannot convert to DataFrame")

    # Create DataFrame
    try:
        df = pd.DataFrame(data_for_df)
        print("DataFrame created successfully.")

        # Save the DataFrame to an Excel file
        excel_output_path = os.path.join(output_folder, f'sorted_data_{timestamp}.xlsx')
        df.to_excel(excel_output_path, index=False)
        print(f"Formatted data saved to Excel at {excel_output_path}")
        
        return df
    except Exception as e:
        print(f"Error creating DataFrame or saving Excel: {str(e)}")
        return None

def calculate_price(input_text, output_text, model=model_used):
    # Initialize the encoder for the specific model
    encoder = tiktoken.encoding_for_model(model)
    
    # Encode the input text to get the number of input tokens
    input_token_count = len(encoder.encode(input_text))
    
    # Encode the output text to get the number of output tokens
    output_token_count = len(encoder.encode(output_text))
    
    # Calculate the costs
    input_cost = input_token_count * pricing[model]["input"]
    output_cost = output_token_count * pricing[model]["output"]
    total_cost = input_cost + output_cost
    
    return input_token_count, output_token_count, total_cost




if __name__ == "__main__":
    url = 'https://news.ycombinator.com/'
    fields=['Title', 'Number of Points', 'Creator', 'Time Posted', 'Number of Comments']

    try:
        # # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Scrape data
        raw_html = fetch_html_selenium(url)
    
        markdown = html_to_markdown_with_readability(raw_html)
        
        # Save raw data
        save_raw_data(markdown, timestamp)

        # Create the dynamic listing model
        DynamicListingModel = create_dynamic_listing_model(fields)

        # Create the container model that holds a list of the dynamic listing models
        DynamicListingsContainer = create_listing_container_model(DynamicListingModel)
        
        # Format data
        formatted_data = format_data(markdown, DynamicListingsContainer)  # Use markdown, not raw_html
        
        # Save formatted data
        save_formatted_data(formatted_data, timestamp)

        # Convert formatted_data back to text for token counting
        formatted_data_text = json.dumps(formatted_data.dict()) 
        
        
        # Automatically calculate the token usage and cost for all input and output
        input_tokens, output_tokens, total_cost = calculate_price(markdown, formatted_data_text, model=model_used)
       

        print(f"Input token count: {input_tokens}")
        print(f"Output token count: {output_tokens}")
        print(f"Estimated total cost: ${total_cost:.4f}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    
