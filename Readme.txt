IR Scientific Document Retrieval
--------------------------------

Instructions:
-------------

Modules
-------
pip install nltk

Creating Positional Index
-------------------------
python ir_main.py create_index path-of-folder-consisting-of-your-data

eg: python ir_main.py create_index data

Positional index files will be created as 
    title_positional_index.json,
    abstract_positional_index.json,
    total_positional_index.json

Asking query
-------------
1.  python ir_main.py query "tag:query"
    eg: python ir_main.py query "title:Hydrocarbons in Coastal Sediments"

    This will return the documents that contain the query in their tag(title or abstract)
    and order them by their cosine similarity scores.

2. python ir_main.py query -e "tag:query"
    eg: python ir_main.py query -e "abstract:Hydrocarbons in Coastal Sediments"

    -e : evaluation
    Same as above but when added in the arguments, 
    Feedback (Relavent/Non relavent) is taken from the user and the precision and recall is printed

Results are printed into the ranked_query_docs.txt file