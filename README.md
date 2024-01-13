# Graph analysis - Chefs

# Description
This project uses graph analysis techniques to visualize the relation between different chefs. Under the html/ folder
you will find an interactive visualization of a chefs graph that can be customized to watch the effects of different
graph properties.

## Data
Extrated from Facebook, it includes links between different chefs and restaurants. Original data can be found here: http://networkrepository.com/fb-pages-food.php

The data has been processed into 2 datasets under fb-pages-food: nodes and edges.

Additional data:
- Restaurant and chef nationality
- Difference between restaurant and chef
- Images

## Script
To process and extract the necessary information from the initial files, the script graph_to_json.py has been used.
This program calculates graph features and saves the information in different JSON files (in the "json" folder) that will later be used for visualization.

There are two different JSON files because at a certain point, the decision was made to simplify the graph by grouping
nodes from the same chain or restaurant into a single one.

## Visualization
The visualization of the various proposed graphs can be found in html/graphs.html.
Various visualizations have been suggested based on the data, along with the option to configure aspects of the graph.