import streamlit as st
from streamlit_option_menu import option_menu
from clama_7b import display_code_lama_7B
from clama_13b import display_code_lama_13B
from clama_34b import display_code_lama_34B
from clama_70b import display_code_lama_70B


st.set_page_config(
        page_title="Coding LLMs",
)

# Define the sidebar
with st.sidebar:
    # Create the options menu
    selected = option_menu(menu_title="Coding Models",
                           options=["Code lama 7B", "Code lama 13B", "Code lama 34B","Code lama 70B"],
                           icons=["code-slash", "code-slash", "code-slash","code-slash"],
                           menu_icon="card-list",
                           default_index=0
                           )
    
if selected == "Code lama 7B":
    display_code_lama_7B(st.secrets["NVIDIA_API_KEY"])
elif selected == "Code lama 13B":
    display_code_lama_13B(st.secrets["NVIDIA_API_KEY"])
elif selected == "Code lama 34B":
    display_code_lama_34B(st.secrets["NVIDIA_API_KEY"])
elif selected == "Code lama 70B":
    display_code_lama_70B(st.secrets["NVIDIA_API_KEY"])