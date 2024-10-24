# EmoTune
#### Video Demo:  <https://youtu.be/0t7vzouKhOk>

## Description
EmoTune is an innovative emotion-based music player that enhances your listening experience by suggesting playlists tailored to your current mood. The application utilizes advanced emotion recognition technology to analyze your facial expressions and voice to detect your emotional state.

## Features
- **Real-Time Emotion Detection**: Utilize webcam input to detect emotions within seconds.
- **Voice Input Recognition**: Speak your mood clearly, and EmoTune will analyze your speech to suggest the appropriate playlists.
- **Manual Mood Entry**: Type in your mood to receive tailored playlist suggestions.
- **Spotify Integration**: Access and open Spotify playlists directly from the app, based on the detected or entered mood.
- **User-Friendly Interface**: Clear instructions guide you through the input methods, making it easy for anyone to use.

## Technologies Used
- OpenCV for real-time video processing.
- FER (Facial Emotion Recognition) for emotion detection.
- Spotipy for Spotify API integration.
- SpeechRecognition for converting spoken input into text.
- Tkinter for creating the user interface.

## How to Use It
1. **Start the Application**: Run the EmoTune application.
2. **Choose Input Method**:
   - **Webcam Input**: Select the webcam option, look at the camera for 10 seconds, and remain still. EmoTune will detect your facial expression and determine your mood.
   - **Voice Input**: Select the voice input option, and clearly state your mood. EmoTune will recognize the emotion from your voice.
   - **Manual Input**: Type your mood directly into the provided text box and submit.
3. **Receive Recommendations**: After detecting your mood or entering it manually, EmoTune will suggest playlists from Spotify that match your emotional state.
4. **Access Playlists**: Click on the provided Spotify links to open your personalized playlists directly in the Spotify app or web player.

## How to Run the Application
1. **Open a Terminal or Command Prompt**: Navigate to the directory where you cloned the EmoTune project.
2. **Activate Your Python Environment**: If you are using a virtual environment, activate it. For example, if you’re using `venv`, run:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. **Install Dependencies**: Ensure that all required packages are installed by running:
   ```bash
   pip install -r requirements.txt
