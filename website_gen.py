#!/usr/bin/python3
import os,sys
#生成网页的工具
title='Fit Server File Browser'
def website_gen(directory):
    htmlfile=f'''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
    </head>
    <body>
    <h1>Index of {directory}</h1>
    <hr>\n
    '''
    filelist=os.listdir(directory)
    filelist.insert(0,'..')
    for file in filelist:
        if os.path.isdir(directory+file):
            htmlfile+=f'''\n<a href="{file}/">{file}/</a><br>\n'''
        else:
            htmlfile+=f'''\n<a href="{file}">{file}</a><br>\n'''
    htmlfile+='''</body>\n</html><hr><p>Fit Http Server Alpha 1</p>'''
    return htmlfile



