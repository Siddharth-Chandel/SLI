import cv2
import numpy as np
from keras.utils import img_to_array
from keras.models import load_model
from keras.utils import img_to_array
from constants import MODEL, SHAPE, VIDEO, GESTURES, QUIT_KEY
import pyttsx3 as speackAI
import _thread
from rich import print as pprint

# Configuring speaking engine
engine = speackAI.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)


# Define the preprocess_frame function
def preprocess_frame(frame):
    # Resize the frame to match the model's expected input shape
    resized_frame = cv2.resize(frame, SHAPE)
    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    # Convert the frame to an array
    array_frame = img_to_array(rgb_frame)
    # Add an extra dimension (batch dimension)
    preprocessed_frame = np.expand_dims(array_frame, axis=0)
    return preprocessed_frame

# Text to speak conversion
def speak(text):
    engine.say(text)
    try:
        engine.runAndWait()
    except RuntimeError as rte:
        pprint('[bright_red]Next...[/bright_red]\n')


def Sign2Voice(model_path: str, video_src: int):
    # Load the pretrained gesture recognition model
    model = load_model(model_path)

    # Set up the video capture
    cap = cv2.VideoCapture(video_src)

    while True:
        # Read a frame from the live camera feed
        ret, frame = cap.read()

        if not ret:
            break

        # Preprocess the frame
        cv2.rectangle(frame, (100, 200, 300, 600),
                      color=(255, 255, 0), thickness=2)
        Pframe = frame[200:600, 100:400]
        processed_frame = preprocess_frame(Pframe)

        # Perform gesture recognition using the pretrained model
        prediction = model.predict(processed_frame)
        predicted_gesture = np.argmax(prediction)

        # Convert the predicted gesture index to a label
        gesture_label = GESTURES[predicted_gesture]

        # Putting gesture name on the frame
        cv2.putText(frame, 'Gesture: ' + gesture_label, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Concurrently speaking the gesture name
        _thread.start_new_thread(speak, (gesture_label,))

        # Representing the video frame
        cv2.imshow('Live Gesture Recognition', frame)

        # Printing the gesture name
        pprint(f'[cyan]Gestures[/cyan] :- [yellow]{gesture_label}[/yellow]')

        # Exit the loop if the key is pressed
        if cv2.waitKey(1) & 0xFF == ord(QUIT_KEY):
            break

    # Release the video capture and close the windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    Sign2Voice(model_path=MODEL, video_src=VIDEO)
