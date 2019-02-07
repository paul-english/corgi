import numpy as np

from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

tk = Tokenizer(num_words=None, char_level=True, oov_token='UNK')
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{} "
char_dict = {}
for i, char in enumerate(alphabet):
    char_dict[char] = i + 1
tk.word_index = char_dict.copy()
tk.word_index[tk.oov_token] = max(char_dict.values()) + 1
vocab_size = len(tk.word_index)

def texts_to_data(texts, max_length):
    global tk
    seq = tk.texts_to_sequences(texts)
    data = pad_sequences(seq, maxlen=max_length, padding='post')
    return np.array(data, dtype='float32')
