# 🇳🇱 Dutch Language Learning Agents

This project is a personalized AI-based language coaching system built using **Streamlit**, **OpenAI (GPT-4o-mini)**, and optionally **Composio**.  
It helps you actively learn Dutch every day by teaching new vocabulary, grammar, practicing conversations, and organizing your weekly learning plan.

---

## 🚀 Project Overview

The system creates a complete Dutch learning workflow with four specialized AI agents:

| Agent | Role |
|:------|:-----|
| 📚 Vocabulary Teacher | Teaches you 5–10 important Dutch words and phrases daily with examples and explanations (Dutch + English). |
| ✍️ Grammar Coach | Provides daily grammar lessons with simple explanations and short exercises. |
| 🗣️ Conversation Trainer | Simulates Dutch job interview conversations, corrects your Dutch, and builds your speaking confidence. |
| 📈 Weekly Learning Planner | Tracks your progress and organizes a study plan for the next week. |

Each agent organizes its output neatly and (optionally) creates a Google Doc for easy review.

---

## 🛠 Tech Stack

- [Python 3.9+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/)
- [Agno SDK](https://pypi.org/project/agno-sdk/) (Agent building framework)
- [Composio API](https://composio.dev/) (for Google Docs automation - optional)

---

## 🔑 Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/dutch-language-agents.git
    cd dutch-language-agents
    ```

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate     # On macOS/Linux
    venv\Scripts\activate.bat     # On Windows
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Prepare API Keys**
    - [Get an OpenAI API key](https://platform.openai.com/account/api-keys)
    - (Optional) [Get a Composio API key](https://app.composio.dev/)

5. **Run the application**
    ```bash
    streamlit run your_app.py
    ```

6. **Enter your API keys** in the sidebar when prompted.

---

## 🎯 Features

- 📚 **Learn Dutch Vocabulary Daily**  
- ✍️ **Master Dutch Grammar with Simple Explanations**  
- 🗣️ **Practice Realistic Dutch Conversations for Interviews**  
- 📈 **Track Your Weekly Progress**  
- 📄 **(Optional) Auto-save all lessons into Google Docs**

---

## 🌟 Future Improvements

- Add **learning memory** (agents remember your past mistakes and achievements).
- Add **speech-to-text** for real spoken Dutch practice.
- Build **leaderboards or streaks** to boost daily motivation.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgments

Special thanks to:
- [OpenAI](https://openai.com/) for the AI models.
- [Streamlit](https://streamlit.io/) for the fast and easy app framework.
- [Composio](https://composio.dev/) for enabling automation features.

---
