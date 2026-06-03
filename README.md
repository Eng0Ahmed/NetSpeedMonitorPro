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
Running the application:
Download NetSpeed.pyw or the provided .zip release.

Double-click to run. It runs silently and efficiently in the background.

Right-click the floating widget to access the menu (Speed Test, Auto-Run, About, Exit).

📜 License & Copyright
Developer: Eng Ahmed Abdelaziz

Version: 1.0.0

Copyright (c) 2026 Eng Ahmed Abdelaziz. All rights reserved.

Licensed under the MIT License. You are free to copy, modify, and redistribute this software as long as the original copyright notice and credit to the author remain intact.

🌍 نظرة عامة (Arabic Description)
برنامج احترافي لمراقبة وقياس سرعة الإنترنت بشكل حي ومستمر من سطح المكتب.

أهم المميزات:

مراقبة حية: واجهة عائمة شفافة تعرض سرعة الرفع والتحميل اللحظية دون إعاقة الاستخدام.

عداد سرعة تفاعلي: أداة قياس للسرعة القصوى (Speed Test) مبنية هندسياً لتعكس السرعة بمؤشر ميكانيكي يتحرك بنعومة فائقة ويتغير لونه حسب نوع القياس.

تكامل مع النظام: إمكانية التشغيل التلقائي مع الويندوز، وحفظ آخر مكان للنافذة على الشاشة تلقائياً.

خفيف ومستقل: يعمل في الخلفية بصمت تام دون استهلاك موارد الجهاز.
