from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOllama
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import time
import subprocess

# Response generator function
def response_generator():
    response = st.session_state.chain.invoke(
        {"text": prompt}
    )

    response_text = response["text"]
    
    # print(response_text)

    print(st.session_state.chain)

    return response_text

selected_model = False

st.title("🦜🔗 Ollama Chatbot")

if "model" not in st.session_state and "selected_model" in st.session_state and not selected_model:
    
    st.session_state.selected_model = st.selectbox('Select model', st.session_state.names, index=None,
   placeholder="Select model to chat with...", disabled=True)

    st.write("Chatting with 🤖", st.session_state.selected_model)

    st.session_state.prompt_template =ChatPromptTemplate.from_template("You are a helpful and knowledgeable assistant. {text}")

    st.session_state.model = ChatOllama(model=str(st.session_state.selected_model)
                    )

    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    st.session_state.chain = LLMChain(llm=st.session_state.model, prompt=st.session_state.prompt_template, memory=st.session_state.memory, output_parser=StrOutputParser(), name=st.session_state.selected_model)

    print(st.session_state.chain)

    selected_model = True

if "selected_model" in st.session_state and "model" in st.session_state:

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask your personal assistant a anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Assistant is typing..."):
                response = response_generator()
            message_placeholder = st.empty()
            
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
            
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            # st.write(full_response)


        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

else:

    result = subprocess.run(['ollama', 'list'], stdout=subprocess.PIPE)

    print(result.stdout.decode('utf-8'))

    # Assuming result.stdout.decode('utf-8') gives the output you posted
    output = result.stdout.decode('utf-8')

    st.session_state.names = tuple([line.split()[0] for line in output.strip().split('\n')[1:]])

    print(st.session_state.names)

    st.write("Choose a model to start chatting")

    st.session_state.selected_model = st.selectbox('Select model', st.session_state.names, index=None,
   placeholder="Select model to chat with...", disabled=False)
    