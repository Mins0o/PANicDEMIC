import csv
import nltk
import random
import pandas as pd
import math
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer as lem

swear_freq = {'dick': 3.33, 'damn': 14.46, 'shit': 34.75, 'fuck': 33.1, 'wtf': 9.85, 'stupid': 12.45, 'sucks': 6.47, 'fucked': 6.8, 'suck': 2.57, 'heck': 2.04}


def get_score(freq):
	output = freq.copy()
	for i in output:
		output[i] = round((10/output[i]),2)
	return output

def read_tweet(filename):
	
	reader = pd.read_csv(filename, sep='\t', header=None, engine='python', skiprows=2, encoding = "utf-16")
	
	id = list(reader[0])
	text = list(reader[1])
	
	input = []
	
	for i in range(len(id)):
		input.append([id[i],text[i]])
	
	return input
	
def swear_score(tweet,score):
	token = nltk.word_tokenize(tweet)
	
	mark = 0
	
	for swear in swear_freq:
		for word in token:
			if word.lower() == swear:
				if word.upper() == word:
					mark += 2*score[swear]
				else:
					mark += score[swear]
				
	return mark
	
score = get_score(swear_freq)

id_tweet = read_tweet('./Tweets_crosstab.csv')

output = []
for i in id_tweet:
	tweet_score = swear_score(i[1],score)
	output.append([i[0],i[1],tweet_score])
	
write = pd.DataFrame(output, columns=['Id', 'Tweet','Swear Score'])
write.to_csv('swear_score.csv')
	
	