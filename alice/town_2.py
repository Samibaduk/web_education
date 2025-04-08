from flask import Flask, request, jsonify
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# создаем словарь, в котором ключ — название города,
# а значение — массив, где перечислены id картинок,
# которые мы записали в прошлом пункте.

cities = {
    'москва': ['1030494/036ef357cdfdcc61cd38',
               '1652229/5ea7e1273cbe9d6ee39f'],
    'нью-йорк': ['1652229/b946fde259c7e4da1fbc',
                 '1656841/f59018f2a126b91a0f61'],
    'париж': ["1652229/e124bccd84887bf26805",
              '1652229/7523ed7fc23b1e8eaa88']
}

LEN_cities = len(cities)

# создаем словарь, где для каждого пользователя
# мы будем хранить его имя
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови своё имя!'
        sessionStorage[user_id] = {
            'first_name': None,
            'game_started': False
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            sessionStorage[user_id]['guessed_cities'] = []
            res['response'][
                'text'] = 'Приятно познакомиться, ' \
                          + first_name.title() \
                          + '. Я - Алиса. Отгадай город по фото!'
            # получаем варианты buttons из ключей нашего словаря cities
            res['response']['buttons'] = [
                {
                    'title': 'Да',
                    'hide': True
                },
                {
                    'title': 'Нет',
                    'hide': True
                },
                {
                    'title': 'Помощь',
                    'hide': True
                }
            ]
    # если мы знакомы с пользователем и он нам что-то написал,
    # то это говорит о том, что он уже говорит о городе,
    # что хочет увидеть.
    else:
        if not sessionStorage[user_id]['game_started']:
            if 'да' in req['request']['nlu']['tokens']:
                if len(sessionStorage[user_id]['guessed_cities']) == LEN_cities:
                    res['response']['text'] = 'Ты угадал все города!'
                    res['end_session'] = True
                else:
                    res['response']['text'] = '0_0'
                    sessionStorage[user_id]['game_started'] = True
                    sessionStorage[user_id]['attemt'] = 1
                    play_game(res, req)

            elif 'нет' in req['request']['nlu']['tokens']:
                res['response']['text'] = 'Ну и ладно!'
                res['end_session'] = True
            elif 'помощь' in req['request']['nlu']['tokens'] or 'помощь' in req['request']['original_utterance'].lower():
                res['response']['text'] = 'Это строка помощи об игре. Твоя задача: Угадать город по фото'
            else:
                res['response']['text'] = 'Я не распознала ответ, так играем или нет?'
                res['response']['buttons'] = [
                    {
                        'title': 'Да',
                        'hide': True
                    },
                    {
                        'title': 'Нет',
                        'hide': True
                    },
                    {
                        'title': 'Помощь',
                        'hide': True
                    }
                ]
        else:
            play_game(res, req)



def play_game(res, req):
    user_id = req['session']['user_id']
    attemt = sessionStorage[user_id]['attemt']

    if attemt == 1:
        city = list(cities.keys())[random.randint(0, LEN_cities - 1)]
        while city in sessionStorage[user_id]['guessed_cities']:
            city = list(cities.keys())[random.randint(0, LEN_cities - 1)]
        sessionStorage[user_id]['city'] = city

        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['title'] = 'Что это за город?'
        res['response']['card']['image_id'] = cities[city][attemt - 1]
        res['response']['buttons'] = [{'title': 'Помощь', 'hide': True}]
    else:
        city = sessionStorage[user_id]['city']
        if get_city(req) == city:
            res['response']['text'] = 'Правильно, угадал! Сыграть ещё?'
            res['response']['buttons'] = [
                {
                    'title': 'Да',
                    'hide': True
                },
                {
                    'title': 'Нет',
                    'hide': True
                },
                {
                    'title': 'Помощь',
                    'hide': True
                }
            ]
            sessionStorage[user_id]['guessed_cities'].append(city)
            sessionStorage[user_id]['game_started'] = False
        else:
            if attemt == 3:
                res['response']['text'] = 'Не угадал, попытки закончились. Это был ' + city.title() + '. Сыграем ещё?'
                res['response']['buttons'] = [
                    {
                        'title': 'Да',
                        'hide': True
                    },
                    {
                        'title': 'Нет',
                        'hide': True
                    },
                    {
                        'title': 'Помощь',
                        'hide': True
                    }
                ]
                sessionStorage[user_id]['guessed_cities'].append(city)
                sessionStorage[user_id]['game_started'] = False
            else:
                res['response']['text'] = 'Неправильно!'
                res['response']['card'] = {}
                res['response']['card']['type'] = 'BigImage'
                res['response']['card']['title'] = 'Не правильно, даю еще попытку! Что это за город?'
                res['response']['card']['image_id'] = cities[city][attemt - 1]
                res['response']['buttons'] = [{'title': 'Помощь', 'hide': True}]
    sessionStorage[user_id]['attemt'] += 1

def get_city(req):
    # перебираем именованные сущности
    for entity in req['request']['nlu']['entities']:
        # если тип YANDEX.GEO то пытаемся получить город(city),
        # если нет, то возвращаем None
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value'].keys():
                return entity['value']['city']
            else:
                return None
        return None

def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    app.run()
