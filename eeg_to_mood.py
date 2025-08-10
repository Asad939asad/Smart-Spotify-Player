import pandas as pd
from joblib import load
import tensorflow as tf

def create_enhanced_dense_model():
    inputs = tf.keras.Input(shape=(2548,))

    # Dense layers with BatchNorm and Dropout
    x = tf.keras.layers.Dense(512, activation='relu')(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.4)(x)

    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.5)(x)

    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.5)(x)


    x = tf.keras.layers.Dense(64, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.5)(x)

    x = tf.keras.layers.Dense(64, activation='relu')(x)

    # Output layer
    outputs = tf.keras.layers.Dense(3, activation='softmax')(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Load saved scaler
def Final_Prediction(csv_data):
  scaler = load('model_files_for_eeg/scaler (1).save')

  # Load your new CSV
  new_data = csv_data

  # Drop label column if exists
  if 'label' in new_data.columns:
      new_data = new_data.drop(columns=['label'])

  X_new = new_data.values

  # Scale features
  X_new_scaled = scaler.transform(X_new)

  # Predict using model
  model = create_enhanced_dense_model()
  model.load_weights("model_files_for_eeg/eeg_model_.weights.h5")
  predictions = model.predict(X_new_scaled)

  # Decode predictions
  predicted_classes = predictions.argmax(axis=1)
  label_map = {0: 'NEUTRAL', 1: 'POSITIVE', 2: 'NEGATIVE'}
  predicted_labels = [label_map[c] for c in predicted_classes]
  return predicted_labels
# d = pd.read_csv('uploads/file.csv')
# predicted_labels = Final_Prediction(d)

# print(predicted_labels)
