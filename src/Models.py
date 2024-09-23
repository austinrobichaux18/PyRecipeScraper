
from typing import List

# DB Models
class DoubleStringConvert:
    def __init__(self, one: str, two: str):
        self.one = one
        self.two = two

class RecipeItemConvert:
    def __init__(self, instructions: List[str], ingredients: List[DoubleStringConvert]):
        self.instructions = instructions
        self.ingredients = ingredients

class RecipeConvert:
    def __init__(self, 
                 id: int, 
                 url: str, 
                 servings: int, 
                 cook_time_minutes: int, 
                 title: str, 
                 images: List[str], 
                 thumbnail_url: str, 
                 items: List[RecipeItemConvert], 
                 topic_url: str, 
                 topic: str, 
                 tag1: str):
        self.id = id
        self.url = url
        self.servings = servings
        self.cook_time_minutes = cook_time_minutes
        self.title = title
        self.images = images
        self.thumbnail_url = thumbnail_url
        self.items = items
        self.topic_url = topic_url
        self.topic = topic
        self.tag1 = tag1
        

# DTO Models
class DoubleString:
    def __init__(self, one: str, two: str):
        self.one = one
        self.two = two

class RecipeItem:
    def __init__(self, instructions: List[str], ingredients: List[DoubleString]):
        self.instructions = instructions
        self.ingredients = ingredients

class Recipe:
    def __init__(self, 
                 id: int, 
                 url: str, 
                 servings: int, 
                 cook_time_minutes: int, 
                 title: str, 
                 images: List[str], 
                 thumbnail_url: str, 
                 items: List[RecipeItem], 
                 topic_url: str, 
                 topic: str, 
                 tag1: str, 
                 cols: int, 
                 rows: int):
        self.id = id
        self.url = url
        self.servings = servings
        self.cook_time_minutes = cook_time_minutes
        self.title = title
        self.images = images
        self.thumbnail_url = thumbnail_url
        self.items = items
        self.topic_url = topic_url
        self.topic = topic
        self.tag1 = tag1
        self.cols = cols
        self.rows = rows
