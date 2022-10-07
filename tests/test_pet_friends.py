import os

from api import PetFriends
from settings import val_email, val_password, neval_email, neval_password

pf = PetFriends()


def test_get_api_key_for_user(email=val_email, password=val_password):
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_val_data(name='Pублик', animal_type='немецкая овчарка', age='3', pet_photo='images/dog.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(val_email, val_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(val_email, val_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Собака-Балабака', "пес", "5", "images/dog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()


def test_update_pet_info(name='Pushkin', animal_type='Собака', age=2):
    _, auth_key = pf.get_api_key(val_email, val_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


############### 10 тест-кейсов

# 1. Добавление питомца без фото
def test_add_pet_new_without_photo(name='Граф', animal_type='лабрадор', age='4'):
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet_inf_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


# 2. Добавить фотографию питомца
def test_add_pet_new_photo(pet_photo='images/dog1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(val_email, val_password)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_new_photo_pet(auth_key, pet_id, pet_photo)

    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:

        raise Exception("There is not my pets")


# 3. Проверяем запрос с валидным email и с невалидным password (negative test)
def test_get_api_key_for_user_invalid_password(email=val_email, password=neval_password):
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 4. Проверяем запрос с невалидным email и с валидным password (negative test)
def test_get_api_key_for_user_invalid_email(email=neval_email, password=val_password):
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 5. Проверяем запрос с невалидным email и с невалидным password (negative test)
def test_get_api_key_for_user_invalid_email_pass(email=neval_email, password=neval_password):
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 6. Передаем пустое значение name при создании питомца (negative test)
def test_add_new_pet_with_empty_name(name='', animal_type='dog', age='3', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    #  Питомец создается с пустым значением в name


# 7. В параметрах name передаем большое значение при создании питомца (negative test)
def test_add_new_pet_with_big_name(
        name='Richi кличка собаки. Чистокровный пес. Имеет 2 награды "Самый красивый пес 2021, 2022 годов. Любимец маленьких детей. Игривый, ласковый, верный защитник!!!',
        animal_type='немецкая овчарка', age='10', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    # Питомец создан с большим количеством слов в имени


# 8. Добавление питомца сo спец.символами вместо букв в name (negative test)
def test_add_new_pet_with_name_characters(name='!@#$%^&&*()_+=?/.,`', animal_type='немецкая овчарка', age='10',
                                          pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    # Питомец создан с именем состоящим из спец.символов


# 9. В параметрах передадим отрицательный возраст при создании питомца (negative test)
def test_add_new_pet_negative_age(name='Richi', animal_type='немецкая овчарка', age='-3', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    # Питомец создан с отрицательным возрастом


# 10. В параметрах передадим возраст больше 100 при создании питомца (negative test)
def test_add_new_pet_age_more(name='Richi', animal_type='немецкая овчарка', age='1000', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
   #Питомец создан с возрастом 1000 лет


# 11. В параметрах передадим возраст буквами при создании питомца (negative test)
def test_add_pet_new_fail_letter_age(name='Richard', animal_type='лабрадор', age='two'):
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet_inf_without_photo(auth_key, name, animal_type, age)

    assert status == 200
   # Питомец добавлен с возрастом "two" вместо 2


# 12. Удалить чужого питомца (negative test)
def test_delete_another_pet():
    _, auth_key = pf.get_api_key(val_email, val_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    # Берём id любого питомца из списка и отправляем запрос на удаление
    pet_id = all_pets['pets'][3]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    #Чужой питомец успешно удален


# 13. В параметрах передадим пустые значения при создании питомца (negative test)
def test_add_pet_new_fail_lempty_value(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(val_email, val_password)

    status, result = pf.add_new_pet_inf_without_photo(auth_key, name, animal_type, age)

    assert status == 200
     # Питомец добавлен с пустыми значениями
