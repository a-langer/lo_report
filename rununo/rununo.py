#!/usr/bin/python3
# http://stackoverflow.com/questions/7783678/remote-control-or-script-open-office-to-edit-word-document-from-python
# установить пакет libreoffice-librelogo
# запускать от python3 ./script.py; установщик пакетов python3-pip, зпускать как pip3
# soffice.exe "-accept=socket,host=localhost,port=2002;urp;" -writer -headless &
# Для Windows - питон встроен в Libreoffice !!!
# set path="C:\Program Files\LibreOffice 5\program"
# set path="C:\Program Files (x86)\LibreOffice5\program"
# перейти в cd "C:\Program Files (x86)\LibreOffice5\program" и выполнить python D:\Distr\program\Python\My-Project\rununo.py
# http://lucasmanual.com/mywiki/OpenOffice#Modifyingtext
# Джанго http://davidmburke.com/2010/09/21/django-and-openoffice-org-uno-reports/
"""
Открыть консоль в каталоге "C:\Program Files (x86)\LibreOffice 5\program"
запускать скрипты оттуда:
C:\Program Files (x86)\LibreOffice 5\program>python D:\Distr\program\Python\My-Project\oracle.py
C:\Program Files (x86)\LibreOffice 5\program>python D:\Distr\program\Python\My-Project\rununo.py
все будет работать на питоне встроенном в libreoffice (3.3.5).
"""

import os, sys, json
print("debug0")
# добавляем каталог модуля libreoffice-uno (не обязательно)
lib_uno = os.path.abspath(os.path.join("C:/Program Files (x86)/LibreOffice 5/program/"))
sys.path.append(lib_uno)
print("debug0.1")
import uno # модуль libreoffice-uno
print("debug0.2")
#import unohelper
#import socket
   
print("debug1")
   
############# libreoffice UNO
ctx = uno.getComponentContext()
service_manager = ctx.getServiceManager() 

# Конфиги
url      = "file:///C:/Users/langer/script/LO_REPORT/rununo/"
file     = "myfile.odt"
new_file = "new_myfile.odt"
host     = "localhost"
port     = 2002

print("debug2")

resolver = ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", ctx)
context = resolver.resolve("uno:socket,host="+ str(host) +",port="+ str(port) +";urp;StarOffice.ComponentContext")
desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
document = desktop.loadComponentFromURL(url+file, "_blank", 0, ())

replace_desc = document.createReplaceDescriptor() 

print("debug3")

def replaceText(key, value):
    replace_desc.setSearchString("{{"+str(key)+"}}") # Текст для замены {{text}}
    print("Передано в UNO: ",key, value) # отладка

    find_iter = document.findFirst(replace_desc)
    while find_iter:
        find_iter.String = str(value) # в виде строки
        find_iter = document.findNext(find_iter.End, replace_desc) # заменяем текст
        if not find_iter: break # текст заменен

print("debug4")
        
    #document.dispose()
############# end UNO
 

############# Парсим  json
out_parameter = """
{
  "template": "myfile.odt",
  "outformat": "docx",
  "text": {
    "name": "Иванов Иван Иванович",
    "age": 30,
    "keywords": [ "human", "developer" ]
  },
  "placeholder": {
    "name": "Иванов Иван Иванович",
    "age": 30,
    "keywords": [ "human", "developer" ]
  },
  "input": {
    "name": "Иванов Иван Иванович",
    "age": 30,
    "keywords": [ "human", "developer" ]
  },
  "userfield": {
    "name": "Иванов Иван Иванович",
    "age": 30,
    "keywords": [ "human", "developer" ]
  }
}
"""

print("debug5")

try:
    decoded = json.loads(out_parameter)
    text_json        = decoded['text']        # замена текста
    placeholder_json = decoded['placeholder'] # заполнение плейсхолдеров
    input_json       = decoded['input']       # заполнение инпутов
    userfield_json   = decoded['userfield']   # заполнение узерфилдов
    #print ("JSON parsing example: ", decoded)
    
    # вытаскиваем ключи и значения из блока 'text'    
    for key, value in text_json.items():
      #print (key,": ", value)
      
      # ф-ция замены текста
      replaceText(key, value)
      
    # сохранить документ
    document.storeAsURL(url+new_file,())
    print("Сохранено в ",url+new_file )
      

# не удалось распарсить json
except (ValueError, KeyError, TypeError):
    print ("Ошибка: JSON format error")
############# end json



sys.exit()
