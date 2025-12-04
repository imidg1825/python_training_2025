from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

print("🚀 Запускаем 'стелс' версию теста!")

# Настройки для обхода защиты
chrome_options = Options()

# Делаем браузер более "человеческим"
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Запускаем браузер в обычном режиме (не headless)
chrome_options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Скрываем что используем Selenium
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 15)  # Увеличиваем время ожидания

try:
    print("🔍 Открываем Google...")
    driver.get("https://www.google.com")
    
    # Имитируем человеческую задержку
    time.sleep(random.uniform(2, 4))
    
    # Ищем поле поиска разными способами
    search_selectors = [
        (By.NAME, "q"),
        (By.CLASS_NAME, "gLFyf"),
        (By.CSS_SELECTOR, "textarea[name='q']"),
        (By.XPATH, "//textarea[@name='q']")
    ]
    
    search_box = None
    for by, selector in search_selectors:
        try:
            search_box = driver.find_element(by, selector)
            break
        except:
            continue
    
    if search_box:
        # Вводим текст с человеческими паузами
        search_text = "Python автоматизация тестирования"
        for char in search_text:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Имитация печати
        
        time.sleep(1)
        search_box.send_keys(Keys.RETURN)
        print("✅ Поисковый запрос отправлен (с человеческими паузами)")
    else:
        print("❌ Не удалось найти поле поиска")
        # Делаем скриншот чтобы понять что видит браузер
        driver.save_screenshot("debug_google_page.png")
        print("📸 Скриншот страницы сохранён как 'debug_google_page.png'")
        driver.quit()
        exit()

    # Ждём результаты с увеличенным временем
    print("⏳ Ждём загрузки результатов...")
    time.sleep(random.uniform(3, 6))
    
    # Проверяем разные возможные структуры результатов
    result_selectors = [
        "#search .g",
        ".g .rc",
        "[data-sokoban-container] div",
        "div#search div",
        ".MjjYud"  # Новый селектор для Google
    ]
    
    results_found = False
    for selector in result_selectors:
        try:
            results = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(results) > 0:
                print(f"✅ Найдено результатов (селектор: {selector}): {len(results)}")
                results_found = True
                break
        except:
            continue
    
    if not results_found:
        # Если результаты не найдены, проверяем не попали ли на капчу
        page_source = driver.page_source.lower()
        if "captcha" in page_source or "робот" in page_source or "robot" in page_source:
            print("🚫 Обнаружена проверка CAPTCHA! Google заподозрил автоматизацию.")
            print("💡 Решение: Попробуй запустить тест позже или используй другой IP")
        else:
            print("🤔 Результаты не найдены, но CAPTCHA не обнаружена")
            print("📄 Текст страницы сохранён в 'page_source.html'")
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

    # Сохраняем скриншот
    driver.save_screenshot("google_stealth_results.png")
    print("✅ Скриншот сохранён как 'google_stealth_results.png'")
    
    print(f"📄 Заголовок страницы: {driver.title}")
    print(f"🌐 Текущий URL: {driver.current_url}")

except Exception as e:
    print(f"❌ Произошла ошибка: {e}")
    # Сохраняем скриншот при ошибке
    driver.save_screenshot("error_screenshot.png")
    print("📸 Скриншот ошибки сохранён")

finally:
    # Закрываем браузер
    driver.quit()
    print("✅ Браузер закрыт")
    print("🎉 'Стелс' тест завершён!")