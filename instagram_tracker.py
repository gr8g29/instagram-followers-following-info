import json
import os
import shutil
from datetime import datetime
from bs4 import BeautifulSoup

# --- Configuration ---
# File paths for the JSON or HTML files provided by Instagram
# 1. This is the new list you download before running the script.
CURRENT_DATA_FILE = "followers_current.data" 
# 2. This file stores the list from the last successful run.
PREVIOUS_DATA_FILE = "followers_previous.data" 
# NOTE: We use '.data' extension to allow it to be either JSON or HTML.
# You must ensure the file you download and rename contains the followers list.
# ---------------------

def load_follower_usernames(filepath):
    """
    Loads and parses the follower list from either a JSON or an HTML file 
    downloaded from Instagram.
    Returns a set of usernames or None if the file is not found.
    """
    if not os.path.exists(filepath):
        print(f"Error: Required file not found: {filepath}.")
        print(f"Please ensure you have placed the new data file and named it '{CURRENT_DATA_FILE}'.")
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Try JSON Parsing (The standard new format)
    try:
        data = json.loads(content)
        
        # Check for the common structure: a list of objects with a 'value' key
        if isinstance(data, list) and all('value' in item for item in data if isinstance(item, dict)):
            print(f"Successfully parsed {filepath} as JSON.")
            return {item.get('value') for item in data if 'value' in item}
        
        # Handle potential other JSON wrappers
        if isinstance(data, dict):
            for key, value in data.items():
                 if isinstance(value, list) and all('value' in item for item in value if isinstance(item, dict)):
                    print(f"Successfully parsed {filepath} as nested JSON.")
                    return {item.get('value') for item in value if 'value' in item}

    except json.JSONDecodeError:
        print(f"File {filepath} is not valid JSON. Trying HTML parsing...")
    except Exception as e:
        print(f"An error occurred during JSON parsing of {filepath}: {e}. Trying HTML parsing...")

    # 2. Try HTML Parsing (The older format)
    try:
        soup = BeautifulSoup(content, 'html.parser')
        usernames = set()
        
        # In the HTML format, usernames are usually inside <a> tags
        # and represent the link to the profile, which contains the username.
        for link in soup.find_all('a', href=True):
            # We look for links that look like an Instagram profile URL
            href = link['href']
            if href.startswith('https://www.instagram.com/'):
                # Extract the username from the URL path
                parts = [p for p in href.split('/') if p]
                if parts and parts[-1] not in ['followers_and_following']: # Exclude general folder link
                     usernames.add(parts[-1])
            
            # For the text inside the link tag (sometimes it's the username directly)
            text_content = link.get_text().strip()
            if text_content and not text_content.startswith('http'): # Simple check to avoid link text
                usernames.add(text_content)


        if usernames:
            print(f"Successfully parsed {filepath} as HTML.")
            return usernames
        else:
            print(f"Error: Could not find any follower data in {filepath} using JSON or HTML parsing techniques.")
            return set()
            
    except Exception as e:
        print(f"An unexpected error occurred during HTML parsing of {filepath}: {e}")
        return set()
        
    return set()

def run_tracker():
    """
    The main function to load, compare, and save the follower lists.
    """
    print("--- Instagram Follower Change Tracker ---")
    
    # 1. Load the new (current) list
    current_followers = load_follower_usernames(CURRENT_DATA_FILE)
    
    if current_followers is None:
        return # Exit if file not found
    if not current_followers:
        print("Warning: Current follower list is empty or could not be parsed.")
        return

    # 2. Load the previous (old) list
    if not os.path.exists(PREVIOUS_DATA_FILE):
        print("\n--- FIRST RUN DETECTED ---")
        print("No previous follower data found. Saving current data for future comparisons.")
        
        # Save the current file to the 'previous' file for the next run
        try:
            # We save the raw content of the current file to the previous data file
            shutil.copyfile(CURRENT_DATA_FILE, PREVIOUS_DATA_FILE)
            print(f"Success: Current list saved as '{PREVIOUS_DATA_FILE}'.")
            print(f"Total followers recorded: {len(current_followers)}")
            print("Please run the script again after your next Instagram data download to see changes.")
            return
        except Exception as e:
            print(f"Error: Failed to save previous follower file: {e}")
            return

    # If previous file exists, load it
    previous_followers = load_follower_usernames(PREVIOUS_DATA_FILE)

    if not previous_followers:
         print("Warning: Previous follower list is empty or could not be read. Cannot perform comparison. Saving current data.")
         shutil.copyfile(CURRENT_DATA_FILE, PREVIOUS_DATA_FILE)
         return
    
    # 3. Perform the comparison
    
    # Unfollowers: Accounts in the OLD list but NOT in the NEW list
    unfollowers = previous_followers - current_followers
    
    # New Followers: Accounts in the NEW list but NOT in the OLD list
    new_followers = current_followers - previous_followers
    
    # 4. Display Results
    
    print(f"\nTime of check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total followers in previous run: {len(previous_followers)}")
    print(f"Total followers in current run: {len(current_followers)}")
    print("-" * 30)

    print(f"\n--- 💔 UNFOLLOWED YOU ({len(unfollowers)}) ---")
    if unfollowers:
        for i, user in enumerate(sorted(unfollowers)):
            print(f"{i+1}. @{user}")
    else:
        print("🎉 No unfollowers detected since the last check!")

    print(f"\n--- ✨ NEW FOLLOWERS ({len(new_followers)}) ---")
    if new_followers:
        for i, user in enumerate(sorted(new_followers)):
            print(f"{i+1}. @{user}")
    else:
        print("Quiet day! No new followers detected.")
        
    print("-" * 30)
    
    # 5. Update the previous list for the next run
    try:
        # Overwrite the previous file with the current data
        shutil.copyfile(CURRENT_DATA_FILE, PREVIOUS_DATA_FILE)
        print(f"\nSuccessfully updated '{PREVIOUS_DATA_FILE}' for your next run.")
        os.remove(CURRENT_DATA_FILE) # Clean up the current file
        print(f"Cleaned up '{CURRENT_DATA_FILE}'.")
    except Exception as e:
        print(f"Error: Failed to update previous follower file for next run: {e}")

if __name__ == "__main__":
    run_tracker()