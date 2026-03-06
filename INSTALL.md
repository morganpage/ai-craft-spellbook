# Installation Guide

This guide covers installing the dependencies required for the AI Craft Spellbook framework.

## Quick Overview

The AI Craft Spellbook framework requires:

- **Python 3.8+** with pip for spell dependencies
- **Node.js** (optional) for Claude Code CLI
- **FFmpeg** for audio/video processing

Choose your operating system below for detailed installation instructions.

## Table of Contents

- [macOS](#macos)
- [Linux](#linux)
- [Windows](#windows)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## macOS

### Python 3.8+ and pip

**Option 1: Using Homebrew (Recommended)**

```bash
# Install Python 3 (includes pip)
brew install python@3.11

# Verify installation
python3 --version
pip3 --version
```

**Option 2: Using Official Installer**

1. Download the installer from [python.org](https://www.python.org/downloads/macos/)
2. Run the installer and follow the prompts
3. Verify installation (see [Verification](#verification))

### Node.js and npm

```bash
# Using Homebrew
brew install node

# Verify installation
node --version
npm --version
```

### FFmpeg

```bash
# Using Homebrew
brew install ffmpeg

# Verify installation
ffmpeg -version
```

---

## Linux

### Python 3.8+ and pip

**Ubuntu/Debian:**

```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

**Fedora/RHEL/CentOS:**

```bash
# Install Python 3 and pip
sudo dnf install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

**Arch Linux:**

```bash
# Install Python 3 and pip
sudo pacman -S python python-pip

# Verify installation
python --version
pip --version
```

### Node.js and npm

**Ubuntu/Debian:**

```bash
# Using NodeSource repository (recommended for latest version)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

**Fedora/RHEL/CentOS:**

```bash
# Using NodeSource repository
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo dnf install -y nodejs

# Verify installation
node --version
npm --version
```

**Arch Linux:**

```bash
# Install Node.js
sudo pacman -S nodejs npm

# Verify installation
node --version
npm --version
```

### FFmpeg

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

**Fedora/RHEL/CentOS:**

```bash
sudo dnf install ffmpeg

# Verify installation
ffmpeg -version
```

**Arch Linux:**

```bash
sudo pacman -S ffmpeg

# Verify installation
ffmpeg -version
```

---

## Windows

### Python 3.8+ and pip

1. Download the installer from [python.org](https://www.python.org/downloads/windows/)
2. During installation:
   - **Important:** Check "Add Python to PATH"
   - Choose "Install for all users" (optional but recommended)
3. Complete the installation
4. Verify installation (see [Verification](#verification))

### Node.js and npm

1. Download the installer from [nodejs.org](https://nodejs.org/)
2. Run the installer and follow the prompts
3. Restart your terminal/command prompt
4. Verify installation (see [Verification](#verification))

### FFmpeg

**Option 1: Using Chocolatey (Recommended)**

```powershell
# Install Chocolatey (if not already installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg

# Verify installation
ffmpeg -version
```

**Option 2: Manual Installation**

1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
2. Extract the downloaded archive
3. Add the `bin` folder to your system PATH:
   - Press `Win + R`, type `sysdm.cpl`, and press Enter
   - Go to the "Advanced" tab and click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add the path to the FFmpeg `bin` folder (e.g., `C:\ffmpeg\bin`)
4. Restart your terminal
5. Verify installation (see [Verification](#verification))

---

## Verification

After installing dependencies, verify everything is working:

```bash
# Check Python version (must be 3.8+)
python --version
# or
python3 --version

# Check pip is installed
pip --version
# or
pip3 --version

# Check Node.js (optional)
node --version

# Check npm (optional)
npm --version

# Check FFmpeg
ffmpeg -version
```

### Expected Versions

| Tool | Minimum Version |
|------|----------------|
| Python | 3.8+ |
| pip | 20.0+ |
| Node.js | 16+ (optional) |
| npm | 8+ (optional) |
| FFmpeg | 4.0+ |

---

## Troubleshooting

### Python

**"python: command not found"**

- Try `python3` instead of `python`
- On macOS/Linux: Create an alias by adding `alias python=python3` to your shell configuration
- On Windows: Make sure Python was added to PATH during installation

**"pip: command not found"**

- Try `pip3` instead of `pip`
- On macOS: `python3 -m pip install --upgrade pip`
- On Linux: `sudo apt install python3-pip` (Ubuntu/Debian)
- On Windows: Reinstall Python and ensure "pip" is selected

**"ModuleNotFoundError: No module named 'pip'"**

- Python installation didn't include pip. Reinstall Python or:
  ```bash
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python3 get-pip.py
  ```

### Node.js/npm

**"node: command not found"**

- Verify Node.js is installed and in your PATH
- Restart your terminal after installation
- On Windows: Restart Command Prompt or PowerShell

**"npm: command not found"**

- npm should be installed with Node.js
- Try reinstalling Node.js from nodejs.org

### FFmpeg

**"ffmpeg: command not found"**

- Verify FFmpeg is installed and in your PATH
- On macOS/Linux: Restart your terminal after installation
- On Windows: Add FFmpeg `bin` folder to PATH and restart terminal
- On Windows with Chocolatey: Restart Command Prompt/PowerShell

**"FFmpeg version too old"**

- Update using your package manager:
  - macOS: `brew upgrade ffmpeg`
  - Ubuntu: `sudo apt update && sudo apt upgrade ffmpeg`
  - Windows: Download latest build from ffmpeg.org

### Virtual Environment Issues

**"venv module not found"**

- On Linux Ubuntu/Debian: `sudo apt install python3-venv`
- On Linux Fedora: `sudo dnf install python3-virtualenv`
- On macOS: Reinstall Python with Homebrew

**Permission errors when creating venv**

- Don't use `sudo` with virtual environments
- Ensure you have write permissions in the current directory
- Try creating in a different location: `python -m venv ~/.venvs/spellbook`

### Claude Code Installation

**Installing Claude Code CLI:**

```bash
# Using npm (requires Node.js)
npm install -g @anthropic-ai/claude-code

# Using pip (requires Python)
pip install claude-code
```

**"EACCES: permission denied" when installing globally**

- Don't use `sudo` with npm. Instead:
  ```bash
  # Create a directory for global packages
  mkdir ~/.npm-global
  npm config set prefix '~/.npm-global'
  echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
  source ~/.bashrc
  ```

---

## Next Steps

After installing dependencies:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/morganpage/ai-craft-spellbook.git
   cd ai-craft-spellbook
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run tests to verify:**
   ```bash
   pytest -v
   ```

For more information, see the main [README.md](README.md).
