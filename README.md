# 🐝 DJ-U-BEE-v3

A modern Discord music bot built with **discord.py**, **Wavelink**, and **Lavalink**.

DJ-U-BEE-v3 is a complete rewrite of my original Discord music bot, focusing on clean architecture, modular design, and a polished user experience.

---

## ✨ Features

### 🎵 Music Playback
- Play songs from YouTube
- Instant autocomplete search
- Spotify track support
- Spotify album support
- Import Spotify playlists from pasted track links
- `/playnext` support
- Automatic queue management

### 🎛 Player Controls
- Previous
- Pause / Resume
- Skip
- Shuffle
- Stop
- Loop modes (Off / Track / Queue)
- Persistent player controls

### 📋 Queue Management
- Interactive queue viewer
- Paginated queue navigation
- Queue button integrated into the player
- Remaining queue duration
- Album artwork previews
- Automatic queue progression
- Search result selection menu

### 🎧 Spotify Integration
- Spotify OAuth
- Track metadata lookup
- Album metadata lookup
- Automatic YouTube matching for playback

### 🎼 Last.fm Integration
- OAuth login
- Logout
- User profile lookup
- Now Playing updates
- Automatic scrobbling

### 🎤 Lyrics
- Fetch lyrics for the currently playing song
- Multi-page lyric embeds for long songs

---

## 🚧 Planned Features

- Custom user playlists
- Playlist sharing
- Save current queue as playlist
- Listening statistics
- User profiles
- Top artists
- Top tracks
- Guild listening statistics
- Queue management commands (`/remove`, `/move`, `/jump`)

---

## 📂 Project Structure

```text
DJ-U-BEE-v3/
│
├── bot.py
├── config.py
│
├── cogs/
├── models/
├── music/
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
- Last.fm API Application

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/MILKYWAY7399/DJ-U-BEE-v3.git
cd DJ-U-BEE-v3
```

### Create a virtual environment

```bash
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

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

LASTFM_API_KEY=your_lastfm_api_key
LASTFM_SHARED_SECRET=your_lastfm_shared_secret

LAVALINK_HOST=localhost
LAVALINK_PORT=2333
LAVALINK_PASSWORD=youshallnotpass
```

### Start Lavalink

Place the following inside the `lavalink/` folder:

- `Lavalink.jar`
- `plugins/`

Start the Lavalink server.

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
- Last.fm API

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**MILKYWAY7399**

Built as a personal project to learn software architecture, asynchronous programming, API integration, and Discord bot development.
