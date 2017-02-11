from spacy.en import English
import nltk
import spacy

#  to make spacy parser Ph.D as a single token
#  spacy.en.English.Defaults.tokenizer_exceptions["Ph.D."] = [{"F": "Ph.D."}]

parser = English()

text = "Paco loves Tacos. Paco has a Ph.D. in Tacology."
tokens = parser(text)

# print the sentences
for sent in tokens.sents:
    print('Sentence')
    print(sent)
    print()

#  token_orth gives the string representation of the token
tokenList = [token.orth_ for token in tokens if not token.orth_.isspace()]


def print_token(t):
    print('value: ', t.orth_)
    print('lemma: ', t.lemma_)
    print('shape: ', t.shape_)

for token in tokens:
    print_token(token)

english_stopwords = set(nltk.corpus.stopwords.words('english'))
#  removing stop words

tokenWithOutStopWords = [token.orth_ for token in tokens if token.orth_ not in english_stopwords]
print("Tokens without stop words")
print(tokenWithOutStopWords)