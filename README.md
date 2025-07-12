# 🇺🇸 Visa Appointment Watcher

📖 Read this in other languages: [简体中文 🇨🇳](./README.zh-CN.md)

---

📅 **Automatically monitor available U.S. visa appointment dates and notify you via email!**  
💡 Powered by Selenium + undetected_chromedriver for stealthy automation  
✉️ Email alerts for added or removed dates

---

## 🚀 Final Product
![Final Product](assert/final.jpg)

## 🔥 Features

- ✅ Monitors [usvisascheduling.com](https://www.usvisascheduling.com) in real-time
- 📌 Automatically selects a target city (default: **WUHAN**)
- ⏱ Checks every 7 minutes
- ✉️ Sends email alerts for appointment changes
- 🧩 Uses `undetected_chromedriver` to reduce bot detection
- 🧪 Manual login supported for CAPTCHA handling

---

## 🚀 How to Run

### 1. Clone the repo

```bash
git clone https://github.com/yourname/visa-appointment-watcher.git
cd visa-appointment-watcher
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure email

Edit the `sendmail()` function:

```python
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465  # Use 465 for SSL
EMAIL_SENDER = "xxx@qq.com"
EMAIL_PASSWORD = "xxx"
EMAIL_RECEIVER = "xxx@qq.com"
```

> Make sure SMTP is enabled and use an **app password** from QQ Mail.
> You can use other mail services, but you may need to adjust the SMTP settings.

### 4. Run the script

```bash
python visa_monitor.py
```

Follow the prompt to manually log in, complete any CAPTCHA, then press Enter.

> You can also run it in the background using `nohup` or a task scheduler like `tmux`.

---

## 📬 Email Example

```
Subject: Visa Appointment Update

Newly available dates:
  + 2025-07-14
  + 2025-07-20

Dates no longer available:
  - 2025-07-11

All currently available:
  * 2025-07-14
  * 2025-07-20
```

---

## ⚠️ Disclaimer

- For educational use only — not for commercial purposes
- Manual login may be required after browser refresh
- Stable internet connection recommended

---

## 📄 License

[MIT License](./LICENSE)
