# scraper.py

from crawler.selenium_crawler import SeleniumCrawler
from handler.converter import HtmlToMarkdownConverter
from handler.fileprocessor import JsonProcessor, RawProcessor
from core.model import DynamicListingModel, DynamicListingContainerModel, Formatter

from settings.config import config

if __name__ == "__main__":
    url = 'https://news.ycombinator.com/'
    fields=['Title', 'Number of Points', 'Creator', 'Time Posted', 'Number of Comments']

    try:
        # # Generate timestamp
        # timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Scrape data
        crawler = SeleniumCrawler()
        raw_html = crawler.get_html(url)

        converter = HtmlToMarkdownConverter()
        markdown = converter.convert(raw_html)
        
        # Save raw data
        raw_processor = RawProcessor()
        raw_processor.write(markdown)

        # Create the dynamic listing model
        DynamicListingModelInstance = DynamicListingModel.create(fields)

        # Create the container model that holds a list of the dynamic listing models
        DynamicListingsContainer = DynamicListingContainerModel.create(DynamicListingModelInstance)
        
        # Format data
        formatter = Formatter()
        formatted_data = formatter.format_data(markdown, DynamicListingsContainer)
        
        # Save formatted data
        json_processor = JsonProcessor()
        json_processor.write(formatted_data)

        # Convert formatted_data back to text for token counting
        formatted_data_text = formatter.get_text(formatted_data) 
        
        
        # Automatically calculate the token usage and cost for all input and output
        input_tokens, output_tokens, total_cost = formatter.calculate_cost(markdown, formatted_data_text, model=config.model_used)
       

        print(f"Input token count: {input_tokens}")
        print(f"Output token count: {output_tokens}")
        print(f"Estimated total cost: ${total_cost:.4f}")

    except Exception as e:
        print(f"An error occurred: {e}")