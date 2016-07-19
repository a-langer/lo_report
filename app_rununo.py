# -*- coding: utf-8 -*-
# this is module bind to LibreOffice
import os
import uno # module libreoffice-uno
import json
from json import dumps
import collections

# flask module
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, make_response, abort, jsonify
app = Flask(__name__)

# return http status error
def respError(status=200, indent=2, sort_keys=False, **kwargs):
    resp = make_response(dumps(dict(**kwargs), ensure_ascii=False, indent=indent, sort_keys=sort_keys).encode('utf8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp.headers['mimetype'] = 'application/json'
    resp.headers['Content-Disposition'] = 'filename=Error.json'
    resp.status_code = status
    return resp
    
# return report file
def respReport(root, new_file):
    resp = send_from_directory(root, new_file, as_attachment=True)
    return resp

def unoConnect(host, port):
    ctx = uno.getComponentContext()
    srv_manager = ctx.getServiceManager() 
    resolver = ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", ctx)
    context = resolver.resolve("uno:socket,host="+ str(host) +",port="+ str(port) +";urp;StarOffice.ComponentContext")
    desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    return desktop
   
def unoOpen(desktop, url, file):
    return desktop.loadComponentFromURL(url+file, "_blank", 0, ())
"""
    try:
        return desktop.loadComponentFromURL(url+file, "_blank", 0, ())
    except Exception:
        print("Не удалось открыть шаблон: "+url+file )
        listErr = {
                    'Message': 'Could not open the template!',
                    'File': file,
                    'Path': url
                  }
        return respError(status=500, sort_keys=None, Error=listErr)
""" 
 
def unoSave(document, url, new_file):
    # сохранить заполненный шаблон
    try:
        document.storeAsURL(url+new_file,())
        # закрыть сохраненный шаблон
        #document.dispose()
    except Exception:
        # закрыть сохраненный шаблон
        document.dispose()
        print ("Не удалось сохранить файл: "+new_file)
        #return ("Не удалось сохранить файл: "+new_file)
        listErr = {
                    'Message': 'Unable to save file!',
                    'File': new_file,
                    'Path': url
                  }
        return respError(status=500, sort_keys=False, Error=listErr)
                           
    else:
        print("Сохранено в "+url+new_file )
        # return report as file
        #root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rununo") + "\\"
        root = "file://" + os.path.dirname(os.path.abspath(__file__)) + "/rununo/"
        #root = "file:///home/admin1/Загрузки/LO_REPORT_0.8/rununo/"
        return respReport(root, new_file)
        
def replaceText(document, text_json_items):
    # дескриптор замены текста
    replace_desc = document.createReplaceDescriptor()
    # вытаскиваем ключи и значения из блока 'text'    
    for key, value in text_json_items:
      #print (key,": ", value)
      # Текст для замены {{text}}
      replace_desc.setSearchString("{{"+str(key)+"}}")
      #print("Передано в UNO: ",key, value) # отладка

      find_iter = document.findFirst(replace_desc)
      while find_iter:
          find_iter.String = str(value) # в виде строки
          find_iter = document.findNext(find_iter.End, replace_desc) # заменяем текст
          if not find_iter: break # текст заменен