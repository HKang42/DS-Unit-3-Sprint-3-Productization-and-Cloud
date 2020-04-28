import basilica
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY")

def basilica_api_client():
    connection = basilica.Connection(API_KEY)
    #print(type(connection)) #> <class 'basilica.Connection'>
    return connection

if __name__ == "__main__":


    print("---------")
    connection = basilica_api_client()

    # test one sentence
    print("---------")
    sentence = "Hello again"
    sent_embeddings = connection.embed_sentence(sentence)
    print(list(sent_embeddings))

    # test list of sentences
    print("---------")
    sentences = ["Hello world!", "How are you?"]
    print(sentences)
    # it is more efficient to make a single request for all sentences...
    embeddings = connection.embed_sentences(sentences)
    print("EMBEDDINGS...")
    print(type(embeddings))
    print(list(embeddings)) # [[0.8556405305862427, ...], ...]

    # test the twitter model
    print("---------")
    tweet = "I love #ArtificialIntelligence"
    tweet_embeddings = connection.embed_sentence(tweet, model="twitter")
    print(list(tweet_embeddings))
