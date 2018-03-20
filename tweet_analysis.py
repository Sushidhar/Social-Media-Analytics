# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:15:18 2017

@author: Sushidhar
"""


import json
import re
from nltk.stem.porter import PorterStemmer
import string
import gensim
from gensim import corpora
from wordcloud import WordCloud
import matplotlib.pyplot
from textblob import TextBlob
import scipy as sc
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
ps = PorterStemmer()

allStopWords={'amp':1, 'donaldtrump':1, 'taguser':1, 'atuser':1, '':1, 'a':1, 'url':1, 'rt':1, 'donald':1, 'trump':1, 'trumps':1, 'about':1, 'above':1, 'after':1, 'again':1, 'against':1, 'just':1, 'will':1, 'now':1, 'all':1, 'am':1, 'an':1, 'and':1, 'any':1, 'are':1, 'arent':1, 'as':1, 'at':1, 'be':1, 'because':1, 'been':1, 'before':1, 'being':1, 'below':1, 'between':1, 'both':1, 'but':1, 'by':1, 'cant':1, 'cannot':1, 'could':1, 'couldnt':1, 'did':1, 'didnt':1, 'do':1, 'does':1, 'doesnt':1, 'doing':1, 'dont':1, 'down':1, 'during':1, 'each':1, 'few':1, 'for':1, 'from':1, 'further':1, 'had':1, 'hadnt':1, 'has':1, 'hasnt':1, 'have':1, 'havent':1, 'having':1, 'he':1, 'hed':1, 'hell':1, 'hes':1, 'her':1, 'here':1, 'heres':1, 'hers':1, 'herself':1, 'him':1, 'himself':1, 'his':1, 'how':1, 'hows':1, 'i':1, 'id':1, 'ill':1, 'im':1, 'ive':1, 'if':1, 'in':1, 'into':1, 'is':1, 'isnt':1, 'it':1, 'its':1, 'its':1, 'itself':1, 'lets':1, 'me':1, 'more':1, 'most':1, 'mustnt':1, 'my':1, 'myself':1, 'no':1, 'nor':1, 'not':1, 'of':1, 'off':1, 'on':1, 'once':1, 'only':1, 'or':1, 'other':1, 'ought':1, 'our':1, 'ours ':1, 'ourselves':1, 'out':1, 'over':1, 'own':1, 'same':1, 'shant':1, 'she':1, 'shed':1, 'shell':1, 'shes':1, 'should':1, 'shouldnt':1, 'so':1, 'some':1, 'such':1, 'than':1, 'that':1, 'thats':1, 'the':1, 'their':1, 'theirs':1, 'them':1, 'themselves':1, 'then':1, 'there':1, 'theres':1, 'these':1, 'they':1, 'theyd':1, 'theyll':1, 'theyre':1, 'theyve':1, 'this':1, 'those':1, 'through':1, 'to':1, 'too':1, 'under':1, 'until':1, 'up':1, 'very':1, 'was':1, 'wasnt':1, 'we':1, 'wed':1, 'well':1, 'were':1, 'weve':1, 'were':1, 'werent':1, 'what':1, 'whats':1, 'when':1, 'whens':1, 'where':1, 'wheres':1, 'which':1, 'while':1, 'who':1, 'whos':1, 'whom':1, 'why':1, 'whys':1, 'with':1, 'wont':1, 'would':1, 'wouldnt':1, 'you':1, 'youd':1, 'youll':1, 'youre':1, 'youve':1, 'your':1, 'yours':1, 'yourself':1, 'yourselves':1}
outLst = []

class tweetAnalysis:
    
    
    def replaceString(self,tweet):
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',tweet)
        tweet = re.sub('@[^\s]+','atuser',tweet)
        tweet = re.sub('#[^\s]+','taguser',tweet)
        return tweet
    

    def cleanData(self,dataJson):
        for dict in dataJson:
            tweets = dict['text'].encode('utf-8')
            tweets = tweets.decode('unicode_escape').encode('ascii','ignore')
            tweets = re.sub(",", " ", tweets)
            tweet = tweets.split()
            lst = []
            for word in tweet:
                word = word.lower()
                word = self.replaceString(word)
                word = word.translate(None,string.punctuation)
                word = word.translate(None,string.digits)
                word = re.sub('[\s]+', ' ', word)
                word = word.strip('\'"')
                if word not in allStopWords:
                    lst.append(word)
            outLst.append(lst)
    
    def sentimentAnalysis(self,outLst):
        sub = []
        pol = []
        for tweet in outLst:
            tweets = ''
            for word in tweet:
                tweets += '{} '.format(word)
            sub.append(TextBlob(tweets).subjectivity)
            pol.append(TextBlob(tweets).polarity)
        print ("average subjectivty: {} " .format(sc.mean(sub)))
        print ("average polarity: {}" .format(sc.mean(pol)))
        matplotlib.pyplot.hist(sub, bins=20) 
        matplotlib.pyplot.xlabel('subjectivity score')
        matplotlib.pyplot.ylabel('tweet count')
        matplotlib.pyplot.grid(True)
        matplotlib.pyplot.show()
        matplotlib.pyplot.hist(pol, bins=20) 
        matplotlib.pyplot.xlabel('polarity score')
        matplotlib.pyplot.ylabel('tweet count')
        matplotlib.pyplot.grid(True)
        matplotlib.pyplot.show()

            
        
    def wordCloud(self,outLst):
        tweets = ''
        for tweet in outLst:
            for word in tweet:
                word = ps.stem(word.decode('utf-8'))
                tweets += '{} '.format(word)
        wordcloud = WordCloud(max_font_size=40).generate(tweets)
        matplotlib.pyplot.figure()
        matplotlib.pyplot.imshow(wordcloud)
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()
        
    


    def ldaModel(self,outLst):
        dictionary = corpora.Dictionary(outLst)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in outLst]
        Lda = gensim.models.ldamodel.LdaModel
        ldamodel = Lda(doc_term_matrix, num_topics=5, id2word = dictionary, passes=10)
        print(ldamodel.print_topics(num_topics=5, num_words=10))
        
    def nmfModelling(self,outLst):
        
        nmfLst = []
        for tweet in outLst:
            tweets = ''
            for word in tweet:
                tweets += '{} '.format(word)
                
            nmfLst.append(tweets)
        
        vectorizer = TfidfVectorizer(stop_words = 'english', min_df = 2)
        dtm = vectorizer.fit_transform(nmfLst)
        num_topics = 10
        num_top_words = 10
        clf = decomposition.NMF(n_components = num_topics, random_state=2)
        doc_topic = clf.fit_transform(dtm)
        topic_words = []
        vocab = vectorizer.get_feature_names()
        for topic in clf.components_:
            word_idx = np.argsort(topic)[::-1][0:num_top_words] 
            print 'top indexes', word_idx
            topic_words.append([vocab[i] for i in word_idx])
            print topic_words[-1]
        
        for t in range(len(topic_words)):
            print("Topic {}: {}".format(t, ', '.join(topic_words[t][:10])))

    
if __name__ == '__main__':
    with open('tweet_stream_10K.json') as f:
        dataJson = json.load(f)
    ta = tweetAnalysis()
    ta.cleanData(dataJson)
    ta.wordCloud(outLst)
    ta.sentimentAnalysis(outLst)
    ta.ldaModel(outLst)
    ta.nmfModelling(outLst)
    
    
        
    






  