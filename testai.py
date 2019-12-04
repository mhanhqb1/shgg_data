from gensim.models.doc2vec import Doc2Vec
from scipy.spatial.distance import cosine
import json, numpy
from hashlib import md5
import spacy
import os
from gensim.models.doc2vec import TaggedDocument

nlp = spacy.load('en')

# For doc2vec
ALPHA = 0.025
EPOCH = 100
INT_SIZE = 16
VEC_DIM = 400
RANDOM_SEED_INT = 0
CORPUS_FILE_NAME = 'c.model'
ORIGINAL_STOP_WORDS = ['.', ',', '...', ' ', '  ', '-pron-','"','\'']
EMPTY_LIST = []

def hash_func(in_str):
    return int(md5(in_str.encode('utf-8')).hexdigest(), INT_SIZE)

def get_infer_vec(in_word_list):
    model.random.seed(RANDOM_SEED_INT)
    return model.infer_vector(in_word_list, alpha=ALPHA, steps=EPOCH)

def a(words, related):
	this_vec = get_infer_vec(get_lower_lemma_of_description(words))
	result = numpy.zeros(len(related))
	i = 0
	for w in related:
		rv = get_infer_vec(get_lower_lemma_of_description(str(w['name'])))
		result[i] = cosine(numpy.array(rv), this_vec)
		i += 1
	result = numpy.argsort(result)
	return result

def get_lower_lemma_of_description(in_description):
    result = []
    if in_description != '':
        this_nlp = nlp(in_description)
        for word in this_nlp:
            this_lemma = word.lemma_.lower()
            if word.is_stop is False and this_lemma not in ORIGINAL_STOP_WORDS:
                result.append(this_lemma)
    return result

def _get_available_words(in_word_list):
    return [t for t in in_word_list if t is not None]

def train_model(in_tagged_docs):
    if not in_tagged_docs == EMPTY_LIST:
        # initialize
        # model.clear_sims()
        model.random.seed(RANDOM_SEED_INT)
        model.build_vocab(in_tagged_docs, update=False)
        model.train(in_tagged_docs, total_examples=len(in_tagged_docs), epochs=EPOCH)
        path = os.path.join('/', CORPUS_FILE_NAME)
        model.save(path)
        model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

# doc2vec model
model = Doc2Vec(
    size=VEC_DIM,
    min_count=1,
    workers=1,
    negative=0,
    sample=0,
    dm=0,
    hs=1,
    epoch=EPOCH,
    alpha=ALPHA,
    hashfxn=hash_func
)

words = 'toi yeu em'
related = [
	{
		'id': 1,
		'name': 'em yeu ai'
	},
	{
		'id': 2,
		'name': 'ai yeu em'
	},
	{
		'id': 3,
		'name': 'em yeu toi'
	},
	{
		'id': 4,
		'name': 'toi yeu em'
	},
	{
		'id': 5,
		'name': 'toi yeu em nhieu'
	},
	{
		'id': 6,
		'name': 'toi khong yeu em'
	},
	{
		'id': 7,
		'name': 'toi ghet em'
	}
]
tagged_docs = []
for text in related:
	this_text = _get_available_words(json.loads(json.dumps(text['name'])))
	tagged_docs.append(TaggedDocument(words=this_text, tags=[str(text['id'])]))

print('Train model')
train_model(tagged_docs)
a = a(words, related)
for x in a:
	print(x + 1)