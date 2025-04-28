import streamlit as st
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from composio_phidata import Action, ComposioToolSet
import os
from agno.utils.pprint import pprint_run_response
from agno.tools.serpapi import SerpApiTools  # (not used yet, but keep for future)

# --- Streamlit Setup ---
st.set_page_config(page_title="🇳🇱 Dutch Learning Agent Team", layout="centered")

# --- Initialize Session State ---
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = ''
if 'composio_api_key' not in st.session_state:
    st.session_state['composio_api_key'] = ''
if 'serpapi_api_key' not in st.session_state:
    st.session_state['serpapi_api_key'] = ''
if 'daily_input' not in st.session_state:
    st.session_state['daily_input'] = ''
if 'weekly_summary' not in st.session_state:
    st.session_state['weekly_summary'] = ''

# --- Sidebar for API Keys ---
with st.sidebar:
    st.title("🔑 API Keys Configuration")
    st.session_state['openai_api_key'] = st.text_input("Enter your OpenAI API Key", type="password").strip()
    st.session_state['composio_api_key'] = st.text_input("Enter your Composio API Key", type="password").strip()
    
    st.info("💡 Tip: You can view detailed responses also in the terminal.")

# --- Check API Keys ---
if not st.session_state['openai_api_key'] or not st.session_state['composio_api_key']:
    st.error("Please enter your OpenAI and Composio API keys.")
    st.stop()

# --- Set environment variable for OpenAI ---
os.environ["OPENAI_API_KEY"] = st.session_state['openai_api_key']

# --- Initialize Composio Tools ---
try:
    composio_toolset = ComposioToolSet(api_key=st.session_state['composio_api_key'])

    create_tools = composio_toolset.get_tools(actions=[Action.GOOGLEDOCS_CREATE_DOCUMENT])
    update_tools = composio_toolset.get_tools(actions=[Action.GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT])

    if not create_tools:
        st.error("❌ Could not find the Google Docs Create Document tool. Check if Google Docs is connected in Composio.")
        st.stop()
    if not update_tools:
        st.error("❌ Could not find the Google Docs Update Document tool. Check if Google Docs is connected in Composio.")
        st.stop()

    google_docs_tool = create_tools[0]
    google_docs_tool_update = update_tools[0]

except Exception as e:
    st.error(f"❌ Error initializing Composio tools: {e}")
    st.stop()


