# adapted from Marco Bonzanini's blog post 'http://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/'
#uses Bing Liu's good/bad term list' https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon'
import re
from nltk.corpus import stopwords
import string
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
 
def file_len(fname):
    #reads the number of lines in a file
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via','RT'] +['1','2','3','4','5','6','7','8','9','10']

character_names = {'Li-Ming':['Li-Ming','Li Ming', 'Ming Li','LiMing'],
                   'Greymane':['Greymane','Genn','Graymane'],
                   'Lunara':['Lunara'],
                   'Cho\'Gall':['Cho\'Gall','ChoGall','Cho Gall','Cho','Gall'],
                   'Artanis':['Artanis'],
                   'Lt. Morales':['Lt. Morales','Lt.Morales','Lt Morales','Medic','Morales'],
                   'Rexxar': ['Rexxar'],
                   'Kharazim':['Kharazim','Khara','Monk'],
                   'Leoric':['Leoric'],
                   'Butcher':['Butcher'],
                   'Johanna':['Johanna','Jo','Crusader'],
                   'Kael\'Thas':['Kael\'Thas','KaelThas','Kael','KT'],
                   'Sylvanas':['Sylvanas','Sylv'],
                   'The Lost Vikings':['The Lost Vikings','Vikings','TLV'],
                   'Thrall':['Thrall'],
                   'Jaina':['Jaina'],
                   'Anub\'Arak':['Anub\'Arak','AnubArak','Anub','Nerub'],
                   'Azmodan':['Azmodan','Azmo'],
                   'Chen':['Chen'],
                   'Rehgar':['Rehgar','Rehgod'],
                   'Zagara':['Zagara','Zag','Zags'],
                   'Murky':['Murky'],
                   'Brightwing':['Brightwing','BW'],
                   'Li Li':['Li Li','LiLi'],
                   'Tychus':['Tychus'],
                   'Stitches':['Stitches'],
                   'Arthas':['Arthas'],
                   'Diablo':['Diablo'],
                   'Tyrael':['Tyrael'],
                   'E.T.C.':['E.T.C.','ETC'],
                   'Sonya':['Sonya','Barbarian','Barb'],
                   'Muradin':['Muradin','Mura'],
                   'Kerrigan':['Kerrigan','Kerri'],
                   'Nova':['Nova'],
                   'Falstad':['Falstad'],
                   'Valla':['Valla'],
                   'Illidan':['Illidan','Illi','Illy'],
                   'Raynor':['Raynor','Jim','Jimmy'],
                   'Zeratul':['Zeratul','Zera'],
                   'Uther':['Uther'],
                   'Malfurion':['Malfurion','Malf'],
                   'Tassadar':['Tassadar','Tass'],
                   'Tyrande':['Tyrande'],
                   'Nazeebo':['Nazeebo','Naz'],
                   'Gazlowe':['Gazlowe'],
                   'Abathur':['Abathur','Abba','Abby','Slug'],
                   'Sgt. Hammer':['Sgt. Hammer','Sgt Hammer','SgtHammer','Hammer'],
                   }

test_dict = {"Zag" : 10,
             "Malf" : 20,
             "Li Ming": 30,
             "kakles" : 40
             }