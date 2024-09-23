import nest_asyncio  # Import nest_asyncio module for asynchronous operations
nest_asyncio.apply()  # Apply nest_asyncio to resolve any issues with asyncio event loop
from scrapegraphai.graphs import SmartScraperGraph

# Configuration dictionary for the graph
graph_config = {
    "llm": {
        "model": "ollama/llama3.1",  # Specify the model for the llm
        "temperature": 0,  # Set temperature parameter for llm
        "format": "json",  # Specify the output format as JSON for Ollama
        "base_url": "http://localhost:11434",  # Set the base URL for Ollama
    },
    # "embeddings": {
    #     "model": "ollama/nomic-embed-text",  # Specify the model for embeddings
    #     "base_url": "http://localhost:11434",  # Set the base URL for Ollama
    # },
    "verbose": True,  # Enable verbose mode for debugging purposes
    # "headless": False,
}


# Initialize SmartScraperGraph with prompt, source, and configuration
smart_scraper_graph = SmartScraperGraph(
    #prompt="List all the content",  # Set prompt for scraping
    prompt="return all the urls for recipes",
    # prompt="list me all the video titles and description",
    # Source URL or HTML content to scrape
    #source="https://github.com/InsightEdge01",
    # source="https://www.youtube.com/results?search_query=path+of+exile",
      source="https://www.allrecipes.com/recipe/274966/sheet-pan-parmesan-chicken-and-veggies/",
    #  source = content,
    config=graph_config, # Pass the graph configuration
)

# Run the SmartScraperGraph and store the result
result = smart_scraper_graph.run()


# Print the result
print(result)
print()

# Prettify the result and display the JSON
import json
output = json.dumps(result, indent=2)  # Convert result to JSON format with indentation
line_list = output.split("\n")  # Split the JSON string into lines
# Print each line of the JSON separately
for line in line_list:
    print(line)
 