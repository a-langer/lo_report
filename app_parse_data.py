# -*- coding: utf-8 -*-
# this is module parse json or xml

# module parse json
import json
# bind to libreoffice module
from app_rununo import *

host     = "localhost"
port     = 2002
url      = "file://" + os.path.dirname(os.path.abspath(__file__)) + "/rununo/"

# coonect to libreoffice
desktop = unoConnect(host, port)

def parseData(dataType, dataMap):
    try:
        decoded = json.loads(dataMap)
        #print ("JSON parsing example: "+dataType) #debug
    except Exception:
        print("Error: JSON format error!") #debug
        listErr = {
                    'Message': 'JSON format error!',
                    'Type': dataType,
                    'Data': dataMap
                  }
        return respError(status=500, indent=1, sort_keys=None, Error=listErr)
        
    else:
        if ('template' in decoded):
            template = decoded['template']
            #print('template: '+ template) #debug
            try:
                # open template
                document = unoOpen(desktop, url, template) 
            except Exception:
                print("Could not open the template: "+url+template ) #debug
                listErr = {
                            'Message': 'Could not open the template!',
                            'File': template,
                            'Path': url
                          }
                return respError(status=500, sort_keys=False, Error=listErr)
            else:
                if ('outformat' in decoded):
                    outformat = decoded['outformat']
                    print('outformat: '+ outformat) #debug
                else: # сделай else для всех проверок
                    print ("outformat none")
                    return("outformat none")
                if ('text' in decoded):
                    text_json = decoded['text'] 
                    # func replace text
                    replaceText(document, text_json.items())
                if ('placeholder'in decoded):
                    placeholder_json = decoded['placeholder']
                    # func replace placeholder
                    # print ('replace placeholder items !!!') #debug
                if ('input'in decoded):
                    input_json = decoded['input'] 
                    # func replace input
                    # print ('replace input items !!!') #debug
                if ('userfield'in decoded):
                    userfield_json = decoded['userfield'] 
                    # func replace userfield
                    # print ('replace userfield items !!!') #debug
                # save templates
                return unoSave(document, url, outformat)
        else:
            print('This json item not used!') #debug
            listErr = {
                        'Message': 'This json item not used!',
                        'Json': str(decoded.items()),
                        'Path': 'url'
                      }
            return respError(status=500, sort_keys=False, Error=listErr)