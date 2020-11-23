# словарь со всеми продуктами
freezer = {}
# словарь с отсортированными значениями
sorted_freezer = {}
com = ''

# функция сортировки


def sort():
    for i in sorted(freezer.items(), key=lambda para: para[1]):
        sorted_freezer = i
        print(sorted_freezer)

# функция добавления продукта


def add(what, how_long):
    freezer[what] = how_long
    print('Продукт добавлен!')

# функция удаления продукта


def delete(what):
    del freezer[what]
    print('Успешно удалено!')


# основной цикл


while com != "стоп":
    print("--------------------")
    print("--------МЕНЮ--------")
    print("======Команды:======")
    print("1. Добавить продукт")
    print("2. Удалить продукт")
    print("3. Отсортировать список")
    print("0. Выход")
    print("====================")
    com = input('Введите команду: ')
    # добавление продукта
    if 'добавить' in com.lower():
        product = input("Название продукта: ")
        # проверка на то, число ли вводит пользователь или нет
        try:
            time = int(input(("сколько дней хранится?: ")))
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

    elif 'сорт' in com.lower():
        sort()

    # завершение
    elif 'стоп' in com.lower():
        print('завершаю работу')
        break

    else:
        print('Неизвестная команда')


print(freezer)
