# 🐝 DJ-U-BEE-v3

A modern Discord music bot built with **discord.py**, **Wavelink**, and **Lavalink**.

DJ-U-BEE-v3 is a complete rewrite of my original Discord music bot, focusing on a cleaner architecture, modular design, and better maintainability.

---

## ✨ Features

### 🎵 Music Playback
- Play songs from YouTube
- Search before playing
- Spotify track support
- Spotify album support
- Import Spotify playlists from pasted track links
- Automatic queue management

### 🎛 Player Controls
- Pause / Resume
- Skip
- Previous
- Shuffle
- Stop
- Loop modes
- Persistent player controls

### 📋 Queue Management
- View queue
- Automatic queue progression
- Search result selection menu

### 🎧 Spotify Integration
- Spotify OAuth
- Track metadata lookup
- Album metadata lookup
- Automatic YouTube matching for playback

---

## 🚧 Planned Features

- Last.fm OAuth
- Automatic Last.fm scrobbling
- Listening statistics
- User profiles
- Top artists
- Top tracks
- Guild listening stats

---

## 📂 Project Structure

```
DJ-U-BEE-v3/
│
├── bot.py
├── config.py
│
├── cogs/
├── music/
├── models/
├── oauth/
├── providers/
├── ui/
│
├── lavalink/
├── storage/
│
├── requirements.txt
└── README.md
```

---

## ⚙ Requirements

- Python 3.11+
- Java 17+
- Lavalink v4
- Discord Bot Token
- Spotify Developer Application

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DJ-U-BEE-v3.git
cd DJ-U-BEE-v3
```

### Create a virtual environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```env
DISCORD_TOKEN=your_discord_token

SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

LAVALINK_HOST=localhost
LAVALINK_PORT=2333
LAVALINK_PASSWORD=youshallnotpass
```

### Start Lavalink

Place:

- `Lavalink.jar`
- plugins

inside the `lavalink/` folder and start the server.

### Run the bot

```bash
python bot.py
```

---

## 🛠 Built With

- Python
- discord.py
- Wavelink
- Lavalink
- Spotify Web API

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**MILKYWAY7399**

Built as a personal project to learn Discord bot development and software architecture.
