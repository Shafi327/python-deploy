import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === CONFIGURATION ===
user = "ImranKhanPTI"
hashtag = "#imrankhan"
since_date = "2025-04-01"
until_date = "2025-04-30"
language = "en"
limit = 1000

# === QUERY ===
query = f"from:{user} {hashtag} since:{since_date} until:{until_date} lang:{language}"

# === SCRAPE TWEETS ===
tweets = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= limit:
        break
    # Filter tweets with link, media, or hashtags
    if "http" in tweet.content or "#" in tweet.content or tweet.media:
        tweets.append([
            tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
            tweet.id,
            tweet.content,
            tweet.user.username,
            tweet.url
        ])

df = pd.DataFrame(tweets, columns=["Date", "Tweet ID", "Content", "Username", "URL"])

# === SAVE LOCALLY ===
filename = f"imrankhan_tweets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(filename, index=False)
print(f"[✓] Saved {len(df)} tweets to {filename}")

# === GOOGLE SHEETS UPLOAD ===
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("my-new-project-399913-535b3d575c8c.json", scope)
client = gspread.authorize(creds)

# Open your sheet (rename as needed)
sheet = client.open("Imran Khan Tweets").sheet1
sheet.clear()

# Upload header and data
sheet.insert_row(df.columns.tolist(), 1)
for row in df.values.tolist():
    sheet.append_row(row)

print("[✓] Uploaded data to Google Sheets successfully.")
