import json
import os
from bs4 import BeautifulSoup

# --- Configuration ---
# You must download both your 'followers' and 'following' lists from Instagram
# and place them in the same directory as this script.
FOLLOWERS_DATA_FILE = "followers_current.data"
FOLLOWING_DATA_FILE = "following_current.data" 
# ---------------------

def load_usernames(filepath):
    """
    Loads and parses the list of usernames from either a JSON or an HTML file 
    downloaded from Instagram (followers or following).
    Returns a set of usernames or an empty set if the file is not found/parsed.
    """
    if not os.path.exists(filepath):
        print(f"🛑 Error: Required file not found: {filepath}.")
        print("Please ensure you have downloaded your Instagram data and correctly named the files.")
        return set()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Attempt JSON Parsing
    try:
        data = json.loads(content)
        
        # Check for the common structure: a list of objects with a 'value' key
        if isinstance(data, list) and all('value' in item for item in data if isinstance(item, dict)):
            print(f"✅ Successfully parsed {filepath} as JSON.")
            return {item.get('value') for item in data if 'value' in item}
        
        # Handle potential other JSON wrappers (like in your existing script)
        if isinstance(data, dict):
            for key, value in data.items():
                 if isinstance(value, list) and all('value' in item for item in value if isinstance(item, dict)):
                    print(f"✅ Successfully parsed {filepath} as nested JSON.")
                    return {item.get('value') for item in value if 'value' in item}

    except json.JSONDecodeError:
        print(f"File {filepath} is not valid JSON. Trying HTML parsing...")
    except Exception as e:
        print(f"An error occurred during JSON parsing of {filepath}: {e}. Trying HTML parsing...")

    # Attempt HTML Parsing
    try:
        soup = BeautifulSoup(content, 'html.parser')
        usernames = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('https://www.instagram.com/'):
                parts = [p for p in href.split('/') if p]
                if parts and parts[-1] not in ['followers_and_following']:
                     usernames.add(parts[-1])
            
            text_content = link.get_text().strip()
            if text_content and not text_content.startswith('http'):
                usernames.add(text_content)

        if usernames:
            print(f"✅ Successfully parsed {filepath} as HTML.")
            return usernames
        else:
            print(f"⚠️ Warning: Could not find any data in {filepath} using JSON or HTML parsing.")
            return set()
            
    except Exception as e:
        print(f"An unexpected error occurred during HTML parsing of {filepath}: {e}")
        return set()
        
    return set()

def find_non_mutual():
    """
    Loads follower and following lists and finds who you follow that doesn't 
    follow you back.
    """
    print("--- 🧐 Instagram Non-Mutual Follower Tracker ---")
    
    # 1. Load the list of accounts *you* follow (your 'following' list)
    following_list = load_usernames(FOLLOWING_DATA_FILE)
    
    # 2. Load the list of accounts that follow *you* (your 'followers' list)
    followers_list = load_usernames(FOLLOWERS_DATA_FILE)
    
    if not following_list:
        print("\nCannot proceed: Following list is empty or could not be loaded.")
        return
    if not followers_list:
        print("\nCannot proceed: Followers list is empty or could not be loaded.")
        return

    # 3. Perform the comparison
    # Non-Mutual: Accounts in your FOLLOWING list but NOT in your FOLLOWERS list
    # This represents people you follow who do not follow you back.
    non_mutuals = following_list - followers_list
    
    # 4. Display Results
    
    print("-" * 40)
    print(f"Total Accounts You Follow: {len(following_list)}")
    print(f"Total Accounts Following You: {len(followers_list)}")

    print(f"\n--- 🚫 YOU FOLLOW, BUT THEY DON'T FOLLOW BACK ({len(non_mutuals)}) ---")
    
    if non_mutuals:
        for i, user in enumerate(sorted(non_mutuals)):
            print(f"{i+1}. @{user}")
    else:
        print("🙌 Great! Everyone you follow is following you back.")
        
    print("-" * 40)

if __name__ == "__main__":
    find_non_mutual()