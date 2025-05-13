# 🤖 Linux Personal Assistant (Statix)

> **"Statix – Simplify your Linux experience with real-time insights 🚀"**

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Tkinter GUI](https://img.shields.io/badge/GUI-Tkinter-yellowgreen.svg)](https://wiki.python.org/moin/TkInter)
[![psutil](https://img.shields.io/badge/psutil-5.9.0-green.svg)](https://pypi.org/project/psutil/)
[![matplotlib](https://img.shields.io/badge/matplotlib-3.5.1-red.svg)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 🚀 Project Overview

**Linux Assistant (Statix)** is a comprehensive desktop utility for Linux power users. It integrates **real-time system monitoring**, **embedded terminal**, **file operations**, **calendar scheduling**, and **system controls** into a unified, themeable dashboard.

Key capabilities:

* 🔍 Real-time CPU, RAM, and disk usage with dynamic visualizations
* 📊 Interactive multi-ring donut charts and line plots for historical trends
* 🖥️ Embedded terminal for running commands and viewing outputs
* 📁 File and directory management (create, delete, navigate, upload)
* 🎨 Four professional themes: Dark, Light, Hacker, Glass
* 📅 Built-in calendar view for month and date lookup
* ⚙️ Quick-access system commands (reboot, service checks)
* 🌐 Raw network interface overview via embedded command output

---

## ✨ Key Features

### ⚙️ Resource Monitoring

* **Multi-Ring Donut Chart**: Concentric rings for CPU, RAM, Disk percentages
* **Dual Line Charts**: Rolling history for CPU and RAM over the last 60 samples
* **Legend Labels**: Real-time numeric readouts updated every second

### 🧾 Command Center

* Integrated terminal panel
* Execute common Linux commands (top, free, df, ip)
* Threaded execution to keep UI responsive

### 🗂 File Management

* Create and delete files/directories with confirmation dialogs
* Upload external files via file chooser
* Basic file system navigation commands wrapped in GUI buttons

### 🎨 Themes

* **Dark**: Low-light friendly
* **Light**: High-contrast clarity
* **Hacker**: Green-on-black retro style
* **Glass**: Modern translucent palette
* Theme persists across sessions (future enhancement)

### 📅 Calendar

* Popup month view for the current year/month
* Read-only calendar rendered in a scrollable text widget

### 🔄 System Controls

* Safe system reboot with confirmation
* Placeholder for future service status controls

### 🌐 Network Info

* Raw output of `ip -brief addr` in terminal panel

---

## 🛠️ Technology Stack

| Component          | Technology         | Purpose                        |
| ------------------ | ------------------ | ------------------------------ |
| Core Engine        | Python 3.9+        | Application logic              |
| GUI Framework      | Tkinter (ttk)      | Cross-platform widgets         |
| Charts & Plots     | Matplotlib         | Donut and line chart rendering |
| System Metrics     | psutil             | CPU, RAM, disk usage           |
| Data Handling      | NumPy              | Historical buffer management   |
| Subprocess Control | subprocess, os     | Command execution              |
| Calendar Rendering | calendar, datetime | Month view generation          |

---

## ⚙️ Installation

### Prerequisites

* Python 3.9 or higher
* Linux OS with GUI support
* `pip` and `git` installed

### Setup

```bash
# Clone the repository
git clone https://github.com/Ashish-equinox/LinuxPersonalAssistant.git
cd LinuxPersonalAssistant

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make script executable
chmod +x linux_assistant.py
```

---

## 🎬 Usage

Launch the assistant:

```bash
./linux_assistant.py
```

Command-line options:

```bash
./linux_assistant.py --theme=Light    # Start with Light theme
./linux_assistant.py --no-history    # Disable trend history buffer
./linux_assistant.py --debug         # Print debug logs
./linux_assistant.py --help          # Show help message
```

---

---

## 📸 UI Screenshots

> ![Theme 1](images/hacker-theme.png)
> Hacker Theme

> ![Theme 2](images/light-theme.png)
> Light Theme

> ![Theme 3](images/dark-theme.png)
> Dark Theme

> ![Create File Dialog](images/create-file.png)
> Dialog for "Create File" operation

> ![Reboot Confirmation Dialog](images/reboot.png)
> Confirmation dialog for system reboot

---

## 📂 Project Structure

```
LinuxPersonalAssistant/
├── linux_assistant.py       # Main application
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── resources/               # (Future) icons and theme files
```

---

## 📃 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements 🎉

Thank you to the open-source Linux community and the tools that inspired this project.

---

**Developed by Ashish 🚀✨**
