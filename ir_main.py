import sys
from question import query
from index_creation import create

if sys.argv[1] == 'create_index':
    create(sys.argv[2])
elif sys.argv[1] == "query":
    if sys.argv[2] == "-e":
        print(query("data",sys.argv[3],0)) #feed back is asked and evaluated
    else:
        query("data",sys.argv[2],1) #feedback is not asked and not evaluated
elif sys.argv[1] == "help":
    print("create_index --> creates index")
    print("query  --> results are printed")
    print("query -e --> results are printed and also evaluated")