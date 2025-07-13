# The (Bender) Twist

> [!IMPORTANT]
> This repository is currently a WIP. Many of The Twist's components, resources, and documentation are still being created. **Nevertheless, leaving a star on this repo allows you to indicate your interest and follow progress!**

🌀 The Bender Twist is a [free](https://en.wikipedia.org/wiki/Free_software) platform that augments the LT25 amplifier's capabilities. This repository is a meta-repo, meaning that it primarily focuses on providing documentation for a project whose contents are spread across several sub-repos.


## 🔖 This Respository

Inside this repository are the two main pieces that make The Twist's computing happen -- the **backend**, controlling the Access Point, API, and Amp connectivity, in addition to the **frontend**, which provides a user-accessible and friendly interface for using The Twist's key features. An overview of both of these parts can be found below:

> [!IMPORTANT]
> Everything in this repository is designed and tested to be run on a Raspberry Pi Zero W. This doesn't mean it won't work on other (primarily Linux) platforms or devices, just that we don't currently support them.

### ⚙️ Backend

- **FastAPI:** The most fundamental technology powering the Pi backend is FastAPI. Through FastAPI, both REST API and websocket (important due to real-time nature of the hardware's adjustments) connections are managed and handled.
- **SQLite:**

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
    chmod +x setup.sh
    ./setup.sh
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
