import sys
from question import query
from index_creation import create

if sys.argv[1] == 'create_index':
    create(sys.argv[2])
elif sys.argv[1] == "query":
    query("data",sys.argv[2])