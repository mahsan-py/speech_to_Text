
import speech_recognition as sr
def start_speech_to_text(number):
# Function to perform speech recognition
    def recognize_speech(audio_file):
        # Initialize recognizer class
        recognizer = sr.Recognizer()
        
        # Load audio file
        with sr.AudioFile(audio_file) as source:
            # Record the audio data from the file
            audio_data = recognizer.record(source)
            
            try:
                # Recognize the speech
                text = recognizer.recognize_google(audio_data)

                with open(output_file, 'w') as file:
                    file.write(text)

                print("Text recognized from audio:", text)
            except sr.UnknownValueError:
                print("Speech recognition could not understand the audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Provide the path to the audio file
    audio_file = "speech/output_denoised"+str(number)+".wav"
    output_file="text_data/output_text"+str(number)+".txt"
# Call the function to recognize speech from the audio file
    recognize_speech(audio_file)
