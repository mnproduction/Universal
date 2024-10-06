# core/model.py

from typing import List, Type

from openai import OpenAI
from pydantic import BaseModel, create_model
import tiktoken

from settings.config import ModelConfig, config, pricing

class DynamicListingModel(BaseModel):
    def create(self, field_names: List[str]) -> Type[BaseModel]:
        field_definitions = {field: (str, ...) for field in field_names}
        return create_model("DynamicListingModel", **field_definitions)

class DynamicListingContainerModel(BaseModel):
    def create(self, listing_model: Type[BaseModel]) -> Type[BaseModel]:
        return create_model("DynamicListingContainerModel", listings=(List[listing_model], ...))

class Trimmer():
    def __init__(self, model: str = "gpt-4o-mini", token_limit: int = 200_000):
        self.model = model
        self.token_limit = token_limit

    def to_token_limit(self, text: str) -> str:
        encoder = tiktoken.encoding_for_model(self.model)
        tokens = encoder.encode(text)
        if len(tokens) > self.token_limit:
            trimmed_text = encoder.decode(tokens[:self.token_limit])
            return trimmed_text
        return text

class Formatter():
    def __init__(self, 
                 data: str, 
                 dynamic_listing_container_model: Type[DynamicListingContainerModel], 
                 model: str = "gpt-4o-mini", 
                 ):
        self.data = data
        self.model = model
        self.model_config = ModelConfig(data)
        self.dynamic_listing_container_model_class = dynamic_listing_container_model  # Store the class type

    def format_data(self) -> str:
        client = OpenAI(api_key=config.OPENAI_API_KEY)

        system_message = self.model_config.system_message
        user_message = self.model_config.user_message

        # Create an instance of the dynamic listing container model
        dynamic_listing_container_instance = self.dynamic_listing_container_model_class()  # Instantiate the model class


        completion = client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            response_format=dynamic_listing_container_instance
        )

        return completion.choices[0].message.parsed


    def calculate_cost(self, input_text: str, output_text: str, model: str = "gpt-4o-mini") -> float:
        encoder = tiktoken.encoding_for_model(model)
        input_token_count = len(encoder.encode(input_text))
        output_token_count = len(encoder.encode(output_text))
        input_cost = input_token_count * pricing[model]["input"]
        output_cost = output_token_count * pricing[model]["output"]
        total_cost = input_cost + output_cost
        
        return input_token_count, output_token_count, total_cost

