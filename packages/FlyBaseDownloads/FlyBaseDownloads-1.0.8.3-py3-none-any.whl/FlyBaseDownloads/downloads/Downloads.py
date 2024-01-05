#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:04:19 2023

@author: javiera.quiroz
"""


import pandas as pd
import fnmatch
from ftplib import FTP
import re
import os

from .download_tsv import Download_tsv
from .download_json import Download_json
from .download_obo import Download_obo
from .download_fb import Download_fb

from FlyBaseDownloads.utilities.database import RTD


class Downloads(Download_tsv, Download_json,
                Download_obo, Download_fb):
    def __init__(self, url, cred):
        
        self.url = url
        self.cred = cred
        
    def download_file(self):
        
        url = self.url
        
        ftp = FTP(url.split('/')[2])
        ftp.login()
        directory_path = '/'.join(url.split('/')[3:-1])
        
        ftp.cwd(directory_path)
        
        remote_files = ftp.nlst()
        
        filtered_files = list(fnmatch.filter(remote_files, url.split('/')[-1]))
        
        files = []
        for file in filtered_files:
            file_path = '../' + file
            if not os.path.exists(file):
                with open(file_path, 'wb') as local_file:
                    ftp.retrbinary('RETR ' + file, local_file.write)
        
                files.append(file)
            else:
                files.append(file)
        
        ftp.quit()
        if len(files) > 0:
            file = files[0]
            rtd = RTD(self.cred)
            rtd.save_reg(file)
            return file
        else:
            print('Failed to download the file')
            return None
        
    
    def get(self, header = None):
        
        file = None
        
        try:
            if self.cred is not None:
                file = self.download_file()
            else:
                print("Try again with correct email")
        except:
            print('Failed to download the file') 
        patron = r"##?\s?\w+"
        
        def df_r(df):
            if re.search(r"FB\w{9}", df.columns[0]):
                df_columns = pd.DataFrame(df.columns).T

                df.columns = range(len(df.columns))
                
               
                df = pd.concat([df_columns, df], ignore_index=True, axis = 0)
            
            if re.search(patron, df.iloc[-1,0]):
                df = df.iloc[:-1, :]
            
            return df
        
        
        if file is not None:
            if re.search('.obo', self.url):
                return super().open_obo(file)
            elif re.search('.json', self.url):
                try:
                    return df_r(super().open_file_json(file))
                    
                except:
                    try:
                        df = super().open_file_json(file)
                        df = pd.concat([df.drop(['driver'], axis=1), df['driver'].apply(pd.Series)], axis=1)

                        df = df.replace({None: pd.NA})
                        return df_r(df)
                    except:
                        return super().open_file_json(file)
                    
            else:
                return df_r(super().open_file_tsv(file, header))
        
    
