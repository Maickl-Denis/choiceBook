from itertools import count
import random
import os
import shutil
import zipfile
from ruamel.std.zipfile import delete_from_zip_file



#собираем множество ключ номер по порядку значени имя директории и возвращаем его
def LsBook(dir):
    count = 1
    NumDir = {}
    for name in dir:
        NumDir[count] = name
        count += 1
    return NumDir

#Из множества выбираем только одну директорию и возращаем ее в списоке с дополнительным параметром 1 - это zip архив, 0 - папка

def Randomaizer(arraySet: set, idx = 1):
    size = len(arraySet)
    choice = arraySet[random.randint(idx, size)]                              
    if "zip" in choice:
        return [choice, 1]          
    else:
        return [choice, 0]



def GetBook(catalog, path):
    dstPath = 'G:\\py\\Book\\'
    if catalog[1] == 0:                                                         # работаем с папками
        os.chdir(path+'\\'+catalog[0])                                          # устанавливаем рабочую директорию 
        catalogIsBook = LsBook((os.listdir()))                                  # получаем список файлов в директории
        if catalogIsBook:
            book = Randomaizer(catalogIsBook)[0]                                # выбираем одну книгу из всего списка
            shutil.move(book, dstPath)                                          # перемещаем книгу в нужное место
            print(f"Я выбрал для вас книгу {book} из каталога {catalog[0]}")
        else: print('Книг в каталоге нет')
    else:                                                                       # работаетм с архивом
        z = zipfile.ZipFile(catalog[0], 'r')                                    # читаем архив
        NumCat = LsBook(z.namelist())                                           # получаем нумерованый список книг в архиве
        if NumCat:
            book = Randomaizer(NumCat)[0]                                       # выбираем одну книгу из всего списка
            print(f"Я выбрал для вас книгу {book}")
            z.extract(book, dstPath)                                            # копируем книгу в нужное место
            print(f"Удаляю книгу {book} из архива {catalog[0]}")
            delete_from_zip_file(catalog[0], pattern=book)                      # удаление файла из архива
            print("Книга удалена")
        else: print('Архив пуст')


path = "G:\\py\\Book\\book"                                                     # путь к директории с книгами

print('Я ищу книгу для вас')
os.chdir(path)                                                                  # устанавливаем рабочую директорию 
LsB = LsBook(os.listdir())
if len(LsB) > 1:
    oneDirOfCatalog = (Randomaizer(LsB, 2))                                     # Выбираем каталог из которого будет выбираться книга (значение 2 показывает с какого каталога начинать выбор)
    GetBook(oneDirOfCatalog, path)                                              # копируем выбраную книгу в папку у удаляется она из общего каталога
else:
    print("В каталоге нет ресурсов для поиска книги")
input("нажмите любую кнопку для завершения программы")
