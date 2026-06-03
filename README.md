# 🌐 NetSpeed Monitor Pro & SpeedTester

An advanced, lightweight Windows desktop widget built with Python and Tkinter. It offers real-time network traffic monitoring seamlessly floating on your desktop, combined with a highly responsive, custom-animated speedometer for active maximum speed testing.

---

## ⚡ Features

- **Live Traffic Monitor:** Floating, transparent widget tracking download and upload speeds every second without blocking any screen content.
- **Dynamic Speedometer (Speed Test):** A beautiful, math-rendered gradient arc speedometer that changes color synchronously based on active test phases (Download/Upload).
- **Smooth Needle Physics:** Real-time feedback and smooth needle interpolation animations instead of abrupt jumps.
- **Smart System Integration:**
  - Hidden position caching (saves window coordinates inside Windows `AppData`).
  - Native Windows Registry integration for an optional Auto-Run toggle.
  - Ghost console redirect prevents app crashing under `.pyw` execution windowless environments.
- **Copyable Contact Info:** Built-in "About" section featuring read-only selectable text for easy developer contact.

---

## 📸 Preview
*(Add your beautiful screenshots or a short GIF here to show the widget in action)*
- `![Live Monitor Widget](preview_monitor.png)`
- `![Active Speedometer](preview_speedtest.png)`

---

## 🛠️ Prerequisites & Installation

The application automatically checks for dependencies, but you can install the required external libraries manually using:

```bash
pip install psutil speedtest-cli