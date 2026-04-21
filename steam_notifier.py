import feedparser
import time
from plyer import notification
import os

# --- Configuration ---
RSS_FEED_URL = "https://www.reddit.com/r/GameDeals/new/.rss"
STEAM_KEYWORDS = ["steam"]
EPIC_KEYWORDS = ["epic games", "epic games store"]
FREE_KEYWORDS = [
    "(100% off/free)", "(100% off / free)",
    "(free/100% off)", "(free / 100% off)",
    "(100% off)", "free to keep", "(free / $"
]
# ---------------------

def send_notification(title, message):
    """Sends a desktop notification."""
    try:
        notification.notify(
            title=title, message=message,
            app_name="Game Notifier", timeout=20
        )
    except Exception as e:
        print(f"Error sending notification: {e}")

def check_for_free_games():
    """Parses the RSS feed and sends a notification if a new free game is found."""
    
    print(f"Checking {RSS_FEED_URL} for new deals...")
    feed = feedparser.parse(RSS_FEED_URL)
    
    if not feed.entries:
        print("Error: Could not fetch or parse the RSS feed.")
        return

    # --- THIS IS THE NEW DEBUG SECTION ---
    print("\n--- All Titles in the Current Feed (for debugging) ---")
    for entry in feed.entries:
        # This new line prints every title from the feed
        print(f"-> {entry.title}") 
    print("----------------------------------------------------\n")
    # --- END OF DEBUG SECTION ---

    print("--- Starting Filter ---")
    new_games_found = 0
    
    for entry in feed.entries:
        title_lower = entry.title.lower()
        
        has_free = any(kw in title_lower for kw in FREE_KEYWORDS)
        
        if has_free:
            if any(kw in title_lower for kw in STEAM_KEYWORDS):
                print(f"Found free Steam game: {entry.title}")
                send_notification("Free Steam Game!", entry.title)
                new_games_found += 1
                
            elif any(kw in title_lower for kw in EPIC_KEYWORDS):
                print(f"Found free Epic Games game: {entry.title}")
                send_notification("Free Epic Game!", entry.title)
                new_games_found += 1
            
    if new_games_found == 0:
        print("No free Steam or Epic games found in the latest feed.")
    print("-----------------------")

if __name__ == "__main__":
    check_for_free_games()