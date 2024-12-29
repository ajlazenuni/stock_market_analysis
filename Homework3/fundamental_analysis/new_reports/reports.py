from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
import traceback

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
driver.get('https://www.mse.mk/mk/reports')


output_folder = "downloaded_reports"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def download_report(report_url, report_name):
    try:

        response = requests.get(report_url, stream=True)
        response.raise_for_status()


        temp_path = os.path.join(output_folder, report_name)
        with open(temp_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        print(f"Downloaded: {report_name}")


        try:

            df = pd.read_csv(temp_path, encoding="ISO-8859-1", delimiter=";")  # Adjust delimiter/encoding if needed
            csv_path = os.path.join(output_folder, f"{os.path.splitext(report_name)[0]}.csv")
            df.to_csv(csv_path, index=False, encoding="utf-8")
            print(f"Converted to CSV: {csv_path}")

            os.remove(temp_path)

        except Exception as e:
            print(f"Could not convert {report_name} to CSV: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {report_name}: {e}")
    except Exception as e:
        print(f"Unexpected error occurred while downloading {report_name}: {e}")


def download_reports():
    try:
        print("Waiting for the year dropdown to appear...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "cmbYear"))
        )
        print("Dropdown found!")

        with ThreadPoolExecutor(max_workers=5) as executor:
            for year in [2024]:
                try:
                    year_select = Select(driver.find_element(By.ID, "cmbYear"))
                    year_select.select_by_value(str(year))

                    for month in range(1, 13):
                        try:
                            month_select = Select(driver.find_element(By.ID, "cmbMonth"))
                            month_select.select_by_value(str(month))

                            category_select = Select(driver.find_element(By.ID, "reportCategorySelectList"))
                            category_select.select_by_value("all")

                            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
                            submit_button.click()
                            print(f"Submit button clicked for Year {year}, Month {month}, Category 'СИТЕ'. Waiting for report links...")

                            WebDriverWait(driver, 60).until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/Repository/Reports/']"))
                            )
                            print(f"Report links for Year {year}, Month {month} loaded successfully.")

                            report_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/Repository/Reports/']")
                            if not report_links:
                                print(f"No reports found for Year {year}, Month {month}.")
                                continue

                            for link in report_links:
                                report_name = link.get_attribute("href").split("/")[-1]
                                report_url = link.get_attribute("href")
                                print(f"Found report: {report_name} with URL: {report_url}")

                                executor.submit(download_report, report_url, report_name)

                        except Exception as e:
                            print(f"Error processing month {month} for year {year}: {e}")
                            traceback.print_exc()

                except Exception as e:
                    print(f"Error processing year {year}: {e}")
                    traceback.print_exc()

    except Exception as e:
        print(f"Error during report downloading process: {e}")
        traceback.print_exc()


download_reports()
driver.quit()


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.mse.mk/mk/reports')

    try:
        download_reports(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
