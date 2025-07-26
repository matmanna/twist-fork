# The Twist

> [!IMPORTANT]
> This repository is still definitely in the prototype stage with many of The Twist's components, resources, and documentation are still being WIPs. **Nevertheless, leaving a star on this repo helps with my motivation, allows you to indicate  interest, and keeps you in the loop with progress as it is made!**

🌀 The Bender Twist is a [free](https://en.wikipedia.org/wiki/Free_software), portable platform that augments the functional capabilities of the LT-series amplifiers made by a certain guitar gear brand that rhymes with "bender" and names products after horses.

# 📌 This Repository

This repository contains the key functionality behind the twist, which is designed to be combined with other add-ons that may be developed in the future (think rechargeable battery support, etc.)

The two main parts within this codebase are the **backend server**--, controlling access point, API, and Amp connectivity functionalities-- and the **frontend control panel**, which provides a user-friendly and easily accessible interface for using and interacting with your Twist device. An overview of both of these parts can be found below in the respository's [Wiki Documentation](/wiki):

## 🚀 Getting Started

> [!NOTE]
> Everything in this repository is designed and tested to be run on a Raspberry Pi Zero 2W. This doesn't mean it won't work on other (primarily Linux) platforms or devices, just that we don't currently support them.

### ⚙️ Backend

- **FastAPI:** The most fundamental technology powering the Pi backend is FastAPI. Through FastAPI, both REST API and websocket (important due to real-time nature of the hardware's adjustments) connections are managed and handled.
- **SQLite:**
- **[lt25.py](https://pypi.org/project/lt25/):** My own python interface for the LT25 amp

### 🖼️ Frontend

- **Svelte:** Valuing simplicity, the frontend control panel uses Svelte and Vite to serve static files which will be
- **Vite:**
- **Skeleton.dev Design:**

## 🚀 Quickstart

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

To start the API manually, run:

```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 80
```

To build the Svelte frontend, run:

```bash
cd frontend
npm run build
```

## 🗺️ Roadmap

Planned features, known bugs, and the overall project roadmap are coorinated using a combination of GitHub's Issues and Projects. The project [tab](/projects) is where more broad, long-term, and important work is tracked, while day-to-day development progress is reserved for Issues and Pull Requests.

- [ ] Control all amp features from device tab (like on actual amp)
- [ ] device control
  - [ ] Turn twist on/off
  - [ ] Reboot twist
  - [ ] Change twist AP/wifi configuration- [ ] Expose API and control API setting
- [ ] Support rPi pico
- [ ] Multiple simultaneous devices
  - [ ] multiple pis attached to one twist
