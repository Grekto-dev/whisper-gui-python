# **Whisper-GUI-Python**

A user-friendly Graphical User Interface (GUI) wrapper for OpenAI's 
Whisper speech recognition model.

Built with **Python** and **Tkinter**, Whisper-GUI-Python bridges the gap
between the command line and the user, offering features like **batch
processing**, **real-time hardware monitoring**, and **comprehensive
parameter configuration** without touching a terminal.

------------------------------------------------------------------------

## 📦 Architecture & Design

Unlike standalone applications that bundle a specific version of the 
Whisper engine into a large executable, Whisper-GUI-Python is designed 
as a lightweight wrapper (launcher) for the official OpenAI Whisper 
CLI installed on your system.

-   **Why this approach?** It ensures you are always using the official
 source code. You can update the Whisper engine independently at any
time (via pip install -U openai-whisper) to access new models and
performance improvements immediately, without waiting for a GUI update.

> **Note:** This means a one-time setup of Python and FFmpeg is 
required, but it offers greater flexibility and keeps the application size 
minimal.
------------------------------------------------------------------------

## ✨ **Features**

-   **Batch Processing:** Drag and drop multiple audio/video files and
    transcribe them sequentially.
-   **Real-Time Monitoring:** View CPU, RAM, GPU, and VRAM usage live
    while transcoding.
-   **Output Management:** Automatically saves transcripts to the source
    directory or a custom folder.
-   **Profile System:** Save and load your favorite configurations
    (language, model size, advanced parameters).
-   **Advanced Control:** Full access to Whisper's advanced CLI
    parameters (`temperature`, `beam_size`, etc.) via tooltips and
    dropdowns.
-   **Multi-Language Interface:** Native support for **English (US)**
    and **Portuguese (Brazil)**.
-   **Auto-Dependency Check:** Automatically detects and offers to
    install missing Python packages (`torch`, `whisper`, etc.) on
    startup.
-   **Live Logging:** View the transcription progress line-by-line in
    the built-in terminal window.

------------------------------------------------------------------------

## 🚀 **Prerequisites**

Before running the application, ensure you have the following installed:

-   **Python 3.8+** (Ensure you check *"Add Python to PATH"* during
    installation).
-   **FFmpeg:** Whisper requires FFmpeg to process audio files (must be
    added to System PATH).
-   **CUDA (Optional but Recommended):** For GPU acceleration, you need
    an NVIDIA card and the appropriate CUDA Toolkit installed.

------------------------------------------------------------------------

## 📦 **Installation**

### **Clone the repository**

``` bash
git clone https://github.com/Grekto-dev/whisper-gui-python
cd whisper-gui-python
```

### **Install Dependencies**

The application has a built-in dependency checker that will attempt to
install missing packages on the first run.
However, you can manually install them using:

``` bash
pip install -r requirements.txt
```

> **Note:** For GPU support, ensure you have the correct version of
> PyTorch installed for your CUDA version.

------------------------------------------------------------------------

## ▶️ **Usage**

### **Using the Launcher (Recommended)**

Double-click the **`launch_whisper.bat`** file.
This script ensures the working directory is correct and keeps the
console open in case of critical errors.

### **Running via Python**

``` bash
python whisper_gui.py
```

------------------------------------------------------------------------

## 🛠️ **How it Works**

1.  **Select Files:** Drag and drop audio/video files into the queue or
    use the *Select Files* button.
2.  **Configure:** Choose the model size (Tiny to Turbo), language, and
    output format.
3.  **Advanced (Optional):** Tweak sampling temperature, beam size, and
    other decoding parameters in the *Advanced* tab.
4.  **Run:** Click **START TRANSCRIPTION**.
5.  **Monitor:** Watch the progress in the *Terminal Log* and check your
    system resources in the top-right monitor.

------------------------------------------------------------------------

## 🌍 **Internationalization**

The app automatically defaults to **English (US)**.
You can change to other languages in the top-right corner
(currently only **Brazilian Portuguese** is supported).
The app will ask to restart to apply the language changes.

------------------------------------------------------------------------

## 👏 **Acknowledgments**

-   **OpenAI:** For the incredible Whisper model.
-   **TkinterDnD2:** For the drag-and-drop functionality.
