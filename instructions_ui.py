import streamlit as st

# Replace this with the actual content of your instruction dictionary
instruction = {
    "introduction": "Welcome to the AI Interviewer!",
    "quick_start": "Here's how to get started...",
    "interface": "The interface works as follows...",
    "models": "We use the following models...",
    "acknowledgements": "Thanks to...",
    "legal": "Legal information..."
}

# Replace this with a simple function if you don't have the utils.ui module
def get_status_color(manager):
    return "🟢" if manager.is_working() else "🔴"

def get_instructions_ui(llm, tts, stt, default_audio_params):
    st.title("Instructions")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(instruction["introduction"])

    with col2:
        space = "&nbsp;" * 10

        tts_status = get_status_color(tts)
        st.markdown(f"TTS status: {tts_status}{space}{tts.config.tts.name}", unsafe_allow_html=True)

        stt_status = get_status_color(stt)
        st.markdown(f"STT status: {stt_status}{space}{stt.config.stt.name}", unsafe_allow_html=True)

        llm_status = get_status_color(llm)
        st.markdown(f"LLM status: {llm_status}{space}{llm.config.llm.name}", unsafe_allow_html=True)

    st.markdown(instruction["quick_start"])

    col3, col4 = st.columns([2, 1])

    with col3:
        st.markdown(instruction["interface"])

    with col4:
        st.markdown("Bot interaction area will look like this. Use Record button to record your answer.")
        st.markdown("Click 'Send' to send you answer and get a reply.")
        
        # Simulating chat example
        st.chat_message("user").write("Candidate message")
        st.chat_message("assistant").write("Interviewer message")
        
        # Simulating send button and audio input
        st.button("Send", disabled=True)
        st.audio(None, format="audio/wav")  # Placeholder for audio input

    st.markdown(instruction["models"])
    st.markdown(instruction["acknowledgements"])
    st.markdown(instruction["legal"])

# Dummy classes for demonstration
class DummyManager:
    def is_working(self):
        return True
    
    class config:
        class tts:
            name = "Dummy TTS"
        class stt:
            name = "Dummy STT"
        class llm:
            name = "Dummy LLM"

# Main Streamlit app
if __name__ == "__main__":
    llm = DummyManager()
    tts = DummyManager()
    stt = DummyManager()
    default_audio_params = {}

    get_instructions_ui(llm, tts, stt, default_audio_params)