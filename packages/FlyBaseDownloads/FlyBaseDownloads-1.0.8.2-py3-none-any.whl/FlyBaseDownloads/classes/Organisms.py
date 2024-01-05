#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:33:17 2023

@author: usuario
"""

from FlyBaseDownloads.downloads.Downloads import Downloads 

class Organisms():
    
    def __init__(self, main_url, cred):
        self.cred = cred
        self.main_url = main_url
        self.org_url = 'species/organism_list_fb*.tsv.gz'
        self.header = 4
        
    
    def Species_list(self):
        
        url = self.main_url + self.org_url
        
        downloads = Downloads(url, self.cred)
        
        return downloads.get(self.header)
