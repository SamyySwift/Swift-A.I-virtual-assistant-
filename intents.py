import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle

intents = {"intents": [
    {"tag": "wakewords",
     "patterns": ['hey swift', 'ok swift', 'swift'],
     "responses": ["what can i do for you", 'how can i help you', 'am here', 'am listening']
    },
    {"tag": "greetings",
     "patterns": ["Hi", "Hey", "Is anyone there?", "Hello", "Hay", "Yo", 'whatsup', 'hey swift', 'ok swift', 'swift'],
     "responses": ["Hello", "Hi", "Hi there", 'Hi human', 'how can i help you']
    },
    {"tag": "goodbye",
     "patterns": ["Bye", "See you later", "Goodbye"],
     "responses": ["See you later", "Have a nice day", "Bye! Come back again"]
    },
    {"tag": "thanks",
     "patterns": ["Thanks", "Thank you", "That's helpful", "Thanks for the help"],
     "responses": ["Happy to help!", "Any time!", "My pleasure", "You're most welcome!"]
    },
    {"tag": "about",
     "patterns": ["Who are you?", "What are you?", "Who you are?", "Who created you?"],
     "responses": ["I'm Swift, am here to do cool tasks for you, ", "i was programmed by samswift to help you do cool stuff ", "I was created by SamSwift, and i am your personal assistant", "i am swift, your virtual assistant"]
    },
    {"tag": "name",
    "patterns": ["what is your name", "what should I call you", "whats your name?", 'your name', 'name'],
    "responses": ["You can call me Swift.", "I'm Swift!", "Just call me Swift", "my name is Swift", 'I go by the name swift']
    },
    {"tag": "help",
    "patterns": ["Could you help me?", "give me a hand please", "Can you help?", "What can you do for me?", "I need a support", "I need a help", "support me please"],
    "responses": ["Tell me how can assist you", "Tell me your problem to assist you", "Yes Sure, How can I support you"]
    },

    {"tag": "search",
     "patterns": ["i want to search ", "search", "i want to search the internet",
                  "i wanna search the web", "search the internet for me"],
     "responses": ["what do you want to search for", "ok, what would you like to search for?",
                   "sure, i can help you search the internet, just tell me what i should search for", "no problem, what do you wanna search for?"]
     }
]
}

# with open('intents.json', 'w') as intents_json:
#   json.dump(intents, intents_json)
#
#
# with open('intents.json') as file:
#     data = json.load(file)
#
#
# training_sentences = []
# training_labels = []
# labels = []
# responses = []
#
# for intents in data['intents']:
#   for patterns in intents['patterns']:
#     training_sentences.append(patterns)
#     training_labels.append(intents['tag'])
#   responses.append(intents['responses'])
#
#   if intents['tag'] not in labels:
#         labels.append(intents['tag'])
#
# num_classes = len(labels)
#
# lbl_encoder = LabelEncoder()
# training_labels = lbl_encoder.fit_transform(training_labels)
#
# vocab_size = 1000
# embedding_dim = 16
# max_len = 20
# oov_token = "<OOV>"
#
# tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token) # adding out of vocabulary token
# tokenizer.fit_on_texts(training_sentences)
# word_index = tokenizer.word_index
# sequences = tokenizer.texts_to_sequences(training_sentences)
# padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)
#
#
# model = Sequential()
# model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
# model.add(GlobalAveragePooling1D())
# model.add(Dense(16, activation='relu'))
# model.add(Dense(32, activation='relu'))
# model.add(Dense(128, activation='relu'))
# model.add(Dense(num_classes, activation='softmax'))
#
# model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#
# epochs = 500
# history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs, verbose=1)
#
# # to save the trained model
# model.save("chat_model")
#
#
# # to save the fitted tokenizer
# with open('tokenizer.pickle', 'wb') as handle:
#     pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
# # to save the fitted label encoder
# with open('label_encoder.pickle', 'wb') as ecn_file:
#     pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)
#
# with open('respones.json', 'w') as response_json:
#   json.dump(responses, response_json)


def chat(usertext):
    model = keras.models.load_model('chat_model')

    with open('intents.json') as file:
        data = json.load(file)

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    with open('respones.json') as file:
        responses = json.load(file)

    # parameters
    max_len = 20
    inp = usertext
    if inp.lower() == "quit":
        exit()

    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                                  truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    proba = result[0][np.argmax(result)]

    for i in data['intents']:
        if (i['tag'] == tag) and (proba > 0.6):
            return np.random.choice(i['responses'])

        elif (i['tag'] != tag) and (proba < 0.6):
            return np.random.choice(["Sorry, I can't answer that question at the moment. Ask another question",
                                     "probably i wasn't trained to answer that question", "Am not sure about my answer"])

