from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *
import os
from streamlit_option_menu import option_menu
from dbtransactions import TransactionFetcher
from dbinventory import InventoryFetcher
import keys
import speech_recognition as sr
import threading


recognizer = sr.Recognizer()

recognized_text = st.empty()
enable_speech_recognition = st.checkbox("Enable Speech Recognition")

ever_turned_on=0







os.environ['OPENAI_API_KEY']="INSERT_KEY_HERE"

st.subheader("Chatbot")

selected = option_menu(
    menu_title=None,
    options=["General", "User Specific"],
    default_index=0,
    orientation="horizontal",
)

if selected == "General":
    st.title(f"{selected}")
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


    # system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
    # and if the answer is not contained within the text below, say 'I don't know'""")

    system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question by using the information given to you  and you can also give your own inputs when required  '""")


    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)




    # container for chat history
    response_container = st.container()
    # container for text box


    # Create a button to open the pop-up box
    if st.button("Open Pop-up Box"):
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = True
        else:
            st.session_state.show_popup = not st.session_state.show_popup

    # Display the pop-up box if the toggle is True
    if st.session_state.get('show_popup', False):
        with st.form("popup_form"):
            st.subheader("Pop-up Box")
            mail = st.text_input("Mail")
            query = st.text_input("Query")
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Process the submitted data
                # Add your logic here
                st.success(f"Submitted: Mail - {mail}, Query - {query}")
                send_mail(mail, query)
                # add_QA_DB(query, "", mail, answered=False)
                st.session_state.show_popup = False  # Close the pop-up box after submitting

    textcontainer = st.container()



    with textcontainer:
        # Start/Stop recording based on checkbox state
        query1=""
        query=None
        count=0
        while enable_speech_recognition:
            ever_turned_on=1
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                if count==0:
                    st.success("Recording... Speak something!")

                
                query1=""
                # while enable_speech_recognition:
                print(f"The button is {enable_speech_recognition}")
                print(count)
                count+=1
                audio = recognizer.listen(source, timeout=None)  # No timeout

                # Attempt to recognize audio
                try:
                    
                    audio_text=""  
                        
                    text = recognizer.recognize_google(audio)
                    
                    recognized_text.text(text)
                    audio_text+=text
                    
                    query1+=audio_text
                    print(query1)
                    if count==1:
                        with open('temp.txt', 'w') as file:
                            # Write the number to the file as a string
                            file.write(query1)
                    else:
                        with open('temp.txt', 'a') as file:
                                # Write the number to the file as a string
                                file.write(query1)
                except sr.UnknownValueError:
                    pass  # No recognized text for this audio)
        with open('temp.txt', 'r') as file:
            # Read the content of the file
            query1 = file.read()

        # Convert the content back to an integer
        if query1:   
            print("exited with")    
            print(query1)           
            if query1:
                with st.spinner("thinking..."):
                    # conversation_string = get_conversation_string()
                    # st.code(conversation_string)
                    # refined_query = query_refiner(conversation_string, query)
                    # st.subheader("Refined Query:")
                    # st.write(query)
                    
                    context = find_match(query1)
                    
                    # print(context)  
                    response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query1}")
                
                st.session_state.requests.append(query1)
                st.session_state.responses.append(response)
                ever_turned_on=0
            with open('temp.txt', 'w') as file:
                file.write("")
        print(f"we are out and the button is The button is {enable_speech_recognition}")
        query = st.text_input("Query: ",key="input")
        if query:
            with st.spinner("typing..."):
                # conversation_string = get_conversation_string()
                # st.code(conversation_string)
                # refined_query = query_refiner(conversation_string, query)
                # st.subheader("Refined Query:")
                # st.write(query)
                
                context = find_match(query)
                
                # print(context)  
                response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
            
            st.session_state.requests.append(query)
            st.session_state.responses.append(response) 
            # if(response != "I don't know"):
            #     add_QA_DB(query, response, "")
            # else:
            #     add_QA_DB_NoAns(query)
        
            
    with response_container:
        if st.session_state['responses']:

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

