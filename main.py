# словарь со всеми продуктами
freezer = {}
# print("выберите продукт из вашего холодильника")
com = ''


# функция добавления продукта
def add(what, how_long):
    freezer[what] = how_long
    print('Продукт добавлен!')


# функция удаления продукта
def delete(what):
    del freezer[what]
    print('Успешно удалено!')


while com != "стоп":
    print("--------------------")
    print("--------МЕНЮ--------")
    print("======Команды:======")
    print("1. Добавить продукт")
    print("2. Удалить продукт")
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

    # завершение
    elif 'стоп' in com.lower():
        print('завершаю работу')
        break

    else:
        print('Неизвестная команда')

print(freezer)
