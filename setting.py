__author__ = 'changwoncheo'
# -*- coding: utf-8 -*-
import logging
logging.basicConfig(filename='crawl.log',level=logging.DEBUG)
class NoParsingFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return not ('Starting' in msg or 'GET' in msg)
logger = logging.getLogger('Crawler')

requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.CRITICAL)    #로깅 되지 않도록


import os
import re
reobj_album = re.compile('\'(.*)\'')#앨범 정규식 (javascript('숫자'))
reobj_djIndex = re.compile(',\'(.*)\'')#앨범 정규식 (javascript('숫자','숫자'))
reobj_filename = re.compile('/(\w*[.]\w*)$')#파일이름 정규식
category = {102:'발라드',103:'댄스',104:'랩_합합',105:'R&B_Soul',106:'록',107:'일렉트로니카',108:'트로트',109:'포크',110:'인디음악'}
def tapNewlineStrip(str):
    return str.encode('utf-8').replace('\n','').replace('\t','')

def writeJson(fileName,dict):
    import json
    with open(fileName, 'w') as outfile:
        json.dump(dict, outfile, ensure_ascii = False, encoding = 'utf-8')