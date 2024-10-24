import tkinter as tk
from tkinter import messagebox
import cv2
from fer import FER
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import speech_recognition as sr
from textblob import TextBlob

client_id = '078b56c0444c4fa7993cd9965d959d53'
client_secret = '442d90ffccc44e428ede6be3cd4823d4'
credentials = SpotifyClientCredentials(client_id='078b56c0444c4fa7993cd9965d959d53', client_secret='442d90ffccc44e428ede6be3cd4823d4')
sp = spotipy.Spotify(client_credentials_manager=credentials)

mood_queries = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "surprise": "surprise",
    "fear": "fear",
    "disgust": "chill",
    "neutral": "relax"
}

playlist_links = []

def recommend_playlists(emotion):
    global playlist_links
    query = mood_queries.get(emotion)
    playlist_links = []
    playlists = []
    if query:
        results = sp.search(q=f'playlist {query}', type='playlist', limit=5)
        for playlist in results['playlists']['items']:
            playlist_links.append(playlist['external_urls']['spotify'])
            playlists.append(f"🎵 Playlist: {playlist['name']} - Link: {playlist['external_urls']['spotify']}\n")
        if playlists:
            return ''.join(playlists)
    return "🎵 Default Playlist: A mix of various genres."

def detect_emotion():
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open webcam.")
        return

    start_time = time.time()
    detected_emotions = {}

    while True:
        ret, frame = cap.read()

        if not ret:
            messagebox.showerror("Error", "Could not read frame from webcam.")
            break

        emotion_data = detector.detect_emotions(frame)
        if emotion_data:
            for face in emotion_data:
                dominant_emotion = face["emotions"]
                top_emotion = max(dominant_emotion, key=dominant_emotion.get)

                if top_emotion in detected_emotions:
                    detected_emotions[top_emotion] += 1
                else:
                    detected_emotions[top_emotion] = 1

        cv2.imshow("Webcam - FER Emotion Detection", frame)

        if time.time() - start_time > 10:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if detected_emotions:
        dominant_emotion = max(detected_emotions, key=detected_emotions.get)
        playlists = recommend_playlists(dominant_emotion)
        result_label.config(state=tk.NORMAL)
        result_label.delete(1.0, tk.END)
        start_index = result_label.index(tk.END)
        result_label.insert(tk.END, f"Detected Emotion: {dominant_emotion}\n{playlists}")
        end_index = result_label.index(tk.END)

        for idx in range(len(playlist_links)):
            result_label.tag_add(f"hyper{idx+1}", start_index + f" + {idx + 1} lines", start_index + f" + {idx + 2} lines")

        result_label.config(state=tk.DISABLED)
    else:
        result_label.config(state=tk.NORMAL)
        result_label.delete(1.0, tk.END)
        result_label.insert(tk.END, "No emotions detected.")
        result_label.config(state=tk.DISABLED)

def on_hyperlink_click(event):
    index = event.widget.index("@%s,%s" % (event.x, event.y))
    tag_names = event.widget.tag_names(index)
    for tag in tag_names:
        if tag.startswith("hyper"):
            playlist_index = int(tag.replace("hyper", "")) - 1
            url = playlist_links[playlist_index]
            webbrowser.open(url)
            break

def manual_input():
    mood = mood_entry.get().lower()
    if mood in mood_queries:
        playlists = recommend_playlists(mood)
        result_label.config(state=tk.NORMAL)
        result_label.delete(1.0, tk.END)
        start_index = result_label.index(tk.END)
        result_label.insert(tk.END, playlists)
        end_index = result_label.index(tk.END)

        for idx in range(len(playlist_links)):
            result_label.tag_add(f"hyper{idx+1}", start_index + f" + {idx + 1} lines", start_index + f" + {idx + 2} lines")

        result_label.config(state=tk.DISABLED)
    else:
        result_label.config(state=tk.NORMAL)
        result_label.delete(1.0, tk.END)
        result_label.insert(tk.END, "Mood not recognized, try again.")
        result_label.config(state=tk.DISABLED)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Info", "Please speak your mood clearly.")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            mood = TextBlob(text).sentiment.polarity
            if mood > 0:
                playlists = recommend_playlists("happy")
            elif mood < 0:
                playlists = recommend_playlists("sad")
            else:
                playlists = recommend_playlists("neutral")
            result_label.config(state=tk.NORMAL)
            result_label.delete(1.0, tk.END)
            result_label.insert(tk.END, playlists)
            result_label.config(state=tk.DISABLED)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results from Google Speech Recognition service.")

root = tk.Tk()
root.title("EmoTune")
root.geometry("800x800")

instruction_label = tk.Label(root, text="Instructions:\n"
                                          "1. To use the webcam: Look at the webcam for 10 seconds. Stay still.\n"
                                          "2. For speech input: Speak clearly to give your mood.")
instruction_label.pack(pady=10)

mood_entry = tk.Entry(root, width=40)
mood_entry.pack(pady=10)

manual_button = tk.Button(root, text="Submit Mood", command=manual_input)
manual_button.pack(pady=5)

speech_button = tk.Button(root, text="Speech Input", command=recognize_speech)
speech_button.pack(pady=5)

camera_button = tk.Button(root, text="Camera Detection", command=detect_emotion)
camera_button.pack(pady=5)

result_label = tk.Text(root, height=10, wrap=tk.WORD, state=tk.DISABLED)
result_label.pack(pady=10)

root.mainloop()
