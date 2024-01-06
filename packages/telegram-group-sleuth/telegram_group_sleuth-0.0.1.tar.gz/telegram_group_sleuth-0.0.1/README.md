# telegram-group-sleuth
Extract and analyze data from Telegram group chats.


# Features:

- Extract messages, media, and metadata from public or private Telegram groups.
- Organize messages chronologically by user for easy analysis.
- Download shared media files (images, videos, audio, documents) into designated folders for offline access.
- Export parsed data into a structured CSV file for further processing and integration with other tools.

# Usage:
from telegram_sleuth import Sleuth

Authenticate with your Telegram API credentials

sleuth = Sleuth(
    api_id='YOUR_API_ID',
    api_hash='YOUR_API_HASH',
    group_username='TARGET_GROUP_USERNAME',
    start_date='2023-11-20',  # Optional: Specify a start date for data extraction
    end_date='2023-11-21',  # Optional: Specify an end date for data extraction
    download_path='/path/to/download/folder',  # Optional: Set a custom download path
    print_to_console=True  # Optional: Print messages to the console as they are extracted
)

# Extract messages and media
data = sleuth.dig()

# Export extracted data to a CSV file
sleuth.export_to_csv('group_chat_data.csv')

# Dependencies:
- telethon
- beauty-print
- python-dateutil
