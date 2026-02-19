# ✨ Mood Discovery Bot: An Intelligent Terminal Explorer

An AI-powered terminal companion that analyzes your mood to curate personalized knowledge journeys. This project bridges the gap between **Natural Language Processing (NLP)** and interactive knowledge discovery.

---

## 🌟 Key Features

* **🧠 Sentiment Analysis:** Uses `TextBlob` to analyze your current mood. Based on your input, the bot selects topics that either match your energy or provide a calm perspective.
* **📚 Wikipedia Integration:** Dynamically fetches "Intelligence Briefings" using the `wikipedia-api`.
* **🎙️ Integrated Voice Synthesis:** Don't want to read? The bot can narrate summaries using `pyttsx3` with a built-in "press Enter to stop" threading feature.
* **🎨 Stylized UI:** Powered by the `Rich` library, featuring centered panels, color-coded tables, and clean prompts for a premium terminal experience.
* **🛡️ Robust Error Handling:** Includes a "Zen Fallback" mode. If Wikipedia is unreachable, the bot provides a moment of reflection instead of crashing.
* **📜 History Tracking:** Automatically logs your discoveries so you can revisit your intellectual path.

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed. You will also need to install the following dependencies:

```bash
pip install wikipediaapi pyttsx3 textblob rich
