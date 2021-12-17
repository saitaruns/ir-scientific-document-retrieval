def evaluate(relevance):
    tot_rel = 0
    for x in relevance:
        if x == 'R' :
            tot_rel += 1

    is_relevant = 0
    
    print("-------------------------------------------------------------------")
    print('The evaluation of our results for the given feedback is: \n')
    print("index precision recall")
    for index,value in enumerate(relevance):
        if value == 'R':
            is_relevant += 1
        precision = is_relevant/(index + 1)
        precision = "{:.2f}".format(precision)
        recall = is_relevant/(tot_rel)
        print(str(index+1) + '      ' + str(precision) + '      ' + str(recall))
