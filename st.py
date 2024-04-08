import pkg_resources
from os import system
import arbitaray
import streamlit as st
import time

import soundfile as sf
import noisereduce as nr
import speechtoText


if(arbitaray.Page_refresh):


    if 'sessionTerminate' not in st.session_state:
        st.session_state.sessionTerminate = False

    if 'recording' not in st.session_state:
        st.session_state.recording = False

    if 'Q_count' not in st.session_state:
        st.session_state.Q_count = 0

    if 'condition_executed' not in st.session_state:
        st.session_state.condition_executed = False  # Add a flag to track whether the condition has been executed

    countx = 0

    def read_Q_file(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            return lines

    lines_data = read_Q_file('file.txt')
    Q_store = ''

    for line in lines_data:
        line.strip()
        Q_store += line

    def filtering_process(Q_TEXT):
        Q_TEXT = Q_TEXT.replace("\n", "")
        Q_TEXT = Q_TEXT.replace("farq", "difference")
        Q_TEXT = Q_TEXT.split("?")
        Q_TEXT.pop(len(Q_TEXT)-1)
        return Q_TEXT

    filter_Q = filtering_process(Q_store)

    def my_text_speech(text_line):
        system("say {}".format(text_line))

    def continue_process(i):
        global countx
        if (len(filter_Q)-1) >= i:
            filename = i + 1
            filename = str(filename)
            filter_Q[i] = filter_Q[i].replace("Q#"+filename+":", "")
            st.write("Q#"+filename+":"+filter_Q[i])
            my_text_speech(filter_Q[i])
            countx = 1 + countx
            print(countx, "value")
        else:
            st.success("interview Complete")

    def remove_noise(filename):
        dataq, samplerateq = sf.read("output7.wav")
        reduced_noise = nr.reduce_noise(y=dataq, sr=samplerateq)
        sf.write("speech/output_denoised"+str(filename+1)+".wav", reduced_noise, samplerateq)

    if st.button("Start Rec") and not st.session_state.sessionTerminate:
            st.sidebar.image("img/microphone.png", use_column_width=True, caption="Microphone")
            st.session_state.recording = True
            status = arbitaray.start_recording(True, True)
            if status == False:
                st.session_state.sessionTerminate = True
                st.error("Session is End")
        

    if st.button("Stop Rec") and not st.session_state.sessionTerminate:
        st.sidebar.empty()  # Clear the sidebar if Stop button is clicked
        arbitaray.start_recording(False, False)
        arbitaray.stop_recording(False)
        remove_noise(st.session_state.Q_count)
        st.write("Stop Recording..........")
        st.session_state.Q_count += 1
        time.sleep(1)
        continue_process(st.session_state.Q_count)
        speechtoText.start_speech_to_text(st.session_state.Q_count)
        time.sleep(1)

    elif st.session_state.Q_count == 0 and countx == 0 and not st.session_state.sessionTerminate and not st.session_state.condition_executed:
        time.sleep(3)
        continue_process(st.session_state.Q_count)
        st.session_state.condition_executed = True  # Set the flag to True to indicate that the condition has been executed

    if st.session_state.sessionTerminate:
        st.error("Your session has ended")
        print('According to me my account is blocked')
else:
    st.error("YOUR Session Is END")



