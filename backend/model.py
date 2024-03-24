import tensorflow as tf
import PIL
import PIL.Image
import pathlib
import matplotlib.pyplot as plt
import numpy as np

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define augmentation parameters
datagen = ImageDataGenerator(
    rotation_range=10,          # Rotate images by up to 10 degrees
    width_shift_range=0.1,      # Shift images horizontally by up to 10% of total width
    height_shift_range=0.1,     # Shift images vertically by up to 10% of total height
    shear_range=0.2,            # Shear transformation
    zoom_range=0.2,             # Zoom in/out by up to 20%
    horizontal_flip=True,       # Flip images horizontally
    brightness_range=[0.8, 1.2],# Adjust brightness levels
    channel_shift_range=20,     # Adjust color channels
    fill_mode='nearest',        # Fill points outside the boundaries of the input with the nearest value
    validation_split=0.2
)

# Load images from directory and apply augmentation
train_generator = datagen.flow_from_directory(
    'asl_dataset/',        # Path to the training dataset directory
    target_size=(64, 64),       # Resize images to 64x64
    batch_size=32,              # Number of images in each batch
    class_mode='categorical',    # Use categorical labels
    subset="training"
)

# Load dataset from directory
# train_ds = tf.keras.utils.image_dataset_from_directory(
#   directory='asl_dataset/',
#   validation_split=0.2,
#   subset='training',
#   seed=123,
#   labels='inferred',
#   label_mode='categorical',
#   batch_size=32,
#   image_size=(64, 64),
#   )
validation_ds = tf.keras.utils.image_dataset_from_directory(
  directory='asl_dataset/',
  validation_split=0.2,
  seed=123,
  subset='validation',
  labels='inferred',
  label_mode='categorical',
  batch_size=32,
  image_size=(64, 64),
  )
class_names = train_generator.class_indices
print(class_names)



AUTOTUNE = tf.data.AUTOTUNE

# Optimize Datasets
# train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
validation_ds = validation_ds.cache().prefetch(buffer_size=AUTOTUNE)
# train_generator = train_generator.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)


# Define Variables
num_classes = len(class_names)
img_height = 64
img_width = 64
input_shape = (img_height, img_width, 3)

#Create Model
model = Sequential([
  layers.Input(shape=input_shape),
  layers.Rescaling(1./255),

  layers.Conv2D(32, (3,3), activation ='relu'),
  layers.MaxPool2D((2,2)),
  layers.BatchNormalization(),

  layers.Conv2D(64, (3,3), activation ='relu'),
  layers.MaxPool2D((2,2)),
  layers.BatchNormalization(),

  layers.Conv2D(128, (3,3), activation ='relu'),
  layers.MaxPooling2D((2, 2)),
  layers.BatchNormalization(),

  layers.Conv2D(256, (3,3), activation ='relu'),
  layers.MaxPooling2D((2, 2)),
  layers.BatchNormalization(),

  layers.Flatten(),

  layers.Dense(512, activation='relu', kernel_regularizer=l2(0.01)),
  layers.Dropout(0.25),
  layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
              metrics=['accuracy'])

model.summary()

epochs=20
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), patience=5)
early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2)


# Train model
history = model.fit(
  train_generator,
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