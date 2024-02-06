import streamlit as st
import requests
import json
import time

@st.cache_data
def code_lama_13b(token,prompt,temp,top_p,seed):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/f6a96af4-8bf9-4294-96d6-d71aa787612e"

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "text/event-stream",
        "content-type": "application/json",
    }

    payload = {
        "messages": [
            {
                "content": f"{prompt}",
                "role": "user"
            }
        ],
        "temperature": temp,
        "top_p": top_p,
        "max_tokens": 1024,
        "seed": seed,
        "stream": True
    }

    try:
        response = requests.post(invoke_url, headers=headers, json=payload, stream=True)

        # List to store content values
        content_list = []

        # Get the total content length
        total_length = int(response.headers.get("content-length", 0))

        # Initialize progress bar
        progress_bar = st.progress(0)

        # Initialize progress counter
        progress_counter = 0

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                if decoded_line.startswith("data:"):
                    try:
                        json_data = json.loads(decoded_line[5:])
                        content = json_data["choices"][0]["delta"]["content"]
                        content_list.append(content)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")

                    # Update progress
                    if total_length > 0:
                        progress_counter += len(decoded_line)
                        progress_bar.progress(min(progress_counter / total_length, 1.0))
                        
                        # Add a small delay to allow the progress bar to update smoothly
                        time.sleep(0.01)

    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None

    # Now content_list contains all the 'content' values from the JSON data
    response_text = "".join(content_list)
    return response_text

def display_code_lama_13B(token):
    
    st.markdown("<h1 style=text-align:center;'>Code Llama 13B</h1>", unsafe_allow_html=True)
    # st.write("Code lama 13b hyper params")
    with st.sidebar:
        st.title("Parameters Tuning (13B)")
        st.session_state.val = st.slider("Select Temperature", key="slider1", min_value=0.1, max_value=1.0, value=0.4, step=0.1,help="Less Temp = More precise\n,High temperature = Creative")
        if st.session_state.val > 0.9:
            st.session_state.val = 1.0
        st.write('Temperature:', st.session_state.val)

        st.session_state.val1 = st.slider("Select Top_P", key="slider2", min_value=0.1, max_value=1.0, value=0.3, step=0.1,help = "nucleus sampling probability threshold")
        if st.session_state.val1 > 0.9:
            st.session_state.val1 = 1.0
        st.write('Top_P:', st.session_state.val1)

        st.session_state.val2 = st.slider("Select Seed", key="slider3", min_value=1, max_value=1000, value=42, step=1,help = "influences the variability of generated content")
        st.write('Seed:', st.session_state.val2)

    if "messages1" not in st.session_state:
        st.session_state["messages1"] =[]

    for msg in st.session_state.messages1:
        with st.chat_message(msg.get("role")):
            st.write(msg.get("content"))
    
    
    prompt = st.chat_input("Ask me anything related Coding:",max_chars=8000)
    # if st.button("Generate Code"):
    #     result = code_lama_7b(prompt,st.session_state.val,st.session_state.val1,st.session_state.val2)
    #     message(f"{result}")
    if prompt:
        st.session_state.messages1.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.write(prompt)
        # with st.chat_message("assistant"):
        #     result = code_lama_7b(prompt,st.session_state.val,st.session_state.val1,st.session_state.val2)
        #     st.write(result)
            
        result = code_lama_13b(token,prompt,st.session_state.val,st.session_state.val1,st.session_state.val2)

        st.session_state.messages1.append({"role":"assistant","content":result})
        with st.chat_message("assistant"):
            st.write(result)
