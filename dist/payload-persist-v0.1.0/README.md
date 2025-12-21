# Secret Server

A portable, secure, file-based secrets manager designed for personal hotspot environments.

## Architecture
See [ARCHITECTURE.md](ARCHITECTURE.md) for deep technical details.

## Mobile Server Setup (Termux)

This project is optimized to run on Android using Termux. Follow these steps to turn your phone into the server.

### 1. Initial Setup
1.  Install **Termux** from F-Droid (preferred) or Google Play.
2.  Open Termux and copy your project files to the phone (e.g., using a USB cable or `git clone`).
3.  Run the automated setup script:
    ```bash
    chmod +x setup_termux.sh
    ./setup_termux.sh
    ```
    *(Note: The script updates your packages. If asked about "package maintainer's version" or encryption configuration, answer `Y` or choose the default "maintainer's version".)*

### 2. Running the Server (Manual)
To start the server manually:
```bash
./start_server.sh
```
The server will be available at `http://0.0.0.0:5001`.

### 3. Auto-Start on Boot (Optional)
To make the server start automatically when you turn on your phone:

1.  Install the **Termux:Boot** app from F-Droid.
2.  Open the **Termux:Boot** app once to grant permissions.
3.  In Termux, create the boot directory:
    ```bash
    mkdir -p ~/.termux/boot
    ```
4.  Copy our boot script there:
    ```bash
    cp termux_boot.sh ~/.termux/boot/
    chmod +x ~/.termux/boot/termux_boot.sh
    ```
5.  **Restart your phone.** The server will start in the background!

### 4. Building the Android App (Standalone APK)

To build a standalone `.apk` that looks like a real app:

1.  **Install Buildozer**:
    ```bash
    pip install buildozer
    sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    ```

2.  **Build the APK**:
    ```bash
    buildozer android debug
    ```

3.  **Install on Phone**:
    The resulting file will be in `bin/`. Transfer it to your phone and install it.
