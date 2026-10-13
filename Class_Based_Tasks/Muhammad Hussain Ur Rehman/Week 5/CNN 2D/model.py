from pathlib import Path
import tensorflow as tf
import keras.layers as layers
import keras.utils as utils





TRAIN_DIR = Path("dataset/train")
VALIDATION_DIR = Path("dataset/validation")
MODEL_DIR = Path("saved_model")
MODEL_PATH = MODEL_DIR / "cnn2d.keras"
category_names = ["cat", "dog", "horse"]



train_dataset = utils.image_dataset_from_directory(
    TRAIN_DIR,
    label_mode="int",
    batch_size=32,
    image_size=(32,32),
    shuffle=True,
    class_names=category_names
)

validate_dataset = utils.image_dataset_from_directory(
    VALIDATION_DIR,
    label_mode="int",
    batch_size=32,
    image_size=(32, 32),
    shuffle=False,
    class_names=category_names
)

AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(AUTOTUNE)
validate_dataset = validate_dataset.prefetch(AUTOTUNE)

model = tf.keras.Sequential([
    layers.Input(shape=(32, 32, 3)),
    layers.Rescaling(1.0 / 255),
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),

    layers.Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    ),
    layers.BatchNormalization(),
    layers.Activation("relu"),
    layers.MaxPool2D(pool_size=(2, 2)),

    layers.Conv2D(
        filters=64,
        kernel_size=(3, 3),
        padding="same",
    ),
    layers.BatchNormalization(),
    layers.Activation("relu"),
    layers.MaxPool2D(pool_size=(2, 2)),

    layers.Conv2D(
        filters=128,
        kernel_size=(3, 3),
        padding="same",
    ),
    layers.BatchNormalization(),
    layers.Activation("relu"),
    layers.MaxPool2D(pool_size=(2, 2)),
    
    layers.Conv2D(
        filters=256,
        kernel_size=(3, 3),
        padding="same",
    ),
    layers.BatchNormalization(),
    layers.Activation("relu"),
    layers.MaxPool2D(pool_size=(2, 2)),
    
    layers.Conv2D(
        filters=512,
        kernel_size=(3, 3),
        padding="same",
    ),
    layers.BatchNormalization(),
    layers.Activation("relu"),
    layers.MaxPool2D(pool_size=(2, 2)),
    
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(3, activation="softmax")
])

model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
    loss='sparse_categorical_crossentropy',
    metrics=["accuracy"]
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=8,
    restore_best_weights=True,
    verbose=1
)
reduce_learning_rate = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=3,
    min_lr=0.00005,
)
history = model.fit(
    train_dataset,
    validation_data=validate_dataset,
    epochs=40,
    callbacks=[early_stopping,reduce_learning_rate]
)

MODEL_DIR.mkdir()
model.save(MODEL_PATH)
