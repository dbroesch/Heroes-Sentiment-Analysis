import operator, json, vincent, math
from collections import Counter
from collections import defaultdict
from preProcess import *
from nltk import bigrams 


def file_len(fname):
    'Reads the number of lines in a file'
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return (i + 1)/2


def mostCommon(hashtag):
   'Prints the most common terms in a given terms list'
   tweetList= hashtagSearch(hashtag)
   terms_all = [term for term in pp(tweetList)]
   count_all.update(terms_all)
   print(count_all.most_common(5))

def term_count(twitterJson):
    'Creates a dictionary with terms as keys and the number of times they appear as values'
    fname = twitterJson
    with open(fname, 'r') as f:
        count_all = Counter()
        count_bigrams= Counter()
        num_tweets = 0
        for line in f:
            try:
                tweet = json.loads(line)
                num_tweets+=1
            except ValueError:
                continue
            # Create a list with all the terms
            terms_all = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@'))]
            # Update the counter
            count_all.update(terms_all)
            count_bigrams.update(bigrams(terms_all))
    return count_all

        
       
def co_occurrences(file):
    'Calculates a term Co-occurence dictionary'
    com = defaultdict(lambda : defaultdict(int))
    with open(file, 'r') as f:
        num_tweets = 0
        for line in f:
            try:
                tweet = json.loads(line)
                num_tweets+=1
            except ValueError:
                continue
            # Create a list with all the terms
            terms_only = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@'))]

            #build co-occurrence matrix
            for i in range(len(terms_only)-1):
                for j in range(i+1, len(terms_only)):
                    w1, w2 = sorted([terms_only[i], terms_only[j]])
                    if w1 != w2:
                        com[w1][w2] +=1
    com_max = []
    #for each term, look for the most common co-occurent terms
    for t1 in com:
        t1_max_terms = max(com[t1].items(), key=operator.itemgetter(1))[:5]
        for t2 in t1_max_terms:
            com_max.append(((t1,t2),com[t1][t2]))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    print(terms_max[:5])



def graphs(twitterJson):
    'Generates a graph with Vincent for use in Jscript'
    fname = twitterJson
    with open(fname, 'r') as f:
        count_all = Counter()
        count_bigrams= Counter()
        for line in f:
            try:
                tweet = json.loads(line)
                num_tweets+=1
            except ValueError:
                continue
            # Create a list with all the terms
            terms_all = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@'))]
            # Update the counter
            count_all.update(terms_all)
            count_bigrams.update(bigrams(terms_all))
        word_freq = count_all.most_common(20)
        labels, freq = zip(*word_freq)
        data = {'data': freq, 'x': labels}
        bar = vincent.Bar(data, iter_idx = 'x')
        bar.to_json("term_freq.json")


def ListGen(txtFile):
    'Generates a list from a text file of words'
    with open(txtFile, 'r') as f:
        pos_list = f.read().splitlines()
    return pos_list


def SO(twitterJson):
    'Calculates the semantic orientation of terms using PMI'
    com = defaultdict(lambda : defaultdict(int))
    fname = twitterJson
    with open(fname, 'r') as f:
        count_all = Counter()
        count_bigrams= Counter()
        tweet_terms= []
        num_tweets=0
        for line in f:
            try:
                tweet = json.loads(line)
                num_tweets+=1
            except ValueError:
                continue
            # Create a list with all the terms
            terms_only = [term for term in preprocess(tweet['text'], lowercase=True) if term not in stop and not term.startswith(('#', '@'))]
            tweet_terms.append(terms_only)
            count_all.update(terms_only)
            #build co-occurrence matrix
            for i in range(len(terms_only)-1):
                for j in range(i+1, len(terms_only)):
                    w1, w2 = sorted([terms_only[i], terms_only[j]])
                    if w1 != w2:
                        com[w1][w2] +=1
    #Calculate the probabily of terms and term co-occurences with good/bad lists        
    p_t={}
    p_t_com = defaultdict(lambda : defaultdict(int))

    for term, n in count_all.items():
        p_t[term] = n/ num_tweets
        for t2 in com[term] :
            p_t_com[term][t2] = com[term][t2] / num_tweets

    positive_vocab = ListGen("positive-words.txt")
    negative_vocab = ListGen("negative-words.txt")

    pmi = defaultdict(lambda : defaultdict(int))
    for t1 in p_t:
        for t2 in com[t1]:
            denom = p_t[t1] * p_t[t2]
            pmi[t1][t2] = math.log2(p_t_com[t1][t2]/denom)

    #Calculates Semantic orientation
    semantic_orientation = {}
    for term, n in p_t.items():
        positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
        negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
        semantic_orientation[term] = positive_assoc-negative_assoc
    return semantic_orientation

def semantic_extremes(orientation_dict):
    'Prints the terms with the highest and lowest sentiment scores'
    semantic_sorted = sorted(orientation_dict.items(), key=operator.itemgetter(1), reverse=True)
    top_pos = semantic_sorted[:10]
    top_neg = semantic_sorted[-10:]
    print(top_pos)
    print(top_neg)

def char_SO(orientation_dict,term_count):
    'creates a dictionary of hero nicknames and associated sentiment scores'
    character_sentiment = {}
    for x in character_names.values():
        for val in x:
            for y,z in orientation_dict.items():
                if y == val.lower():
                    character_sentiment.update({y:[z]})

    for x,y in character_sentiment.items():
        for z,a in term_count.items():
            if z == x:
                character_sentiment[x].append(a)

    #condenses nick names entries into a dictonary of hero names as keys, and a list of lists of sentiment scores and occurences for each nickname. ex: Kael'Thas: [[sent#1,occ1],[sent#2,occ#2]]
    cond_char_sent= {}
    for x,y in character_sentiment.items():
        for a,z in character_names.items():
            for val in z:
                if x==val.lower():
                    if a in cond_char_sent:
                        cond_char_sent[a].append(y)
                    else:
                     temp = {a:[list(y)]}
                     cond_char_sent.update(temp)
    #print(cond_char_sent)    
    #print("SEPERATOR!!! \n \n")

    #calculates a weighted arithmetic mean of the sentiment scores for the different hero nicknames
    avg_char_sent={}
    for x,y in cond_char_sent.items():
        numer=0
        denom=0
        for vals in y:
            numer += vals[0]*vals[1]
            denom += vals[1]
        temp = [numer/denom,denom]
        temp_dict={x:temp}
        avg_char_sent.update(temp_dict)
    print(avg_char_sent)

    #formats and writes sentiment dictionary to csv file format for external editing
    with open("char_sent.txt", 'w') as f:
        for x,y in avg_char_sent.items():
            f.write("%s,%s,%s\n" % (x,y[0],y[1]))
        

