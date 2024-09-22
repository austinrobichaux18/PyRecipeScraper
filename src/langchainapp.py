from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
import requests

url = "https://r.jina.ai/" + "https://www.allrecipes.com/recipe/274966/sheet-pan-parmesan-chicken-and-veggies/"

pageContents :str =""
try:
    response = requests.get(url)
    response.raise_for_status()

    chunk_size = 1024
    for chunk in response.iter_content(chunk_size=chunk_size):
        pageContents+=chunk.decode("utf-8")  # get the content chunk by chunk
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")
    
model = ChatOllama(
                model = "llama3.1",
                temperature = 0,
                verbose=True,
                # other params ...
            )
 
# messages = [
#                 ("system", "You are a chef teacher. Read the contents and output the ingredients and the directions"),
#                 ("contents", pageContents),
#             ]

query = "read the following and output only the ingredients and directions: " + pageContents
# model.invoke(messages)
 
# Define your desired data structure.
# class Joke(BaseModel):
#     setup: str = Field(description="question to set up a joke")
#     punchline: str = Field(description="answer to resolve the joke")


# And a query intented to prompt a language model to populate the data structure.
# joke_query = "Tell me a joke."

class Ingredient(BaseModel):
    name:str= Field(description="name of ingredient")
    quantity:str= Field(description="quantity of measurement")
    measurement:str= Field(description="measurement of ingredient")


class Direction(BaseModel):
     number:str= Field(description="step number")
     detail:str= Field(description="step information detail")


class Result(BaseModel):
    ingredients:list[Ingredient]= Field(description="ingredients")
    directions:list[Direction]= Field(description="directions")


# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Result)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

result = chain.invoke({"query": query})
print(result)

# # Prettify the result and display the JSON
# import json
# output = json.dumps(result, indent=2)  # Convert result to JSON format with indentation
# line_list = output.split("\n")  # Split the JSON string into lines
# # Print each line of the JSON separately
# for line in line_list:
#     print(line)
 