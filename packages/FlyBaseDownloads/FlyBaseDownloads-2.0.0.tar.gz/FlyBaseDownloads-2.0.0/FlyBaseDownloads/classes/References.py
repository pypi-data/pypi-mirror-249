#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:35:38 2023

@author: usuario
"""

from FlyBaseDownloads.downloads.Downloads import Downloads 

class References():
    
    def __init__(self, main_url, cred):
        self.cred = cred
        self.main_url = main_url
        self.org_url = 'references/fbrf_pmid_pmcid_doi_fb*.tsv.gz'
        self.header = 2
        
    
    def FBrf_PMid_PMCid_doi(self):
        
        url = self.main_url + self.org_url
        
        downloads = Downloads(url, self.cred)
        
        df = downloads.get(self.header)
        
        return df.iloc[1:, :]
