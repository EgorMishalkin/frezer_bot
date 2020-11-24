# словарь со всеми продуктами
freezer = {'сок': 30,
           'яблоко': 25,
           'котлеты': 1,
           'суп': 1}
com = ''


# функция добавления продукта
def add(what, how_long):
    freezer[what] = how_long
    print('Продукт добавлен!')


# функция удаления продукта
def delete(what):
    del freezer[what]
    print('Успешно удалено!')


# функция сортировки
def notice():
    # создаем новый словарь, где будем записывать
    global freezer
    clear_freezer = {}
    for key, value in freezer.items():
        if value == 3:
            print(f'{key} испортится через 3 дня! поторопитесь съесть)')
            clear_freezer[key] = value
        elif value == 2:
            print(f'{key} испортится через 2 дня! поторопитесь съесть!')
            clear_freezer[key] = value
        elif value == 1:
            print(f'{key} испортится завтра! поторопитесь съесть!')
            clear_freezer[key] = value
        elif value == 0:
            print(f'{key} испортился! обязательно выкиньте продукт')
        else:
            clear_freezer[key] = value

    freezer = clear_freezer


# функция нового дня(все сроки годности - 1)
def new_day():
    # уменьшам каждое значение на 1
    global freezer
    for key, value in freezer.items():
        value -= 1
        freezer[key] = value


# основной цикл
while com != "стоп":
    print("--------------------")
    print("--------МЕНЮ--------")
    print("======Команды:======")
    print("1. Добавить продукт")
    print("2. Удалить продукт")
    print("3. увед")
    print("0. Выход")
    print("====================")
    com = input('Введите команду: ')
    # добавление продукта
    if 'добавить' in com.lower():
        product = input("Название продукта: ")
        # проверка на то, число ли вводит пользователь или нет
        try:
            time = int(input("сколько дней хранится?: "))
            add(product, time)
        # если не число
        except ValueError:
            print('Недопустимое значение! введите число')

    # удаление продукта
    elif 'удалить' in com.lower():
        print("Какой продукт удалить: ", end='')
        # выводим весь список продуктов в холодильнике
        for i in list(freezer.keys()):
            print(i, end=' ')
        print()
        product = input()
        # Если неверный ключ
        try:
            delete(product)
        except KeyError:
            print("Такого продукта в холодильнике нет!")

    # сортирока списка продуктов

    elif 'увед' in com.lower():
        new_day()
        notice()

    # завершение
    elif 'стоп' in com.lower():
        print('завершаю работу')
        break

    else:
        print('Неизвестная команда')


print(freezer)
