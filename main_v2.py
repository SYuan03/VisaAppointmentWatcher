from datetime import date
from email.utils import formataddr
import os
import sys
import traceback
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

EMAIL_RECEIVERS = [
    "1xx@qq.com", 
    "2xx@qq.com"
]

VISA_TYPE_TO_VALUE = {
    "Guangzhou_B1B2": "xxx",
    "Wuhan_B1B2": "7b6af614-b0db-ec11-a7b4-001dd80234f6",
}

FLAG_FILE = "login.flag"

class Tee:
    def __init__(self, *streams):
        self.streams = streams
    def write(self, data):
        for s in self.streams:
            s.write(data)
            s.flush()
    def flush(self):
        for s in self.streams:
            s.flush()

# logfile = open("log.txt", "a", encoding="utf-8")
logfile = open("log.txt", "w", encoding="utf-8")
sys.stdout = sys.stderr = Tee(sys.__stdout__, logfile)

# options = uc.ChromeOptions()
# options.add_argument("--no-first-run --no-service-autorun --password-store=basic")

# driver = uc.Chrome(options=options)

# can be deleted, not sure whether it works
options = uc.ChromeOptions()
# PROFILE_DIR = "uac_profile"
# options.add_argument(f"--user-data-dir={os.path.abspath(PROFILE_DIR)}")
# options.add_argument("--no-first-run --no-service-autorun --password-store=basic")

driver = uc.Chrome(options=options)

wait = WebDriverWait(driver, 30)

current_dates = set()

# sendmail
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendmail(added_dates, removed_dates, all_dates, visa_type):
    if not added_dates and not removed_dates:
        return  # No change, no need to send

    # Email configuration
    SMTP_SERVER = "smtp.qq.com"
    SMTP_PORT = 465  # Use 465 for SSL
    EMAIL_SENDER = "xxx@qq.com"
    EMAIL_PASSWORD = "xxx"
    

    # Construct email content
    subject = f"Visa Appointment Update [{visa_type}]"
    body_lines = []

    if added_dates:
        body_lines.append("Newly available dates:")
        for d in sorted(added_dates):
            body_lines.append(f"  + {d}")

    if removed_dates:
        body_lines.append("\nDates no longer available:")
        for d in sorted(removed_dates):
            body_lines.append(f"  - {d}")

    body_lines.append("\nAll currently available:")
    for d in sorted(all_dates):
        body_lines.append(f"  * {d}")

    body = "\n".join(body_lines)

    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = formataddr(("Visa Notifier", EMAIL_SENDER))
        msg["To"] = ", ".join(EMAIL_RECEIVERS)
        msg["Subject"] = subject

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())
        server.quit()
        print("Email sent via QQ successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


try:
    driver.get("https://www.usvisascheduling.com/zh-CN/schedule/")
    print("Page opened. Please log in manually (complete any verification if needed)...")
    # input("Press Enter after login is complete...")

    # print("Wait here 60s to complete login...")
    # time.sleep(60)

    print("Waiting for login to complete, please create the file `login.flag` to continue...")
    while not os.path.exists(FLAG_FILE):
        time.sleep(1)
    
    print("Login complete, continue...")
    print(f"pid: {os.getpid()}")

    while True:
        try:
            # Refresh the page
            driver.refresh()
            print("Page refreshed.")
            time.sleep(12)

            # Save HTML for debugging
            with open("page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            wait.until(EC.presence_of_element_located(
                (By.ID, "post_select")
            ))
            visa_type = "Wuhan_B1B2"
            select = Select(driver.find_element(By.ID, "post_select"))
            select.select_by_value(VISA_TYPE_TO_VALUE[visa_type])
            # select = Select(driver.find_element(By.ID, "post_select"))
            # select.select_by_value("7b6af614-b0db-ec11-a7b4-001dd80234f6")
            print(f"Location selected: {visa_type}")
            time.sleep(12)

            # Extract dates
            available_dates = set()
            day_cells = driver.find_elements(By.CSS_SELECTOR, "td.greenday")
            for cell in day_cells:
                try:
                    day = cell.find_element(By.CSS_SELECTOR, "[data-date]").get_attribute("data-date")
                    month = int(cell.get_attribute("data-month")) + 1
                    year = int(cell.get_attribute("data-year"))
                    full_date = date(year, month, int(day)).isoformat()
                    available_dates.add(full_date)
                except Exception as e:
                    print(f"Skipped one cell due to error: {e}")

            # Compute difference *before* updating current_dates
            if available_dates != current_dates:
                added_dates = available_dates - current_dates
                removed_dates = current_dates - available_dates
                # sendmail
                sendmail(added_dates, removed_dates, available_dates, visa_type)

                print("New appointment date changes detected:")

                if added_dates:
                    print(" - Newly available dates:")
                    for d in sorted(added_dates):
                        print(f"   + {d}")

                if removed_dates:
                    print(" - Dates no longer available:")
                    for d in sorted(removed_dates):
                        print(f"   - {d}")

                # Now update current_dates
                current_dates = available_dates
            else:
                print("No new dates found.")
                for d in sorted(current_dates):
                    print(d)

        except Exception as e:
            print("Error in this cycle:")
            traceback.print_exc()

        print("Waiting 5 minutes before next check...")
        for i in range(5):
            print(f" - Waiting... {5 - i} minutes remaining")
            time.sleep(60)

finally:
    driver.quit()
