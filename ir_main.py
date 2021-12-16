import sys
from index_creation import create

if sys.argv[1] == 'create_index':
    create(sys.argv[2])