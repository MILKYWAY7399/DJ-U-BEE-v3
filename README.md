# 🐝 DJ U BEE v3

> A modern Discord music bot built with **discord.py**, **Wavelink**, and **Lavalink**.

DJ U BEE v3 is a complete rewrite of my original Discord music bot, focused on clean architecture, modular design, and an intuitive user experience.

---

## ✨ Features

### 🎵 Music Playback
- YouTube playback
- Spotify track support
- Spotify album support
- Spotify playlist import
- Instant autocomplete search
- `/play`
- `/playnext`
- Automatic queue management
- Radio Mode (automatic recommendations)

### 🎛️ Interactive Player
- Previous
- Pause / Resume
- Skip
- Stop
- Shuffle
- Seek controls (±5s / ±10s / ±30s)
- Loop (Off / Track / Queue)
- Live progress bar
- Persistent player controls

### 📋 Queue Management
- Interactive queue viewer
- Pagination
- Queue duration
- Album artwork
- Search selection menu
- Queue button integration

### 🎧 Spotify Integration
- OAuth authentication
- Track lookup
- Album lookup
- Playlist import
- Automatic YouTube matching

### 🎼 Last.fm Integration
- OAuth login/logout
- User profile lookup
- Now Playing updates
- Automatic scrobbling

### 🎤 Lyrics
- Lyrics for the current song
- Multi-page lyric embeds

### 📊 Listening Statistics
- Per-user listening statistics
- Songs played
- Listening time
- Top artists
- Top songs
- Server-wide tracking

---

## 🚧 Planned Features

- Server leaderboards
- Server statistics
- Monthly listening history
- Listening streaks
- Playlist sharing
- Save queue as playlist
- Queue management (`/remove`, `/move`, `/jump`)
- Dashboard

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

## ⚙️ Requirements

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

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file.

```env
DISCORD_TOKEN=

SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

LASTFM_API_KEY=
LASTFM_SHARED_SECRET=

LAVALINK_HOST=localhost
LAVALINK_PORT=2333
LAVALINK_PASSWORD=youshallnotpass
```

### Start Lavalink

Place inside the `lavalink/` directory:

- `Lavalink.jar`
- `plugins/`

Start Lavalink before launching the bot.

### Run the bot

```bash
python bot.py
```

---

## 🛠️ Built With

- Python
- discord.py
- Wavelink
- Lavalink
- Spotify Web API
- Last.fm API

---

## 📜 License

Licensed under the MIT License.

---

## 👨‍💻 Author

**MILKYWAY7399**

DJ U BEE v3 is a personal project built to explore software architecture, asynchronous programming, API integrations, and modern Discord bot development.
