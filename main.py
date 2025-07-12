from datetime import date
from email.utils import formataddr
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = uc.ChromeOptions()
options.add_argument("--no-first-run --no-service-autorun --password-store=basic")

driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 20)

current_dates = set()

# sendmail
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendmail(added_dates, removed_dates, all_dates):
    if not added_dates and not removed_dates:
        return  # No change, no need to send

    # Email configuration
    SMTP_SERVER = "smtp.qq.com"
    SMTP_PORT = 465  # Use 465 for SSL
    EMAIL_SENDER = "xxx@qq.com"
    EMAIL_PASSWORD = "xxx"
    EMAIL_RECEIVER = "xxx@qq.com"

    # Construct email content
    subject = "Visa Appointment Update"
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
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], msg.as_string())
        server.quit()
        print("Email sent via QQ successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


try:
    driver.get("https://www.usvisascheduling.com/zh-CN/schedule/")
    print("Page opened. Please log in manually (complete any verification if needed)...")
    input("Press Enter after login is complete...")

    while True:
        try:
            # Refresh the page
            driver.refresh()
            print("Page refreshed.")
            time.sleep(6)

            # Save HTML for debugging
            with open("page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#post_select option[value="7b6af614-b0db-ec11-a7b4-001dd80234f6"]')
            ))
            select = Select(driver.find_element(By.ID, "post_select"))
            select.select_by_value("7b6af614-b0db-ec11-a7b4-001dd80234f6")
            print("Location selected: WUHAN")
            time.sleep(6)

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
                sendmail(added_dates, removed_dates, available_dates)

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
            print(f"Error in this cycle: {e}")

        print("Waiting 7 minutes before next check...")
        for i in range(7):
            print(f" - Waiting... {7 - i} minutes remaining")
            time.sleep(60)

finally:
    driver.quit()
