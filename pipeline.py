import nltk

texts = [
    """
    The Indian subcontinent was home to the urban Indus Valley Civilisation of the 3rd millennium BCE. In the following millennium, the oldest scriptures associated with Hinduism began to be composed. Social stratification, based on caste, emerged in the first millennium BCE, and Buddhism and Jainism arose. Early political consolidations took place under the Maurya and Gupta empires; later peninsular Middle Kingdoms influenced cultures as far as Southeast Asia. In the medieval era, Judaism, Zoroastrianism, Christianity, and Islam arrived, and Sikhism emerged, all adding to the region's diverse culture. Much of the north fell to the Delhi Sultanate; the south was united under the Vijayanagara Empire. The economy expanded in the 17th century in the Mughal Empire. In the mid-18th century, the subcontinent came under British East India Company rule, and in the mid-19th under British Crown rule. A nationalist movement emerged in the late 19th century, which later, under Mahatma Gandhi, was noted for nonviolent resistance and led to India's independence in 1947.
    """
] 
 
for text in texts:
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        tagged_words = nltk.pos_tag(words)
        ne_tagged_words = nltk.ne_chunk(tagged_words)
        print(ne_tagged_words)


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start


  
def source(texts, targets):
    for text in texts:
        for t in targets:
            t.send(text)

@coroutine
def sent_tokenize_pipeline(targets):
    while True:
        text = (yield)
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            for target in targets:
                target.send(sentence)
 
@coroutine
def word_tokenize_pipeline(targets):
    while True:
        sentence = (yield)
        words = nltk.word_tokenize(sentence)
        for target in targets:
            target.send(words)
 
@coroutine
def pos_tag_pipeline(targets):
    while True:
        words = (yield)
        tagged_words = nltk.pos_tag(words)
 
        for target in targets:
            target.send(tagged_words)
 
@coroutine
def ne_chunk_pipeline(targets):
    while True:
        tagged_words = (yield)
        ner_tagged = nltk.ne_chunk(tagged_words)
 
        for target in targets:
            target.send(ner_tagged)


@coroutine
def printer():
    while True:
        line = (yield)
        print(line)


source(texts, targets=[
    sent_tokenize_pipeline(targets=[
        printer(),  # print the raw sentences
        word_tokenize_pipeline(targets=[
            printer(),  # print the tokenized sentences
            pos_tag_pipeline(targets=[
                printer(),  # print the tagged sentences
                ne_chunk_pipeline(targets=[printer()]),
            ])
        ])
    ])
])
 
 
