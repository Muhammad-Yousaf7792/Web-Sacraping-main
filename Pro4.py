from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
import time

mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anas,.1122",
    database="anas_db"
)
cursor = mysql_conn.cursor()

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://ypages.pk/lahore/cafes.htm")
time.sleep(6)

print("PAGE TITLE:", driver.title)

tel_elements = driver.find_elements(
    By.XPATH, "//*[contains(text(),'Tel')]"
)

print("Tel elements found:", len(tel_elements))

count = 0
seen = set()

for tel in tel_elements:
    try:
        block = tel.find_element(By.XPATH, "./ancestor::div[1]")
        text = block.text.strip().split("\n")
        
        cafe_name = text[0]

        if len(cafe_name) < 4 or cafe_name in seen:
            continue

        phone = None
        for line in text:
            if "Tel" in line:
                phone = line.replace("Tel:", "").strip()

        email = "N/A"
        for line in text:
            if "@" in line:
                email = line.strip()

        cursor.execute(
            """
            INSERT INTO Bag (cafe_name, phone, email)
            VALUES (%s, %s, %s)
            """,
            (cafe_name, phone, email)
        )

        seen.add(cafe_name)
        count += 1
        print("Inserted:", cafe_name)

        if count == 10:
            break

    except Exception as e:
        continue

mysql_conn.commit()
driver.quit()

print(f"✅ {count} cafes successfully inserted!")