# 1. Daily Language Coach
daily_coach_agent = Agent(
    name="Dutch Vocabulary Teacher",
    role="Dutch Vocabulary Teacher",
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
    tools=[google_docs_tool],
    instructions=[
        "Teach the user 5 to 10 new important Dutch words or phrases daily that are useful for Dutch-speaking job interviews.",
        "For each word or phrase, provide:",
        "- The Dutch word/phrase",
        "- English translation",
        "- Example sentence in Dutch",
        "- English translation of the example sentence",
        "- Quick tip on when to use it (formally, casually, common interview situations)",
        "Be supportive, motivating, and realistic.",
        "After generating the feedback, use the provided Google Docs tool to create a real Google Document with the content you wrote. Then include the actual Google Doc link in your final response.",
        "Make sure to include the link to the Google Doc in your response.",
        "Use the Google Docs tool to create a new document for each daily feedback session.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# 2. Language Assessor
language_assessor_agent = Agent(
    name="Dutch Grammar Coach",
    role="Dutch Grammar Coach",
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
    tools=[google_docs_tool],
    instructions=[
        "Teach the user 1 key Dutch grammar topic daily that is important for Dutch-speaking job interviews.",
        "Explain the grammar concept in simple Dutch, and also add an English explanation.",
        "Give at least 3 Dutch example sentences using the grammar rule, with English translations.",
        "Provide a few short exercises (fill in the blanks, correct the sentence, etc.) based on the topic.",
        "Create a well-formatted Google Doc with today's grammar lesson and exercises.",
        "Return the real Google Doc link to the user."
    ],
    show_tool_calls=True,
    markdown=True,
)

# 3. Weekly Language Planner
weekly_planner_agent = Agent(
    name="Weekly Language Planner",
    role="Dutch Learning Tracker and Planner",
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
    tools=[google_docs_tool],
    instructions=[
        "Track the user's Dutch learning journey: topics mastered, new vocabulary learned, common mistakes identified.",
        "Create a clear weekly study plan: topics to review, new topics to study, and daily activities.",
        "Organize the plan in a simple weekly schedule format.",
        "Align all planning with the user's goal to prepare for Dutch-speaking job interviews at B1 level fluency.",
        "Store the weekly plan in a Google Doc and include the link in the response."
    ],
    show_tool_calls=True,
    markdown=True,
)

# 4. Virtual Dutch Partner
virtual_partner_agent = Agent(
    name="Virtual Dutch Partner",
    role="Dutch Conversation Practice Simulator",
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
    tools=[google_docs_tool],
    instructions=[
        "Simulate a realistic Dutch conversation based on job interviews or daily life topics.",
        "Adjust conversation difficulty to user's current level.",
        "Correct grammar, vocabulary, and structure politely and explain corrections.",
        "Suggest useful expressions or structures to sound more natural.",
        "Summarize the conversation, list key mistakes and suggestions for improvement.",
        "Store the conversation summary in a Google Doc and include the link in the response."
    ],
    show_tool_calls=True,
    markdown=True,
)

# --- UI Tabs: Daily and Weekly ---
tab1, tab2 = st.tabs(["📅 Daily Routine", "📈 Weekly Planner"])

# --- Daily Routine ---
with tab1:
    st.title("📅 Daily Dutch Learning Routine")

    st.session_state['daily_input'] = st.text_area(
        "Paste your daily Dutch exercises, answers, or writing here:",
        placeholder="e.g., My speaking practice notes, grammar exercises, vocabulary list..."
    )

    if st.button("Run Daily Language Coach"):
        if not st.session_state['daily_input']:
            st.error("Please enter your daily input first.")
        else:
            with st.spinner("Coaching you..."):
                daily_coach_response: RunResponse = daily_coach_agent.run(st.session_state['daily_input'], stream=False)

            st.success("✅ Feedback generated!")
            st.markdown("### Google Doc Link:")
            st.markdown(daily_coach_response.content)
            pprint_run_response(daily_coach_response, markdown=True)

    if st.button("Run Language Assessor"):
        if not st.session_state['daily_input']:
            st.error("Please enter your daily input first.")
        else:
            with st.spinner("Testing your Dutch skills..."):
                assessor_response: RunResponse = language_assessor_agent.run(st.session_state['daily_input'], stream=False)

            st.success("✅ Assessment complete!")
            st.markdown("### Google Doc Link:")
            st.markdown(assessor_response.content)
            pprint_run_response(assessor_response, markdown=True)

    if st.button("Practice Dutch Conversation"):
        with st.spinner("Starting conversation..."):
            conversation_response: RunResponse = virtual_partner_agent.run(
                "Let's simulate a Dutch conversation based on today's practice. Focus on realistic interaction and interview style.",
                stream=False
            )

        st.success("✅ Conversation complete!")
        st.markdown("### Google Doc Link:")
        st.markdown(conversation_response.content)
        pprint_run_response(conversation_response, markdown=True)

# --- Weekly Planner ---
with tab2:
    st.title("📈 Weekly Dutch Learning Planner")

    st.session_state['weekly_summary'] = st.text_area(
        "Write a quick summary of your week's learning progress:",
        placeholder="e.g., This week I learned about verb conjugations and practiced speaking about my hobbies."
    )

    if st.button("Generate Weekly Plan"):
        if not st.session_state['weekly_summary']:
            st.error("Please enter your weekly summary first.")
        else:
            with st.spinner("Building your weekly plan..."):
                weekly_response: RunResponse = weekly_planner_agent.run(st.session_state['weekly_summary'], stream=False)

            st.success("✅ Weekly plan created!")
            st.markdown("### Google Doc Link:")
            st.markdown(weekly_response.content)
            pprint_run_response(weekly_response, markdown=True)
