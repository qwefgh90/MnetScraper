__author__ = 'changwoncheo'
# -*- coding: utf-8 -*-
import os
import re
reobj_album = re.compile('\'(.*)\'')#앨범 정규식
reobj_filename = re.compile('/(\w*[.]\w*)$')#파일이름 정규식
category = {102:'발라드',103:'댄스',104:'랩_합합',105:'R&B_Soul',106:'록',107:'일렉트로니카',108:'트로트',109:'포크',110:'인디음악'}
