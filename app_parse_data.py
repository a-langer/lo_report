# -*- coding: utf-8 -*-
# this is module parse json or xml

# module parse json
import json
# bind to libreoffice module
from app_rununo import *

host     = "localhost"
port     = 2002
#url      = "file:///C:/Users/langer/script/LO_REPORT/rununo/"
url      = "file://" + os.path.dirname(os.path.abspath(__file__)) + "/rununo/"
#url      = "file:///home/admin1/Загрузки/LO_REPORT_0.8/rununo/"
# coonect to libreoffice
desktop = unoConnect(host, port)

def parseData(dataType, dataMap):
    try:
        decoded = json.loads(dataMap)
        #print ("JSON parsing example: "+dataType)
    except Exception:
        print("Error: JSON format error!")
        listErr = {
                    'Message': 'JSON format error!',
                    #'Message': 'Неправильный формат Json!',
                    'Type': dataType,
                    'Data': dataMap
                  }
        return respError(status=500, indent=1, sort_keys=None, Error=listErr)
        
    else:
        if ('template' in decoded):
            template = decoded['template']
            #print('template: '+ template)
            try:
                document = unoOpen(desktop, url, template) # open template
            except Exception:
                print("Не удалось открыть шаблон: "+url+template )
                listErr = {
                            'Message': 'Could not open the template!',
                            'File': template,
                            'Path': url
                          }
                return respError(status=500, sort_keys=False, Error=listErr)
            else:
                if ('outformat' in decoded):
                    outformat = decoded['outformat']
                    print('outformat: '+ outformat)
                if ('text' in decoded):
                    text_json = decoded['text'] 
                    # replace text
                    replaceText(document, text_json.items())
                if ('placeholder'in decoded):
                    text_json = decoded['placeholder']
                    # replace placeholder
                    print ('replace placeholder items !!!')
                if ('input'in decoded):
                    text_json = decoded['input'] 
                    # replace input
                    print ('replace input items !!!')
                if ('userfield'in decoded):
                    text_json = decoded['userfield'] 
                    # replace userfield
                    print ('replace userfield items !!!')
                # save templates
                return unoSave(document, url, outformat)
        else:
            print('This json item not used!')
            listErr = {
                        'Message': 'This json item not used!',
                        'File': decoded.items(),
                        'Path': 'url'
                      }
            return respError(status=500, sort_keys=False, Error=listErr)