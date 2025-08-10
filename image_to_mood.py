import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, Conv2D, BatchNormalization, Activation, Add, MaxPooling2D, Dropout, Flatten, Dense
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

from sklearn.metrics import classification_report, confusion_matrix
# --- Define Residual Block ---
def residual_block(x, filters, kernel_size=3, strides=1):
    shortcut = x

    # First conv layer
    x = Conv2D(filters, kernel_size, strides=strides, padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # Second conv layer
    x = Conv2D(filters, kernel_size, strides=1, padding='same')(x)
    x = BatchNormalization()(x)

    # Shortcut connection with possible downsampling
    if strides != 1 or shortcut.shape[-1] != filters:
        shortcut = Conv2D(filters, kernel_size=1, strides=strides, padding='same')(shortcut)
        shortcut = BatchNormalization()(shortcut)

    x = Add()([x, shortcut])
    x = Activation('relu')(x)
    return x
def build_resnet_like_model(input_shape=(48, 48, 1), num_classes=7):
    inputs = Input(shape=input_shape)

    # Initial Conv Layer
    x = Conv2D(64, 3, strides=1, padding='same')(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # Residual Blocks with increasing filters
    x = residual_block(x, 64)
    x = residual_block(x, 64)

    x = residual_block(x, 128, strides=2)  # Downsample
    x = residual_block(x, 128)

    x = residual_block(x, 128, strides=2)  # Downsample
    x = residual_block(x, 128)

    x = residual_block(x, 128, strides=2)  # Downsample
    x = residual_block(x, 128)

    # Global Max Pooling + Dense layers
    x = MaxPooling2D(pool_size=4)(x)
    x = Flatten()(x)
    x = Dense(512, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)

    outputs = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs, outputs)
    model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
    )   
    return model

def preprocess_image(img_path, target_size=(48,48)):
    # Load image in grayscale mode
    img = image.load_img(img_path, color_mode='grayscale', target_size=target_size)
    # Convert to numpy array
    img_array = image.img_to_array(img)
    # Normalize pixel values to [0,1]
    img_array = img_array / 255.0
    # Add batch dimension: (48,48,1) -> (1,48,48,1)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_single_image( img_path, class_names):
    # Preprocess image
    img = preprocess_image(img_path)

    # Predict probabilities
    model = build_resnet_like_model()
    model.load_weights('model_files_for_eeg/resnet_.weights.h5')
    preds = model.predict(img)
    # print(preds)
    pred_class_idx = np.argmax(preds)
    confidence = preds[0][pred_class_idx]

    predicted_label = class_names[pred_class_idx]
    return predicted_label


# # # 2. Define your class names (must match training classes order)
# class_names = ['angry', 'happy', 'fear', 'happy', 'neutral', 'sad', 'surprise']
# #  # replace with your classes

# # # 3. Predict on a new image
# img_path = 'model_files_for_eeg/The_joy_of_the_happy_face_by_Rasheedhrasheed.jpg'
# label = predict_single_image(img_path, class_names)
# print(label)