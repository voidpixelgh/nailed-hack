import streamlit as st
from streamlit_pills import pills
from st_utils import (
    add_builder_config,
    add_sidebar,
    get_current_state,
)

current_state = get_current_state()

####################
#### STREAMLIT #####
####################

st.set_page_config(
    page_title="Build a RAGs chatbot, powered by Vectara & LlamaIndex 💬🦙",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("Build a RAGs chatbot, powered by Vectara & LlamaIndex 💬🦙")
st.info(
    "Use this page to build your RAG bot over your data!"
)

if "vectara_api_key" not in st.secrets:
    st.error("**NOTE**: Misisng secret VECTARA_API_KEY")
if "vectara_customer_id" not in st.secrets:
    st.error("**NOTE**: Misisng secret VECTARA_CUSTOMER_ID")
if "vectara_corpus_id" not in st.secrets:
    st.error("**NOTE**: Misisng secret VECTARA_CORPUS_ID")

add_builder_config()
add_sidebar()

st.info(f"Currently building/editing agent: {current_state.cache.agent_id}", icon="ℹ️")

# add pills
selected = pills(
    "Outline your task!",
    [
        "I want to analyze this PDF file (data/nailed.pdf)",
        "I want to search over my document.",
    ],
    clearable=True,
    index=None,
)

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "What RAG bot do you want to build?"}
    ]


def add_to_message_history(role: str, content: str) -> None:
    message = {"role": role, "content": str(content)}
    st.session_state.messages.append(message)  # Add response to message history


for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


# TODO: this is really hacky, only because st.rerun is jank
if prompt := st.chat_input(
    "Your question",
):  # Prompt for user input and save to chat history
    # TODO: hacky
    if "has_rerun" in st.session_state.keys() and st.session_state.has_rerun:
        # if this is true, skip the user input
        st.session_state.has_rerun = False
    else:
        add_to_message_history("user", prompt)
        with st.chat_message("user"):
            st.write(prompt)

        # If last message is not from assistant, generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = current_state.builder_agent.chat(prompt)
                    st.write(str(response))
                    add_to_message_history("assistant", str(response))

        else:
            pass

        # check agent_ids again
        # if it doesn't match, add to directory and refresh
        agent_ids = current_state.agent_registry.get_agent_ids()
        # check diff between agent_ids and cur agent ids
        diff_ids = list(set(agent_ids) - set(st.session_state.cur_agent_ids))
        if len(diff_ids) > 0:
            # # clear streamlit cache, to allow you to generate a new agent
            # st.cache_resource.clear()
            st.session_state.has_rerun = True
            st.rerun()

else:
    # TODO: set has_rerun to False
    st.session_state.has_rerun = False
# with st.sidebar:

# print("Hello world")