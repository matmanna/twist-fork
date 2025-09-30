# The Twist

🌀 The Bender Twist is a [free](https://en.wikipedia.org/wiki/Free_software), portable platform that augments the functional capabilities of LT-series amps made by a certain guitar brand that rhymes with "bender" and names products after horses.

> [!IMPORTANT]
> This platform is still a prototype with many of its components being WIP. **Nevertheless, leaving a star helps the project a lot and keeps you in the loop with progress! ⭐**

## 📌 This Repository

This repository contains the key functionality behind the twist, which is designed to be combined with other add-ons that may be developed in the future (think rechargeable battery support, etc.)

The two main parts within this codebase are the **backend server**--, controlling access point, API, and Amp connectivity functionalities-- and the **frontend control panel**, which provides a user-friendly and easily accessible interface for using and interacting with your Twist device. An overview of both of these parts can be found in the respository's [Wiki Documentation](/wiki).

**Platform Features**
- 🌀 Bender Twist LT 0
  - 📡 Wireless access point connectivity
  - 🌐 Web-based control panel & API
    - 📊 Data stored per-twist
  - 📱 Mobile control panel app (soon!)
    - 📊 Data stored per-app
  - 🛰️ Router-baee Wi-Fi support
    - 📻 Multiple-twist support (router)
  - 🖲️ Footswitch playlists

- Bender Twist LT pico (soon!)
 
## 🖼️ Setup Overview 

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/58ce5217-b79b-4d99-894d-8866c4a96b48">
  <source media="(prefers-color-scheme: light)" srcset="[light-mode-image.png](https://github.com/user-attachments/assets/c4c7d9b0-8648-43ab-8645-886d6eda53cf)">
  <img alt="Fallback image description" src="[default-image.png](https://github.com/user-attachments/assets/c4c7d9b0-8648-43ab-8645-886d6eda53cf)">
</picture>


## 🚀 Getting Started

> [!NOTE]
> Everything in this repository is designed and tested to be run on a Raspberry Pi Zero 2W. This doesn't mean it won't work on other (primarily Linux) platforms or devices, just that we don't currently support them.

1. Install The Twist on your Pi
   a. Flash the Official Image (Recommended)
   Go to the latest [release](/releases), download the "twist-pi-official-image-v{semver}.img.xz" file, and follow the [flashing guide](/FLASHING.md) to get it on your pi!
   b. Alternatively: SSH into Pi and DIY install
   ```bash
   git clone https://github.com/bendertools/twist-pi.git
   cd twist-pi
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```
2. Connect to the WiFi network "the-twist" and you're set!

## 💻 Developing

To start the backend manually, run:

```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 80 --reload
```

To build new changes to the Svelte frontend, run. Unfortunately, due to no amp simulator being built for LtAmp.py (that maintainer should really get on that!!), you may have to build every time you make changes. Sorry :(

```bash
cd frontend
npm run build
```

## 🗺️ Roadmap

Planned features, known bugs, and the overall project roadmap are coorinated using a combination of GitHub's Issues and Projects. The project [tab](https://github.com/bendertools/projects) is where more broad, long-term, and important work is tracked, while day-to-day development progress is reserved for Issues and Pull Requests.
