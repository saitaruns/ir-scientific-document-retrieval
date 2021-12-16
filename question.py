import math
from index_creation import doc_tokenize
import json


# building corpus for the question
def get_question(question):
    v = {}
    doc_tokenize(question, v)
    return v


# create vector of relevance document for the question and compute his length
def get_question_vector(positional_index, v):
    r = {}
    q_len = 0
    for term in v:
        if term in positional_index:
            idf = positional_index[term][0]
        else:
            continue
        tf = v[term][0]
        w = idf * tf
        docs = positional_index[term][1]
        for doc in docs:
            if doc not in r:
                r[doc] = 0
            q_score = idf * docs[doc]
            r[doc] += w * q_score
            q_len += q_score
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
def query(q):
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
    f = open("ranked_query_docs.txt", "w")
    # max_val = list(r.values())[0]
    for doc in r:
        # if r[doc] < max_val/4:
        #     break
        f.write(doc+"\n")
    f.close()
    file.close()
