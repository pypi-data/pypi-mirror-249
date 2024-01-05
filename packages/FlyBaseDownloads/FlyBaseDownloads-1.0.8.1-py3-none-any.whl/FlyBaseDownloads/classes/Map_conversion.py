#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 17:37:56 2023

@author: usuario
"""

from FlyBaseDownloads.downloads.Downloads import Downloads 


class Map_conversion():
    
    def __init__(self, main_url, cred):
        self.cred = cred
        self.main_url = main_url
        self.go_url = 'ontologies/'
        self.header = None
        
    def get(self):
        
        url = self.main_url + self.go_url + self.un_url
        downloads = Downloads(url, self.cred)
        
        return downloads.get(self.header)
        
    def FBbt(self):
        self.un_url = 'fly_anatomy.obo.gz'
        return self.get()
    
    def FBdv(self):
        self.un_url = 'fly_development.obo.gz'
        return self.get()
    
    def FBcv(self):
        self.un_url = 'flybase_controlled_vocabulary.obo.gz'
        return self.get()
    
    def FBsv(self):
        self.un_url = 'flybase_stock_vocabulary.obo.gz'
        return self.get()
