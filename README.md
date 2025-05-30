# telegram-Autoresponder-Compliment-Bot
A script for automating Telegram messaging using Telethon. Supports multiple modes: auto-reply, timed reply, one-time reply, and compliment sending when someone comes online.

⚙️ Features
autoreply — replies to incoming messages if you haven't messaged the user first.
autoreply_once — replies only once to each user.
autoreply_timed — replies at a fixed interval (e.g., every 24 hours).
ompliment — sends compliments when a user comes online or was recently online.

🛠 Installation

    pip install telethon

🚀 Getting Started

Set your Telegram API credentials at the top of the script:

    api_id_x =  your_api_id_here
    api_hash_x = 'your_api_hash_here'
 
 Choose the desired mode:

    MODE = 'autoreply'  # Options: 'autoreply', 'autoreply_once', 'autoreply_timed', 'compliment'

Run the script:
                           
    python3 sender.py

During the first run, you'll be prompted to enter your phone number and a verification code. If two-factor authentication is enabled, you’ll also need your password.
🧠 How It Works
autoreply — replies if the last message was from the user.
autoreply_once — sends one reply per user, no repeats.
autoreply_timed — replies only after a specified interval has passed.
compliment — watches for selected users to come online and sends a random compliment.

🔧 Configuration

Reply timeout for autoreply_timed mode:

    REPLY_TIMEOUT = 60 * 60 * 24  # 24 hours

Customize reply and compliment texts:

    autoreply_templates = [...]
    compliments_list = [...]

Set target users for compliment mode:

    targets = [
          {'type': 'username', 'value': '@username1'},
          {'type': 'id', 'value': 123456789},
       ]

❗ Notes
Only works in private chats (not groups or channels).
For compliment mode, users must allow you to see their online status.
You can use either username or user ID to target users.
