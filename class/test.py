from requests import get, post, delete

# все данные
print(get('http://localhost:5000/api/v2/user').json())

# 1 элемент
print(get('http://localhost:5000/api/v2/user/1').json())

# нет юзера
print(get('http://localhost:5000/api/v2/user/100000000000').json())

# не верный запрос
print(get('http://localhost:5000/api/v2/user/q').json())


# пустой запрос
print(post('http://localhost:5000/api/v2/user').json())

# не все поля
print(post('http://localhost:5000/api/v2/user', json={'name': 'hello'}).json())

# все поля
print(post('http://localhost:5000/api/v2/user', json={
'name': 'Kostya',
'surnae': 'Podvysotskiy',
'age': 18,
'address': 'Ne skazu',
'email': 'kostya.vit.99@mail.ru',
'position': 'proga',
'speciality': 'proger',
'hashed_password': 'wolf'}).json())


# нет в базе
print(delete('http://localhost:5000/api/v2/user/999').json())

# удалить 1
print(delete('http://localhost:5000/api/v2/user/1').json())
