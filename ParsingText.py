from spacy.en import English
import nltk

parser = English()

text = "I love Tacos. I have a Ph.D. in Tacology."
tokens = parser(text)

# print the sentences
for sent in tokens.sents:
    print('Sentence')
    print(sent)
    print()




