import os
import glob
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import img_to_array, load_img
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils import img_to_array

from constants import MODEL, SHAPE

# Set the paths to the directories containing the image and GIF files
image_train_path = 'assets/data/*/*.jpg'
gif_train_path = 'assets/ISL_Gifs/*.gif'

# Set the image dimensions and number of classes
image_width, image_height = SHAPE
num_classes = 125

# Define the lists to store data and labels
X_train_image = []
y_train_image = []
X_train_gif = []
y_train_gif = []

# Load and preprocess the training data from images
for image_file in glob.glob(image_train_path):
    # Load the image file
    image = load_img(image_file, target_size=(image_width, image_height))
    # Preprocess the image
    image_array = img_to_array(image)
    # Append the image array to the training set
    X_train_image.append(image_array)
    # Extract the class label from the subdirectory name
    label = image_file.split('\\')[-2]
    y_train_image.append(label)

# Load and preprocess the training data from GIFs
for gif_file in glob.glob(gif_train_path):
    # Load the GIF file
    gif = cv2.VideoCapture(gif_file)
    frames = []
    while True:
        ret, frame = gif.read()
        if not ret:
            break
        # Preprocess the frame
        frame = cv2.resize(frame, (image_width, image_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)
    gif.release()
    # Convert frames to numpy array
    gif_data = np.array(frames)
    # Reshape the GIF data to match the image dimensions
    gif_data = np.reshape(gif_data, (-1, image_width, image_height, 3))
    # Append the GIF data to the training set
    X_train_gif.extend(gif_data)
    # Extract the class label from the GIF file name
    label = os.path.splitext(os.path.basename(gif_file))[0]
    y_train_gif.extend([label] * gif_data.shape[0])

# Convert the training data and labels to numpy arrays
X_train_image = np.array(X_train_image)
y_train_image = np.array(y_train_image)
X_train_gif = np.array(X_train_gif)
y_train_gif = np.array(y_train_gif)

# Concatenate the image and GIF data
X_train = np.concatenate((X_train_image, X_train_gif), axis=0)
y_train = np.concatenate((y_train_image, y_train_gif), axis=0)

# Encode the class labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)

# Convert the encoded labels to one-hot encoded vectors
y_train_one_hot = np.eye(num_classes)[y_train_encoded]

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train_one_hot, test_size=0.2, random_state=42)

# Create the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu',
          input_shape=(image_width, image_height, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, validation_data=(X_val, y_val))

# Save the trained model
model.save(MODEL)

print('Trained successfully...')