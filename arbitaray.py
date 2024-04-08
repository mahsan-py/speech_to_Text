

import numpy as np
import queue
import sys
import streamlit as st
import sounddevice as sd
import soundfile as sf
# import noisereduce as nr

q_data = np.empty((512,512))
q = queue.Queue()
samplerate = 44100
channels = 1
subtype = 'PCM_24'
device = None  # Set to None if not specified
filename = "output7.wav"  # Set to None if not specified
global_file = None
global_stream = None
threshold = 0.04  # Adjust according to your environment
silence_threshold = 30  # seconds
loopvalue=False
start_time = None 
x=True
count=0
validuser=True
Page_refresh=True

def is_speaking(audio_data):
    # Calculate the root mean square (RMS) amplitude
    rms = np.sqrt(np.mean(np.square(audio_data)))
    return rms > threshold


if validuser:
    def callback(indata, frames, time, status):


        global start_time, x , Page_refresh

        if start_time is None:
            start_time = time.currentTime

        if is_speaking(indata):
            print("You are speaking.")
            start_time = time.currentTime  # Update the last spoken time
        else:
            print("You are not speaking.")
            # print("")

        # Check if it has been more than 10 seconds since the last speech
        if time.currentTime - start_time > silence_threshold:
            print("No speech detected for more than 10 seconds. Terminating program.")
            x = False
            Page_refresh=False
            # raise sd.CallbackAbort  # Terminate the progr


        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

def start_recording(status,validity):
    global global_file, global_stream, q_data,validuser,x,count
    validuser=validity
    while status and count==0:

        
        
        with sf.SoundFile(filename, mode='w', samplerate=samplerate, channels=channels, subtype=subtype) as file:

            global_file = file

            with sd.InputStream(samplerate=samplerate, device=device, channels=channels, callback=callback):

                global_stream = sd.InputStream(samplerate=samplerate, device=device, channels=channels, callback=callback)
                
                while x:

                    if not st.session_state.recording:
                        break
                    data = q.get()
                
                    file.write(data)
                    if x==False:
                        break
        if x!=True:
            count=1
            return False                




def stop_recording(condition):
    global global_file, global_stream, q_data,validuser
    validuser=condition
    st.session_state.recording = False
    print('Recording finished:', repr(filename))
    # removing_noise(i)
    





