import os
import random
import shutil
import zipfile
from lxml import etree
from tqdm import tqdm

def list_all_folder_is_book(dir_path: list) -> dict:
    """
    Создаем словарь со всеми папками и архивами в библиотеке
    :param dir_path: Список элементов в директории
    :return: словарь с нумеровыными значения элементов в папке
    """
    return {count: name for count, name in enumerate(dir_path)}


def randomaizer(dict_directories: dict, idx=1) -> list:
    """
    Из нумаровного словаря с директориями выбираем один элемент
    :param dict_directories: Словарь со всеми директориями из которого надо выбрать один,
    приходит: ключь - номер по порядку, Значение - название директории или архива
    :param idx: Значение с какого элемента начинать выбирать элемент. По умолчанию первый (0) элемент пропускается
    :return: Возращаем список [Элемент в каталоге, флаг]
    Флаг:   1 - элемент является zip архивом
            0 - элемент является папкой
    """
    choice = dict_directories[random.randint(idx, len(dict_directories) - 1)]
    if choice.endswith('.zip'):
        return [choice, 1]
    else:
        return [choice, 0]


def get_book(catalog, path, dst_path) -> None:
    """
    Функция реализует получение книги из каталога, сохранение ее в нужную директорию и удаления из каталого/архива
    :param catalog: Приходит имя каталога и его тип 1 - zip архив, 0 - папка
    :param path: путь до библиотеки
    :param dst_path: путь куда сохранить выбранную книгу
    :return: None
    """
    if catalog[1] == 0:
        os.chdir(path + '\\' + catalog[0])
        book_in_catalog = list_all_folder_is_book((os.listdir()))
        if book_in_catalog:
            book = randomaizer(book_in_catalog, 0)[0]
            shutil.move(book, dst_path)
            print(f"Я выбрал для вас книгу {book} из каталога {catalog[0]}")
        else:
            print('Книг в каталоге нет')
    else:
        with zipfile.ZipFile(catalog[0], 'r') as z_file:
            books_in_archive = list_all_folder_is_book(z_file.namelist())
            if books_in_archive:
                book = randomaizer(books_in_archive, 0)[0]
                print(f"Я выбрал для вас книгу {book}")
                temp_zip = zipfile.ZipFile('temp.zip', 'w', compression=zipfile.ZIP_DEFLATED)
                print(f"Удаляю книгу {book} из архива {catalog[0]}")
                for file in tqdm(z_file.filelist):
                    if file.filename != book:
                        zipfile.ZipFile(catalog[0]).extract(file.filename)
                        temp_zip.write(file.filename)
                        os.remove(file.filename)
                    else:
                        z_file.extract(book, dst_path)
            else:
                print("Книг нет")
        temp_zip.close()
        os.remove(catalog[0])
        os.rename("temp.zip", catalog[0])
    if book:
        new_name_book = f"{info_book(dst_path + "\\" + book)}.fb2"
        os.rename(dst_path+"\\"+book, dst_path+"\\"+new_name_book)
        print(f"Книга называется {new_name_book}")


def info_book(book):
    result = ''
    tree = etree.parse(book, parser=etree.XMLParser(recover=True, remove_blank_text=True))

    ns_map = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0', 'l': 'http://www.w3.org/1999/xlink'}

    name_book = tree.xpath('//fb:description/fb:title-info/fb:book-title/text()', namespaces=ns_map)
    f_name = tree.xpath('//fb:description/fb:title-info/fb:author/fb:first-name/text()', namespaces=ns_map)
    m_name = tree.xpath('//fb:description/fb:title-info/fb:author/fb:middle-name/text()', namespaces=ns_map)
    l_name = tree.xpath('//fb:description/fb:title-info/fb:author/fb:last-name/text()', namespaces=ns_map)

    if f_name:
        result += f'{f_name[0]} '
    if m_name:
        result += f'{m_name[0]} '
    if l_name:
        result += f'{l_name[0]} - '
    if name_book:
        result += f'{name_book[0]}'

    return result

if __name__ == '__main__':
    PATH = r"[path]"
    DST_PATH = r"[path]"

    os.chdir(PATH)

    all_archive_books = list_all_folder_is_book(os.listdir())


    if len(all_archive_books) > 1:
        one_dir_of_catalog = randomaizer(all_archive_books)
        try:
            get_book(one_dir_of_catalog, PATH, DST_PATH)
        except Exception as e:
            print(e)
        finally:
            input('Нажмите любую клавишу')
    else:
        input("Не нашел где искать книги")

