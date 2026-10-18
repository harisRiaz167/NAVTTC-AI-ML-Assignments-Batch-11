
import pandas as pd
import numpy
import sklearn
import tensorflow 
import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# read data
df = pd.read_csv("cnn_text_classification.csv")

# hyperparameters
MAX_WORDS = 50000
MAX_LEN = 50

# tokenization
tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
tokenizer.fit_on_texts(df["text"])
sequences = tokenizer.texts_to_sequences(df["text"])

# padding
X = pad_sequences(sequences, maxlen=MAX_LEN,padding="post", truncating="post")
y = df["label"].values

# spliting data into training and testing/validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout

NUM_CLASSES = 1 
ACTIVATION = 'sigmoid'
LOSS_FUNCTION = 'binary_crossentropy'

model = Sequential([
    Embedding(input_dim=MAX_WORDS, output_dim=64, input_length=MAX_LEN),

    Conv1D(filters=128, kernel_size=5, activation='relu'),
    GlobalMaxPooling1D(),
    Dense(32, activation='relu'),
    Dropout(0.5),
    
    Dense(NUM_CLASSES, activation=ACTIVATION)
])

model.compile(optimizer='adam', loss=LOSS_FUNCTION, metrics=['accuracy'])

model.summary()

history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=1
)


# 1. Save the model architecture and weights
model.save("sentiment_cnn_model.keras")
print("Model saved successfully!")

def predict_sentiment(new_text):

    test_seq = tokenizer.texts_to_sequences([new_text])
    test_padded = pad_sequences(test_seq, maxlen=MAX_LEN, padding='post', truncating='post')
    
    prediction = model.predict(test_padded, verbose=0)[0][0]
    
    sentiment = "Positive" if prediction >= 0.5 else "Negative"
    confidence = prediction if prediction >= 0.5 else (1 - prediction)
    
    print(f"Text: '{new_text}' -> Sentiment: {sentiment} ({confidence*100:.2f}% confidence)")

print("\n--- Testing Model Predictions ---")
predict_sentiment("The story was messy and weak")
predict_sentiment("The movie was charming and brilliant.")