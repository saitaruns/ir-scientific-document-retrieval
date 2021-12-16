# IR Scientific Document Retrieval

## Instructions

### Creating Inverted Index

> python ir_main.py create_index path-of-folder-consisting-of-your-data

eg: python ir_main.py create_index data

Inverted index will be created into inverted_index.json

### Asking query

> python ir_main.py query "tag:query"

eg: python ir_main.py query "title:Hydrocarbons in Coastal Sediments"