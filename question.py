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


def feedBack():
    f = input("Is the above result relavant?(Y/N)")
    if(f=="Y" or f=="y"):
        return "R"
    elif(f=="N" or f=="n"):
        return "NR"
    else:
        print("Invalid Input. Yy/Nn are valid\n")
        return feedBack()

def query(path,q,fl):
    try:
        tag, q = q.split(':')
    except:
        tag = "total"
    v = get_question(q)
    file = open(f"index/{path}_{tag}_positional_index.json", "r")
    d = json.load(file)
    positional_index = d["positional_index"]
    r, q_len = get_question_vector(positional_index, v)
    docs_len = d["len_docs"]
    r = get_relevance_docs(r, q_len, docs_len)
    tree = ET.parse(f"data/{path}/{path}-abst-v1.2.1.xml")
    root = tree.getroot()
    i = 1

    feed = []
    print(f"{len(r.keys())} results found\n\n")
    cnt = 5
    for docid in r.keys():
        if cnt>0:
            doc = root.find(f".//article[@ocid='{docid}']")
            title = doc.find("./title").text
            abstract = doc.find("./abstract").text
            print(i,". Title:",title,end="\n\n")
            print("Abstract:")
            print(abstract)
            print("-------------------------------------------------------------------")
            i+=1
            if fl==0:
                feed.append(feedBack())
        else:
            x = input("Press Y/y to print more results or N/n to exit")
            if x == "Y" or x == "y":
                cnt = 10
            else:
                break
        cnt-=1
    f = open("ranked_query_docs.txt", "w")
    # max_val = list(r.values())[0] #if you want only the most relavant documents
    for doc in r:
        # if r[doc] < max_val/4:
        #     break
        f.write(doc+"\n")
    f.close()
    file.close()
    return feed
