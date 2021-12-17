import sys
from question import query
from index_creation import create
from evaluation import evaluate

if sys.argv[1] == 'create_index':
    create(sys.argv[2], sys.argv[3])
elif sys.argv[1] == "query":
    if sys.argv[2] == "-e":
        relevance = query(sys.argv[3],sys.argv[4],0) #feed back is asked and evaluated
        evaluate(relevance)
    else:
        query(sys.argv[2],sys.argv[3],1) #feedback is not asked and not evaluated
elif sys.argv[1] == "help":
    print("create_index --> creates index")
    print("query  --> results are printed")
    print("query -e --> results are printed and also evaluated")