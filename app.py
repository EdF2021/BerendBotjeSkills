# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import streamlit as st
from PIL import Image

import openai

openai_api_key = os.getenv("OPENAI_API_KEY")
# openai_api_key = st.secrets["OPENAI_API_KEY"]


# IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images/productoer.jpeg')


image = Image.open("images/producttoer.jpeg")


from streamlit.logger import get_logger


LOGGER = get_logger(__name__)
ENCODINGS = 'cl100k_base'

def run():
    st.set_page_config(
            page_title="Berend-Botje Skills",
            page_icon="👋",
            layout="wide",
            initial_sidebar_state="collapsed"
            )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ## Welkom bij Berend-Botje Skills 👋 """)

        st.markdown("""
        ##### Berend-Botje is een slimme AI assistent die je helpt om *smart* te werken.""")
        st.markdown("""
        ###### Afhankelijk van de taak zal Berend een keuze maken welke skills er nodig zijn. De skills zijn allen **Powered by OpenAI** en maken gebruik van AI modellen als ChatGPT. Het verschil met ChatGPT is dat alle informatie binnen de omgeving van de gebruiker blijft!"""
        )
    with col2:
        st.image(image, caption=None, use_column_width=True, clamp=True, channels="RGB", output_format="auto")
    
    # st.sidebar.success("Kies één van Berend's skills")
    st.markdown(""" ##### 👈 Voorbeelden.
    **1. [De Lesplanner](Lesplan_Demo)**
    **2. [De Notulist](Mapping_Demo)**
    **3. [De Dataanalist](DataFrame_Demo)**
    **4. [De Datavormgever](Plotting_Demo)**
    **5. [De Chatbot](Chat_Demo)**
    **6. [De Samenvatter](Samenvatter_Demo)**


    **Disclaimer: Aan het gebruik, of resulaten van Berend-Botje Skills kunnen geen rechten worden verleend. Noch zijn wij aansprakelijk voor enig gevolg van dit gebruik. Bedenk dat de voorbeelden die hier getoond worden nog in een premature fase verkeren: het is werk onder constructie...** 
    """)


if __name__ == "__main__":
    run()
