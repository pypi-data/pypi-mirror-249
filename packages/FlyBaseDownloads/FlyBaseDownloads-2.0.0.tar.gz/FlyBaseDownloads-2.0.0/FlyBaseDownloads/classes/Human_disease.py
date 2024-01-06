#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 18:34:38 2023

@author: usuario
"""

from FlyBaseDownloads.downloads.Downloads import Downloads 

class Human_disease():
    
    def __init__(self, main_url, cred):
        self.cred = cred
        self.main_url = main_url
        self.gen_url = 'human_disease/'
        self.header = None
        
    def get(self):
        
        url = self.main_url + self.gen_url + self.un_url
        downloads = Downloads(url, self.cred)
        
        return downloads.get(self.header)
        
    def Disease_model_annotations(self):
        self.gen_url = 'human_disease/'
        self.un_url = 'disease_model_annotations_fb_*.tsv.gz'
        self.header = 4
        return self.get()
    
    def Human_Orthologs(self):
        self.gen_url = 'orthologs/'
        self.un_url = 'dmel_human_orthologs_disease_fb_*.tsv.gz'
        self.header = 3
        return self.get()