def show_chat(userfinal,passfinal, transaction_fetcher):
    context2 = transaction_fetcher.fetch_transactions_by_user(userfinal, passfinal)
    print(context2)
    
    # Display the chat interface here
    st.title(f"{selected}")
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    llm2 = ChatOpenAI(model_name="gpt-3.5-turbo")

    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


    # system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
    # and if the answer is not contained within the text below, say 'I don't know'""")

    system_msg_template2 = SystemMessagePromptTemplate.from_template(template="""Answer the question by using the information give to you and based on that give more inputs from your side'""")


    human_msg_template2 = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template2 = ChatPromptTemplate.from_messages([system_msg_template2, MessagesPlaceholder(variable_name="history"), human_msg_template2])

    conversation2 = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template2, llm=llm2, verbose=True)




    # container for chat history
    response_container2 = st.container()
    # container for text box


    # Create a button to open the pop-up box
    if st.button("Open Pop-up Box"):
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = True
        else:
            st.session_state.show_popup = not st.session_state.show_popup

    # Display the pop-up box if the toggle is True
    if st.session_state.get('show_popup', False):
        with st.form("popup_form"):
            st.subheader("Pop-up Box")
            mail = st.text_input("Mail")
            query = st.text_input("Query")
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Process the submitted data
                # Add your logic here
                st.success(f"Submitted: Mail - {mail}, Query - {query}")
                send_mail(mail, query)
                # add_QA_DB(query, "", mail, answered=False)
                st.session_state.show_popup = False  # Close the pop-up box after submitting

    textcontainer2 = st.container()



    with textcontainer2:
        query2 = st.text_input("Query: ", key="input")
        if query2:
            with st.spinner("typing..."):
                # conversation_string = get_conversation_string()
                # st.code(conversation_string)
                # refined_query = query_refiner(conversation_string, query)
                # st.subheader("Refined Query:")
                # st.write(query)
                
                # context = find_match(query)

                
                # print(context)  
                context2 = transaction_fetcher.fetch_transactions_by_user(userfinal, passfinal)
                print(context2)

                response2 = conversation2.predict(input=f"Context:\n {context2} \n\n Query:\n{query2}")
            
            st.session_state.requests.append(query2)
            st.session_state.responses.append(response2) 
            # if(response != "I don't know"):
            #     add_QA_DB(query, response, "")
            # else:
            #     add_QA_DB_NoAns(query)
            
    with response_container2:
        if st.session_state['responses']:

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
    st.write("Chat interface will be displayed here.")

    
if selected == "User Specific":
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'Mhash@win576',
        'host': 'db.eoehrierllfhmxlltdyf.supabase.co'
    }

    transaction_fetcher = TransactionFetcher(db_params)
    with open(r"C:\Users\daksh\OneDrive\Desktop\hackathons\MHash\mhashauthentication\mhash-agri-main-template\username.txt", "r") as username_file:
        userfinal = username_file.read()
    with open(r"C:\Users\daksh\OneDrive\Desktop\hackathons\MHash\mhashauthentication\mhash-agri-main-template\password.txt", "r") as password_file:
        passfinal = password_file.read()

    
    show_chat(userfinal, passfinal, transaction_fetcher)






    
if selected == "Inventory": 
    db_params2 = {
        'dbname': 'mhash',
        'user': 'postgres',
        'password': 'Mhash@win576',
        'host': 'db.eoehrierllfhmxlltdyf.supabase.co'
    }

    inventory_fetcher = InventoryFetcher(db_params2)
    context2 = inventory_fetcher.fetch_stock()
    
    # Display the chat interface here
    st.title(f"{selected}")
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    llm2 = ChatOpenAI(model_name="gpt-3.5-turbo")

    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


    # system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
    # and if the answer is not contained within the text below, say 'I don't know'""")

    system_msg_template2 = SystemMessagePromptTemplate.from_template(template="""Answer the question by only using the information given to you in the query and no inputs from your side, 
    and if the answer is not contained within the text below, say 'I don't know'""")


    human_msg_template2 = HumanMessagePromptTemplate.from_template(template="{input}")
    

    prompt_template2 = ChatPromptTemplate.from_messages([system_msg_template2, MessagesPlaceholder(variable_name="history"), human_msg_template2])

    conversation2 = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template2, llm=llm2, verbose=True)




    # container for chat history
    response_container2 = st.container()
    # container for text box


    # Create a button to open the pop-up box
    if st.button("Open Pop-up Box"):
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = True
        else:
            st.session_state.show_popup = not st.session_state.show_popup

    # Display the pop-up box if the toggle is True
    if st.session_state.get('show_popup', False):
        with st.form("popup_form"):
            st.subheader("Pop-up Box")
            mail = st.text_input("Mail")
            query = st.text_input("Query")
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Process the submitted data
                # Add your logic here
                st.success(f"Submitted: Mail - {mail}, Query - {query}")
                send_mail(mail, query)
                # add_QA_DB(query, "", mail, answered=False)
                st.session_state.show_popup = False  # Close the pop-up box after submitting

    textcontainer2 = st.container()



    with textcontainer2:
        query2 = st.text_input("Query: ", key="input")
        if query2:
            with st.spinner("typing..."):
                # conversation_string = get_conversation_string()
                # st.code(conversation_string)
                # refined_query = query_refiner(conversation_string, query)
                # st.subheader("Refined Query:")
                # st.write(query)
                
                # context = find_match(query)

                
                # print(context)  
                print(context2)
                response2 = conversation2.predict(input=f"Context:\n {context2} \n\n Query:\n{query2}")
            
            st.session_state.requests.append(query2)
            st.session_state.responses.append(response2) 
            # if(response != "I don't know"):
            #     add_QA_DB(query, response, "")
            # else:
            #     add_QA_DB_NoAns(query)
            
    with response_container2:
        if st.session_state['responses']:

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
    st.write("Chat interface will be displayed here.")
    st.title(f"{selected}")

