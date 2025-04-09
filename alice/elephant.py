from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)
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

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!"],
            'elephant': False
        }
        res['response']['text'] = f'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    animal = 'кролик' if sessionStorage[user_id]['elephant'] else 'слон'


    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
        'я покупаю',
        'я куплю'
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = f'Отлично! {animal.title()}а можно найти на Яндекс.Маркете!'
        if sessionStorage[user_id]['elephant']:
            res['response']['end_session'] = True
        else:
            sessionStorage[user_id] = {
                'suggests': [
                    "Не хочу.",
                    "Не буду.",
                    "Отстань!"],
                'elephant': True
            }
            res['response']['text'] += f'\nА теперь купи кролика!'
            res['response']['buttons'] = get_suggests(user_id)
    else:
        res['response']['text'] = \
            f"Все говорят '{req['request']['original_utterance']}', а ты купи {animal}а!"
        res['response']['buttons'] = get_suggests(user_id)


# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    animal = 'кролик' if sessionStorage[user_id]['elephant'] else 'слон'


    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session


    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": f"https://market.yandex.ru/search?text={animal}",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
