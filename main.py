import wikipediaapi
import pyttsx3
import random
import os
import threading
from textblob import TextBlob
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align
from rich.table import Table

console = Console()
engine = pyttsx3.init()

# FIX: Added a more specific User-Agent to prevent Wikipedia from blocking you
wiki = wikipediaapi.Wikipedia(
    user_agent="MoodDiscoveryBot/3.0 (https://yourwebsite.com; contact@email.com)", 
    language='en'
)

HISTORY_FILE = "history.log"

# --- ASSETS ---
MOOD_ASSETS = {
    "positive": {
        "quotes": ["\"Joy is the simplest form of gratitude.\"", "\"The more grateful I am, the more beauty I see.\""],
        "keywords": ["Happiness", "Renaissance", "Wonder"],
        "closings": ["Keep that light shining! ✨", "Have a brilliant day! 🌟"]
    },
    "negative": {
        "quotes": ["\"The root of joy is gratefulness.\"", "\"Quiet the mind, and the soul will speak.\""],
        "keywords": ["Stoicism", "Resilience", "Lighthouse"],
        "closings": ["This too shall pass. 🌿", "Be gentle with yourself. 🕯️"]
    },
    "neutral": {
        "quotes": ["\"Be present in all things.\"", "\"Look at everything as if for the first time.\""],
        "keywords": ["Architecture", "Cosmology", "Philosophy"],
        "closings": ["Stay curious. 🌎", "Knowledge is the best companion. 📚"]
    }
}

# --- FUNCTIONS ---

def save_to_history(topic):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(topic + "\n")

def get_recent_history(n=5):
    if not os.path.exists(HISTORY_FILE): return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return f.read().splitlines()[-n:][::-1]

def fetch_safe_page(title):
    """Bulletproof fetch to handle 'Wikipedia Not Available' errors."""
    try:
        p = wiki.page(title)
        # Force a network check immediately
        summary_text = p.summary[:500]
        if not summary_text:
            raise Exception("Empty Page")
        return p.title, summary_text
    except Exception:
        # If Wikipedia is down/blocked, provide this 'Zen' fallback
        return "Internal Peace", "It seems Wikipedia is currently unreachable. Use this moment to breathe. Silence is a source of great strength."

def speak_with_stop(text):
    """Speaks text; pressing Enter stops it immediately."""
    console.print("\n[italic grey]>> Press ENTER to stop audio and continue...[/italic grey]")
    
    engine.say(text)
    
    def run_voice():
        try:
            engine.startLoop(False)
            while engine.isBusy():
                engine.iterate()
            engine.endLoop()
        except:
            pass

    t = threading.Thread(target=run_voice, daemon=True)
    t.start()
    
    input() # Wait for user to hit Enter
    engine.stop()

# --- MAIN ---
print("\n" * 2)
console.print(Align.center(Panel.fit("[bold cyan]✨ THE MASTER HYBRID EXPLORER ✨[/bold cyan]")))

recent = get_recent_history()
if recent:
    table = Table(title="Recent Discoveries", show_header=True, header_style="bold magenta")
    table.add_column("No.", style="dim", width=4)
    table.add_column("Topic", style="cyan")
    for i, item in enumerate(recent, 1):
        table.add_row(str(i), item)
    console.print(Align.center(table))

print("\n")
console.print("[bold yellow]1. Mood Discovery[/bold yellow]")
console.print("[bold yellow]2. Specific Topic[/bold yellow]")
mode = Prompt.ask("Choose your path", choices=["1", "2"], default="1")

mood_cat = "neutral" 

if mode == "1":
    user_text = Prompt.ask("[bold magenta]How's your mood today?[/bold magenta]")
    polarity = TextBlob(user_text).sentiment.polarity
    mood_cat = "positive" if polarity > 0.2 else "negative" if polarity < -0.2 else "neutral"
    
    try:
        base = random.choice(MOOD_ASSETS[mood_cat]["keywords"])
        p_obj = wiki.page(base)
        links = list(p_obj.links.keys())
        final_title = random.choice(links) if links else base
    except:
        final_title = "Gratitude"
else:
    final_title = Prompt.ask("[bold magenta]What is your target topic?[/bold magenta]")

# Fetching with the safety net
res_title, res_summary = fetch_safe_page(final_title)

# --- RESULTS (Centered) ---
save_to_history(res_title)
current_quote = random.choice(MOOD_ASSETS[mood_cat]["quotes"])
current_closing = random.choice(MOOD_ASSETS[mood_cat]["closings"])

console.print(Align.center(f"\n[italic blue]{current_quote}[/italic blue]\n"))



panel_content = f"[bold cyan]Source:[/bold cyan] {res_title}\n\n{res_summary}..."
console.print(Align.center(Panel(panel_content, title="📚 Intelligence Briefing", border_style="magenta", width=80)))

if Prompt.ask("\nRead summary aloud?", choices=["y", "n"], default="y") == "y":
    speak_with_stop(res_summary)

print("\n")
console.print(Align.center(f"[bold grey]{current_closing}[/bold grey]"))
print("\n" * 2)
