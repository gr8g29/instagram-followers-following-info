### Instagram Follower Change Tracker Instructions ###
This script works by comparing a historical list of your followers with a new list you download from Instagram.

### Prerequisite: Install BeautifulSoup ###
Since this script parses HTML files, you must install the beautifulsoup4 library using the following command: 
pip install beautifulsoup4

### Step 1: Download Your Instagram Data (Manual Step) ###
You must manually request and download your follower data from Instagram's Account Center. This process is required for every time you want to check for changes. 
Make sure you are logged into your instagram account, then go to this link : https://accountscenter.instagram.com/info_and_permissions/ 
Export Information: Click Export your information.
Request an Export: Click the Create Export button.
Choose where to export: Click the Export to Device button.
Verify that your email address is correct, that is where you will get sent the link to your exported data.
Select Data to Export:
Choose "Some of your information".
Scroll down and select only Connections.
Format: Select JSON as the format, but note that the resulting file may still be an HTML file depending on the data set. The script handles both!
Choose a date range (e.g., "All time").
Submit Request: Submit the request. Instagram will email you a link to download a ZIP file (this can take a few minutes up to 48 hours, depending on their load).

### Step 2: Prepare the Files ###
Once you receive the ZIP file from Instagram:
Unzip the File: Extract the contents of the ZIP file.
Locate the Follower List: Inside the extracted folder, navigate to the connections folder. You are looking for a file named followers_1.json or followers.html.
Rename and Place the File:
Copy the follower list file (followers_1.json or followers.html).
Paste it into the same directory as the instagram_tracker.py script.
Rename this file to followers_current.data. (Using .data tells the script it could be any format, either JSON or HTML).

### Step 3: Run the Script ###
Open your terminal or command prompt.
Navigate to the directory where you saved instagram_tracker.py and followers_current.data.
Run the script:
python instagram_tracker.py

### How It Works on Each Run ###
First Run:
The script sees that followers_previous.json doesn't exist. It simply reads followers_current.json, saves a copy of it as followers_previous.json, and exits.
Subsequent Runs:
You download a new file from Instagram and rename it to followers_current.json.
The script compares followers_current.json against followers_previous.json.
It reports the difference (who unfollowed and who followed).
It deletes followers_current.json and uses the new list to overwrite followers_previous.json, preparing it for your next check.






### Instagram Non Mutual Followers Tracker Instructions ###
Follow Step 1 from your readme.md to download your data from Instagram.
Unzip the file you receive.
Go into the connections folder.
You need to locate the followers file (e.g., followers_1.json) and the following file (e.g., following.json or following_1.json).
Place both of these files in the same directory as the new non_mutual_tracker.py script.
Rename the files:
Rename the following list to following_current.data.
Rename the followers list to followers_current.data.
Open your terminal, navigate to the directory, and run the script:
python non_mutual_tracker.py
The script will then print the list of people you follow who are not following you back.
