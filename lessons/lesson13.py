from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

print("🚀 Запускаем первый автоматизированный тест!")

# Настройка драйвера Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 1. Открываем Google
    driver.get("https://www.google.com")
    print("✅ Google открыт")
    
    # 2. Находим поле поиска и вводим запрос
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Python автоматизация тестирования")
    search_box.send_keys(Keys.RETURN)
    print("✅ Поисковый запрос отправлен")
    
    # 3. Ждём немного чтобы увидеть результат
    time.sleep(3)
    
    # 4. Проверяем, что результаты загрузились
    results = driver.find_elements(By.CSS_SELECTOR, "div.g")
    if len(results) > 0:
        print(f"✅ Найдено результатов: {len(results)}")
    else:
        print("❌ Результаты не найдены")
        
    # 5. Делаем скриншот
    driver.save_screenshot("google_search_results.png")
    print("✅ Скриншот сохранён")

except Exception as e:
    print(f"❌ Произошла ошибка: {e}")

finally:
    # Закрываем браузер
    driver.quit()
    print("✅ Браузер закрыт")
    print("🎉 Первый тест завершён успешно!")