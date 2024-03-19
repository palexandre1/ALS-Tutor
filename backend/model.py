import tensorflow as tf
import PIL
import PIL.Image
import pathlib
import matplotlib.pyplot as plt
import numpy as np

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

# Load dataset from directory
train_ds = tf.keras.utils.image_dataset_from_directory(
  directory='asl_dataset/',
  validation_split=0.2,
  subset='training',
  seed=123,
  labels='inferred',
  label_mode='categorical'
  )
validation_ds = tf.keras.utils.image_dataset_from_directory(
  directory='asl_dataset/',
  validation_split=0.2,
  seed=123,
  subset='validation',
  labels='inferred',
  label_mode='categorical'
  )
class_names = train_ds.class_names
print(class_names)

AUTOTUNE = tf.data.AUTOTUNE

# Optimize Datasets
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
validation_ds = validation_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1./255)
normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))

# Define Variables
num_classes = len(class_names)
img_height = 256
img_width = 256
input_shape = (img_height, img_width, 3)


# Data Augmentation
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
  ])

#Create Model
model = Sequential([
  layers.Input(shape=input_shape),
  data_augmentation,
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.2),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

epochs=15

# Train model
history = model.fit(
  normalized_ds,
  validation_data=validation_ds,
  epochs=epochs
)

# Save the model
model.save('asl_model.keras')

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')

plt.savefig('analysis.png', bbox_inches='tight')