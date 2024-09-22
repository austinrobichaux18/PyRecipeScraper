# pip install torch torchvision
# pip install transformers
# pip install scrapegraphai
# pip install playwright 
# pip install nest_asyncio

#This is a comment
print("test")

x = 5
y = "John"
print(x)
print(y)

x = 4       # x is of type int
x = "Sally" # x is now of type str
print(x)

x = "John"
# is the same as
x = 'John'

x = "awesome"
a = x.upper()
def myfunc():
  print("Python is " + x)

myfunc()

class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Drive!")
    
    

import torch
from transformers import pipeline

nlp = pipeline("text-generation", model="t5-base")

# Generate text
generated_text = nlp("Write a short story about")
print(generated_text[0])

nlp = pipeline("summarization", model="t5-base")
print(generated_text[0])

# This will allow you to summarize text using me and the T5-Base model.

# If you want to use me with other models or tasks, you can find them on the Hugging Face Model Hub:
# https://huggingface.co/models



