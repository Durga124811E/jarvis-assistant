# JARVIS - Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Linux (Kali Linux recommended), Windows, or macOS
- **RAM**: 4GB minimum
- **Disk Space**: 2GB for tools and libraries

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Durga124811E/jarvis-assistant.git
cd jarvis-assistant
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install System Dependencies

#### On Kali Linux/Debian:

```bash
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    ffmpeg \
    portaudio19-dev \
    libportaudio2
```

#### On Ubuntu:

```bash
sudo apt-get install -y \
    python3-dev \
    ffmpeg \
    portaudio19-dev
```

#### On Fedora:

```bash
sudo dnf install -y \
    python3-devel \
    ffmpeg \
    portaudio-devel
```

#### On macOS:

```bash
brew install ffmpeg portaudio
```

#### On Windows:

1. Download FFmpeg from: https://ffmpeg.org/download.html
2. Extract and add to PATH
3. Install Visual C++ Build Tools

### 5. Configure Audio (For Voice Features)

#### On Linux:

```bash
# Test microphone
arecord -l

# Install PulseAudio if needed
sudo apt-get install pulseaudio
```

#### On Windows:

1. Ensure microphone is connected and enabled
2. Test in Settings > Sound

### 6. Verify Installation

```bash
python jarvis.py --version
```

## Usage

### Start Jarvis

```bash
python jarvis.py
```

### Voice Command Mode

Simply speak your commands:
- "help" - See all commands
- "search jobs" - Find jobs
- "edit video" - Video editing
- "create video" - AI video generation
- "teach me hacking" - Learn ethical hacking

### Troubleshooting

#### Microphone Not Working

```bash
# Check audio devices
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"

# Set specific microphone in config
# Edit config.py and set MICROPHONE_INDEX
```

#### FFmpeg Not Found

```bash
# Add FFmpeg to PATH
export PATH="/path/to/ffmpeg/bin:$PATH"
```

#### ImportError for modules

```bash
# Reinstall specific package
pip install --upgrade pyaudio
# or
pip install --upgrade opencv-python
```

#### Permission Issues on Linux

```bash
# Add user to audio group
sudo usermod -a -G audio $USER
sudo usermod -a -G video $USER
newgrp audio
```

## Optional: Kali Linux Specific Setup

### Install Hacking Tools

```bash
# Already included in Kali, but update them
sudo apt-get update
sudo apt-get install -y \
    nmap \
    wireshark \
    metasploit-framework \
    burpsuite \
    hashcat
```

### Enable Hacking Module Full Features

The hacking module is automatically available, but to use actual penetration testing:

1. **Set up a lab environment** (VirtualBox, Proxmox, etc.)
2. **Use HackTheBox or TryHackMe** for practice
3. **Follow all legal and ethical guidelines**

## Post-Installation

1. Create `.env` file for API keys (optional)
2. Configure preferences in `config.py`
3. Test each module:

```bash
# Test video module
python -m modules.video_editor

# Test job search
python -m modules.job_search

# Test AI video
python -m modules.ai_video

# Test hacking guide
python -m modules.hacking_guide
```

## Updating Jarvis

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Getting Help

- Check README.md for features
- Review module documentation
- Check troubleshooting section
- Open an issue on GitHub

---

**Happy learning and stay ethical! 🔒**
