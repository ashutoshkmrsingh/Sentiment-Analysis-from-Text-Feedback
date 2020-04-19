from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from statistics import mean
from string import punctuation

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

aspect_mobile = {('camera','photography'):[0, 0, 0],('battery'):[0, 0, 0],('display','screen','picture','look','design','UI','touch'):[0, 0, 0],
                 ('charge', 'charging', 'power','discharing'):[0, 0, 0],
                 ('sound','speaker','mic','microphone','music','voice'):[0, 0, 0],('processor','storage','performance','heating','hanging '):[0,0,0],
                 ('money','budget','price'):[0,0,0],('unlocking','finger print','sensor','unlock'):[0,0,0]}


def aspect_cal(input_):
        sent_analyzer = SentimentIntensityAnalyzer()

        input_=input_.replace(' but ',',')

        tokenize_list =word_tokenize (input_)

        #print(tokenize_list)

        try:
            if tokenize_list[1]=='and':
                split_list = input_.split('.')
            else:
                split_list = input_.split(' and ')
        except Exception:
            split_list = input_
        #print(split_list)

        l=[]
        for sentence in split_list:
        #print(sentence)
            remove_punctuation = strip_punctuation(sentence)
            sent_=remove_punctuation.lower()
            for word in sent_.split(' '):
                #print(word)
                for key,value in aspect_mobile.items():
                    if word in key:
                        #print(key,word)
            #                 l.append(word)
                        if word=='':
                            continue
                        else:
                            #print(remove_punctuation)
                            polarity = sent_analyzer.polarity_scores(remove_punctuation)

                            #print(word)
                            count_=input_.count(word)
                            for key_,value_ in polarity.items():
                                if key_=='neg':
                                    if count_>1:
                                        value[0]+=value_/count_
                                    else:
                                        value[0]+=value_
                                elif key_=='neu':
                                    if count_>1:
                                        value[1]+=value_/count_
                                    else:
                                        value[1]+=value_
                                elif key_=='pos':
                                    if count_>1:
                                        value[2]+=value_/count_
                                    else:
                                        value[2]+=value_
                                    break
        return aspect_mobile
# input_ = input()
# aspect_cal(input_)