# 🇺🇸 Visa Appointment Watcher

📖 Read this in other languages: [简体中文 🇨🇳](./README.zh-CN.md)

---

📅 **Automatically monitor available U.S. visa appointment dates and notify you via email!**  
💡 Powered by Selenium + undetected_chromedriver for stealthy automation  
✉️ Email alerts for added or removed dates

---

## Update  
[2025.7.15] Updated `main_v2.py` (Potentially more stable than `v1`)

- **Login Completion Flag**:  
  To indicate that login is complete, **create a `login.flag` file** instead of pressing Enter.  
  This is necessary because pressing Enter is not possible when the process runs in the background.

- **Important**: You must update the value for your target city.  
  Refer to the image below to find the correct value, then update the following lines in `main_v2.py`:
  - https://github.com/SYuan03/VisaAppointmentWatcher/blob/47f2c28e043dd952ae8c6814ae7d2f0651eb5d18/main_v2.py#L17-L20
  - https://github.com/SYuan03/VisaAppointmentWatcher/blob/47f2c28e043dd952ae8c6814ae7d2f0651eb5d18/main_v2.py#L136

  <img width="1995" height="1299" alt="image" src="https://github.com/user-attachments/assets/3c7c7c23-79ad-47b6-bc7c-95b9bc60d3e1" />



## 🚀 Final Product
<img src="assert/final.jpg" alt="Final Product" width="300"/>

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
python main.py
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
