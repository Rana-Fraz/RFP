from nltk import pos_tag,word_tokenize

import nltk
# nltk.download('all')
word="fraz is a working of khan"
tokens=word_tokenize(word)
for i in tokens:
    print (pos_tag([i]))