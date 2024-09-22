import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, field_validator
from bs4 import BeautifulSoup as bs
import markdownify 
import requests

def get_recipe(url):
    # get the recipe from the url
    web_content = requests.get(url).text
    
    doc = bs(web_content, "html.parser")

    ingredients = doc.find("div", id="mm-recipes-structured-ingredients_1-0").encode_contents()
    directions = doc.find("div", id="mm-recipes-steps_1-0").encode_contents()

    ingredients_web_text = markdownify.markdownify(ingredients, heading_style="ATX")
    directions_web_text = markdownify.markdownify(directions, heading_style="ATX")


    model = OllamaLLM(model="llama3.1", temperature=0) # llama3.1:8b-instruct-q2_K

    class Ingredient(BaseModel):
        name: str = Field(description="the name of the ingredient")
        quantity: int = Field(description="the quantity of the ingredient. list this field as a decimal value. ex: 1.0, 0.4, etc.")
        unit: str = Field(description="the unit of the ingredient. ex: cup, tbsp, slices, whole items, to taste, pinch, etc.")
        special_instructions: str = Field(description="any special instructions for the ingredient. example, butter is melted, chopped, etc.")
        
        @field_validator("quantity")
        def validate_quantity(cls, v):
            if isinstance(v, str):
                # try to convert the string to a number
                try:
                    v = float(v)
                except ValueError:
                    raise ValueError("The quantity must be a number.")
                return v
            else:
                return v
            

    class Step(BaseModel):
        description: str = Field(description="the step description")

    # Define your desired data structure.
    class Recipe(BaseModel):
        ingredients: list[Ingredient] = Field(description="a list of recipe ingredients")
        
        @field_validator("ingredients")
        def validate_ingredients(cls, v):
            if len(v) == 0:
                raise ValueError("There must be at least one ingredient.")
            return v

    class RecipeSteps(BaseModel):
        title: str = Field(description="the title of the recipe")
        steps: list[Step] = Field(description="a list of steps to follow to make the recipe")

    # Set up a parser + inject instructions into the prompt template.
    ingredients_parser = JsonOutputParser(pydantic_object=Recipe)

    ingredients_prompt = PromptTemplate(
        template="Here is a webpage that contains a recipe. Find the ingredients listed in the recipe. only print the json with no additional commentary. \n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": ingredients_parser.get_format_instructions()},
    )

    ingredient_chain = ingredients_prompt | model | ingredients_parser

    recipe_parser = JsonOutputParser(pydantic_object=RecipeSteps)
    recipe_prompt = PromptTemplate(
        template="Here is a webpage that contains a recipe. List the to steps to create the recipe. only print the json with no additional commentary. \n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": recipe_parser.get_format_instructions()},
    )
    recipe_chain = recipe_prompt | model | recipe_parser


    ingredients_result = ingredient_chain.invoke({"query": ingredients_web_text})

    recipe_result = recipe_chain.invoke({"query": directions_web_text})

    print(json.dumps(ingredients_result, indent=2))
    print(json.dumps(recipe_result, indent=2))
    
# get_recipe("https://www.allrecipes.com/recipe/244520/belizean-chicken-stew/")
# get_recipe("https://www.allrecipes.com/recipe/15181/famous-chicken-francaise/")
# get_recipe("https://www.allrecipes.com/country-ham-and-biscuits-recipe-8707673")
get_recipe("https://www.allrecipes.com/recipe/274966/sheet-pan-parmesan-chicken-and-veggies/")

