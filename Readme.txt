IR Scientific Document Retrieval
--------------------------------

Instructions:
-------------

Modules
-------
pip install nltk

Creating Positional Index
-------------------------
python ir_main.py create_index data-folder folder-consisting-of-xml-documents 

eg: python ir_main.py create_index data elsevier

Positional index files will be created as 
    elsevier_title_positional_index.json,
    elsevier_abstract_positional_index.json,
    elsevier_total_positional_index.json

Asking query
-------------
1.  python ir_main.py query folder-consisting-of-xml-documents "tag:query"
    eg: python ir_main.py query elsevier "title:Hydrocarbons in Coastal Sediments"

    This will return the documents that contain the query in their tag(title or abstract)
    and order them by their cosine similarity scores.

2. python ir_main.py query -e folder-consisting-of-xml-documents "tag:query"
    eg: python ir_main.py query -e elsevier "abstract:Hydrocarbons in Coastal Sediments"

    -e : evaluation
    Same as above but when added in the arguments, 
    Feedback (Relavent/Non relavent) is taken from the user and the precision and recall is printed

Results are also printed into the ranked_query_docs.txt file