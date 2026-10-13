import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import keras


df = pd.read_csv("cnn_text_classification.csv")
X = df.iloc[:, 1].fillna("").astype(str)
y = df.iloc[:, 2].astype("int32")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

X_train = X_train.to_numpy(dtype=object)
X_test = X_test.to_numpy(dtype=object)
y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

vectorizer = keras.layers.TextVectorization(max_tokens=20000,output_mode="int",output_sequence_length=100)
vectorizer.adapt(X_train)

inputs = keras.Input(shape=(), dtype=tf.string)
x = vectorizer(inputs)
x = keras.layers.Embedding(input_dim=20000,output_dim=128)(x)
x = keras.layers.SpatialDropout1D(0.2)(x)
x = keras.layers.Conv1D(128, 3, padding="same", activation="relu")(x)
x = keras.layers.Conv1D(64, 3, padding="same", activation="relu")(x)
x = keras.layers.Conv1D(32, 3, padding="same", activation="relu")(x)
x = keras.layers.Conv1D(16, 3, padding="same", activation="relu")(x)
x = keras.layers.GlobalMaxPooling1D()(x)
x = keras.layers.Dense(16, activation="relu")(x)
x = keras.layers.Dropout(0.4)(x)
outputs = keras.layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs, outputs)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=4,
    restore_best_weights=True,
)

reduce_learning_rate = keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=2,
    min_lr=1e-6,
)

model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=40,
    batch_size=32,
    callbacks=[early_stop,reduce_learning_rate],
)

test_loss, test_accuracy = model.evaluate(X_test,y_test,)

print(f"Test accuracy: {test_accuracy:.3f}")
print(f"Test loss: {test_loss:.3f}")

model.save("text_cnn.keras")



