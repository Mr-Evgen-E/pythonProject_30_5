import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome('D:\pythonProject\pythonProject_30_5_1\driver\chromedriver.exe')
    # Устанавливаем неявное ожидание
    driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.set_window_size(1200, 900)
    yield driver
    driver.quit()


email = "Enter your e-mail"
password = "Enter your password"


def test_user_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку входа на страницу "Мои питомцы"
    driver.find_element(By.CSS_SELECTOR, '.nav-link[href="/my_pets"]').click()

    # После клика входа на страницу пользователя ожидаем (неявное ожидание)
    # появления класса (task3.fill) с данными пользователя и с карточками животных
    driver.find_element(By.CSS_SELECTOR, '.task3.fill')

    # Ожидаем появления элемента в структуре документа при получении количества питомцев пользователя
    WDW(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left')))
    # Получаем количество животных из информации об пользователе
    receive_of_number_pets = driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    split_number = receive_of_number_pets.get_attribute('textContent').split("\n")
    numbers_of_pets = int(split_number[3].split(": ")[1])

    # Ожидаем появления элемента в структуре документа при запросе фотографий
    WDW(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                         '.table.table-hover th[scope="row"] img')))
    images = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover th[scope="row"] img')

    names = []
    descriptions = []
    ages = []

    # Ожидаем появления элемента в структуре документа при запросе имени, породы и возраста
    # Задержка при поиске элемента имени.
    (WDW(driver, 5).until
     (EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[2]/div/div/table/tbody/tr[1]/td[1]'))))
    # Задержка при поиске элемента возраста
    (WDW(driver, 5).until
     (EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[2]/div/div/table/tbody/tr[1]/td[3]'))))
    # Задержка при поиске элемента породы (описания)
    (WDW(driver, 5).until
     (EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[2]/div/div/table/tbody/tr[1]/td[2]'))))

    # Получаем списки имен, возрастов и пород и записываем в соответствующие переменные
    for i in range(1, numbers_of_pets + 1):
        name_of_pet = (driver.find_element(By.XPATH,
                                           f'/html/body/div[1]/div/div[2]/div/div/table/tbody/tr[{i}]/td[1]')
                       .get_attribute('textContent').replace(' ', ''))
        names.append(name_of_pet)

    for i in range(1, numbers_of_pets + 1):
        age_of_pet = (driver.find_element(By.XPATH,
                                          f'/html/body/div[1]/div/div[2]/div/div/table/tbody/tr[{i}]/td[3]')
                      .get_attribute('textContent').replace(' ', ''))
        ages.append(age_of_pet)

    for i in range(1, numbers_of_pets + 1):
        description_of_pet = (
            driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div/table/tbody/tr[{i}]/td[2]')
            .get_attribute('textContent').replace(' ', ''))
        descriptions.append(description_of_pet)

    # Проверяем наличие питомцев у пользователя
    assert numbers_of_pets > 0

    # Проверяем, что у больше половины животных есть фото
    count_photo_not_empty = 0
    count_photo_empty = 0
    for i in range(numbers_of_pets):
        image_source = images[i].get_attribute('src')
        if image_source != '':
            count_photo_not_empty += 1
        else:
            count_photo_empty += 1

    assert count_photo_not_empty > count_photo_empty

    # Проверяем, что у всех питомцев есть имя
    for name in names:
        assert name != ''

    # Проверяем, что у всех питомцев есть возраст
    for age in ages:
        int(age)
        assert age != ''

    # Проверяем, что у всех питомцев есть порода
    for description in descriptions:
        assert description != ''

    # Данный тест перед проверкой совпадения имен, т.к. если имена совпадают, то до этого теста не доходит
    # Для полной картины все тесты надо разбить по разным функциям
    # Формируем список словарей, что бы проверить на полное соответствие "имя, порода, возраст" питомцев
    keys = ['name', 'description', 'age']
    zipped = zip(names, descriptions, ages)
    list_of_dict = [dict(zip(keys, values)) for values in zipped]

    for i in range(len(list_of_dict) - 1):
        for i2 in range(i, len(list_of_dict) - 1):
            coincide = sum(
                k in list_of_dict[i2 + 1] and list_of_dict[i][k] == list_of_dict[i2 + 1][k] for k in list_of_dict[i])

            # Проверка на совпадение всех 3 элементов во всех словарях (полное совпадение Имя, Порода, Возраст)
            assert coincide != 3

    # Проверяем повторяющиеся имена в списке
    has_duplicates_names = len(names) > len(set(names))
    assert not has_duplicates_names
