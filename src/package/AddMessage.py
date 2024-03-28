#! /usr/bin/python
# -
# *- coding: utf-8 -*-
"""
WEB SCRAPING 
Date: '24 MAR 2024'
Update: '24 MAR 2024'
Author: Marco De Stavola '
"""

class AddMessage():
    def __init__(self,MESSAGE,EXPORT_FILE=None,MODE=None):
        self.MESSAGE                = MESSAGE
        if EXPORT_FILE is not None:
            self.EXPORT_FILE            = EXPORT_FILE
        if MODE is not None:
            self.MODE                   = MODE

    def AddMessageAndLogFile(self):
        with open(self.EXPORT_FILE, self.MODE) as f:
            print(self.MESSAGE, file=f)