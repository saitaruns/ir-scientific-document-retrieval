import math
from index_creation import doc_tokenize
import json
import xml.etree.ElementTree as ET


# building corpus for the question
def get_question(question):
    v = {}
    doc_tokenize(question, v)
    return v


# create vector of relevance document for the question and compute his length

#gold damaged
def get_question_vector(positional_index, v):
    r = {}
    q_len = 0
    for term in v: #{shipment : [1,[]] ,gold : 1, damaged: 1}
        if term in positional_index:
            idf = positional_index[term][0]
        else:
            continue
        tf = v[term][0]
        w = idf * tf # vector value of query of this term
        q_len += w ** 2
        docs = positional_index[term][1] # docs consisting of term
        for doc in docs:
            if doc not in r:
                r[doc] = 0
            q_score = idf * docs[doc] # vector value of doc of this term
            r[doc] += w * q_score  # dot product of this term
    q_len = math.sqrt(q_len)
    return r, q_len


# compute cosine similarity for every document in the vector of relevance documents and sort them
def get_relevance_docs(r, q_len, docs_len):
    for doc in r:
        s = r[doc]
        doc_len = docs_len[doc]
        r[doc] = s / (doc_len * q_len)
    return dict(sorted(r.items(), key=lambda item: item[1], reverse=True))


# call the rest of the functions in this file and writing to output file all relevance documents with score higher
# than the threshold
# title: query split(:)[1]

# def queryProcess(q):
#     try:
#         tag, q = q.split(':')
#     except:
#         tag = "total"
    
#     return 

def query(path,q):
    try:
        tag, q = q.split(':')
    except:
        tag = "total"
    v = get_question(q)
    file = open(f"{tag}_positional_index.json", "r")
    d = json.load(file)
    positional_index = d["positional_index"]
    r, q_len = get_question_vector(positional_index, v)
    docs_len = d["len_docs"]
    r = get_relevance_docs(r, q_len, docs_len)
    tree = ET.parse(f"{path}/sample-abstract-data.xml")
    root = tree.getroot()
    i = 1
    for docid in r.keys():
        doc = root.find(f".//article[@ocid='{docid}']")
        title = doc.find("./title").text
        abstract = doc.find("./abstract").text
        print(i,"Title\n",title,end="\n")
        print(" Abstract\n",abstract)
        print("-------------------------------------------------------------------")
        i+=1
    
    
        # print(topic)
    f = open("ranked_query_docs.txt", "w")
    # max_val = list(r.values())[0]
    for doc in r:
        # if r[doc] < max_val/4:
        #     break
        f.write(doc+"\n")
    f.close()
    file.close()
