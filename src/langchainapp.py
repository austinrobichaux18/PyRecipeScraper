import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, field_validator
from bs4 import BeautifulSoup as bs
import markdownify 
import requests

#"https://r.jina.ai/" +
# url =  "https://www.allrecipes.com/recipe/274966/sheet-pan-parmesan-chicken-and-veggies/"

url = "https://www.allrecipes.com/recipe/283464/easy-plum-cake/"

# get the recipe from the url
web_content = requests.get(url).text
web_text = bs(web_content, "html.parser").get_text()

article = bs(web_content, "html.parser").find("article").encode_contents()

web_text = markdownify.markdownify(article, heading_style="ATX") 

model = OllamaLLM(
                model = "llama3.1",
                temperature = 0,
                verbose=True,
            )
 
class Ingredient(BaseModel):
    name:str= Field(description="name of ingredient")
    quantity:str= Field(description="quantity of measurement")
    measurement:str= Field(description="measurement of ingredient")


class Direction(BaseModel):
     number:str= Field(description="step number")
     detail:str= Field(description="step information detail")


class Recipe(BaseModel):
    ingredients:list[Ingredient]= Field(description="ingredients")
    directions:list[Direction]= Field(description="directions")
    @field_validator("ingredients")
    def validate_ingredients(cls, v):
        if len(v) == 0:
            raise ValueError("There must be at least one ingredient.")
        return v
    
    @field_validator("directions")
    def validate_steps(cls, v):
        if len(v) == 0:
            raise ValueError("There must be at least one direction.")
        return v

# And a query intented to prompt a language model to populate the data structure.
query = web_text

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Recipe)

prompt = PromptTemplate(
    template="Find the main content of this webpage. Transcribe the recipe from it. \n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
 
chain = prompt | model | parser

result = chain.invoke({"query": query})
data = json.dumps(result, indent=2)

with open("Output.json", "w") as my_file:
    my_file.write(data)

# # Prettify the result and display the JSON
# import json
# output = json.dumps(result, indent=2)  # Convert result to JSON format with indentation
# line_list = output.split("\n")  # Split the JSON string into lines
# # Print each line of the JSON separately
# for line in line_list:
#     print(line)
 