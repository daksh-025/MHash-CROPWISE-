import pickle
import tensorflow as tf

print(tf.__version__)
model = pickle.load(open(r'potato.pkl', 'rb'))
print(model.summary())