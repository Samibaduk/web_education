import time
from datetime import datetime

# в нашей программе одна минута реального времени будет соответствовать одной секунде времени работы программы
# если установить коэффициент в 0.5, то половине секунды времени работы программы
COEFF = 1


def dish(num, prepare, wait):
    """
    функция имитирует приготовление одного блюда
    :param num: номер блюда по порядку
    :param prepare: сколько минут на подготовку
    :param wait: сколько минут на ожидание готовности
    :return:
    """
    print(f"start {datetime.now().strftime('%HH:%MM:%SS')} prepare dish {num} {prepare} min")
    time.sleep(COEFF * prepare)
    print(f"start {datetime.now().strftime('%HH:%MM:%SS')} wait dish {num} {wait} min")
    time.sleep(COEFF * wait)
    print(f"{datetime.now().strftime('%HH:%MM:%SS')} dish {num} is ready")


def main():
    """
    функция запускает "приготовление" блюд
    :return:
    """
    dish(1, 2, 3)
    dish(2, 5, 10)
    dish(3, 3, 5)


if __name__ == '__main__':
    t0 = time.time()  # запоминаем время начала работы
    main()  # запускаем приготовление
    delta = int((time.time() - t0) / COEFF)  # считаем затраченное время
    print(f"{datetime.now().strftime('%HH:%MM:%SS')} It took {delta} min")