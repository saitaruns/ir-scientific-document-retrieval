import xml.etree.ElementTree as ET
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import math

total_docs = 0
positional_index = {}
len_docs = {}
d = {"positional_index": positional_index, "len_docs": len_docs}
stopwords = {"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out",
             "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into",
             "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the",
             "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were",
             "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to",
             "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have",
             "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can",
             "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself",
             "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by",
             "doing", "it", "how", "further", "was", "here", "than"}


# input: part of doc/ question, corpus
# this function tokenize the text, remove stopwords and punctuation marks, and add the stems to the corpus
def doc_tokenize(doc, v):
    ps = PorterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    txt = tokenizer.tokenize(doc)
    for index, term in enumerate(txt):
        term = term.lower()
        if term.isalpha() and (term not in stopwords):
            term = ps.stem(term)
            if term not in v:
                v[term] = [0, []]
            v[term][0] += 1
            v[term][1].append(index)

# building the corpus by the specific part (title/ abstract/ fulltext)
def doc_part(v, doc, part):
    txt = doc.findall(f"./{part}")
    doc_tokenize(txt[0].text, v)


# input: document
# output: corpus for the document
def corpus(doc, tag):
    v = {}
    if tag != "total":
        doc_part(v, doc, tag)
    else:
        doc_part(v, doc, "title")
        txt = doc.find("./fulltext")
        segment = txt.findall(".//segment")
        if txt is not None:
            for seg in segment:
                doc_tokenize(seg.text, v)
                # doc_part(v, seg, "segment")
    return v


# input: path to directory that contain the XML files
# the function building inverted index from every XML RECORD in the XML files and compute vector length for them
def add_docs_from_files(path, tag, filename):
    global total_docs
    # doc_list = ['sample-abstract-data', 'sample-fulltext-data']
    if tag == 'total':
        tree = ET.parse(f"{path}/{filename}/{filename}-fulltext-v1.2.1.xml")
    else:
        tree = ET.parse(f"{path}/{filename}/{filename}-abst-v1.2.1.xml")
    root = tree.getroot()
    print(f"Indexing {tag}")
    for doc in root.findall(".//article"):
        total_docs += 1
        v = corpus(doc, tag)
        doc_id = doc.attrib["ocid"]
        max_tf = max([x[0] for x in v.values()])
        for term in v:
            if term not in positional_index:
                # doc-freq, tf, positions
                positional_index[term] = [0, {}, {}]
            positional_index[term][0] += 1
            positional_index[term][1][int(doc_id)] = v[term][0] / max_tf
            positional_index[term][2][int(doc_id)] = v[term][1]
    for term in positional_index:
        positional_index[term][0] = math.log2(total_docs / positional_index[term][0])
        idf = positional_index[term][0]
        for num_doc in positional_index[term][1]:
            tf = positional_index[term][1][num_doc]
            if num_doc not in len_docs:
                len_docs[num_doc] = 0
            len_docs[num_doc] += (idf * tf)**2
    for doc in len_docs:
        len_docs[doc] = math.sqrt(len_docs[doc])


def indexing(path, tag, filename):
    add_docs_from_files(path, tag, filename)
    j = json.dumps(d)
    f = open(f"index/{filename}_{tag}_positional_index.json", "w")
    f.write(j)
    f.close()

def create(path, filename):
    indexing(path, "title", filename)
    indexing(path, "abstract", filename)
    indexing(path, "total", filename)