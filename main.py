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
    for key, value in freezer.items():
        if value == 3:
            print(f'{key} испортится через 3 дня! поторопитесь съесть)')
        if value == 2:
            print(f'{key} испортится через 2 дня! поторопитесь съесть!')
        if value == 1:
            print(f'{key} испортится завтра! поторопитесь съесть!')
        if value == 0:
            print(f'{key} испортился! обязательно выкиньте продукт')
            print(freezer)


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
        product = input("Какой продукт удалить: ")
        # Если неверный ключ
        try:
            delete(product)
        except KeyError:
            print("Такого продукта в холодильнике нет!")

    # сортирока списка продуктов

    elif 'увед' in com.lower():
        notice()

    # завершение
    elif 'стоп' in com.lower():
        print('завершаю работу')
        break

    else:
        print('Неизвестная команда')


print(freezer)
