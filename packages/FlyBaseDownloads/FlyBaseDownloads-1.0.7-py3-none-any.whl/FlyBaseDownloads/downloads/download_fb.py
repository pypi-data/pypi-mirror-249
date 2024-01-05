#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 12:30:45 2024

@author: javicolors
"""

import pandas as pd
import gzip
import re
import csv

class Download_fb():
    
    def open_fb(self, file_path,start_line, columns):
        a = []

        if re.search(r'gz', file_path):
            
            try:
                with gzip.open('../' + file_path, 'rt') as file:
                    df = csv.reader(file, delimiter='\t')
                    a.append(pd.DataFrame(df))
            
                df = a[0]
                
                df = df.iloc[start_line:, :-2]
                df.columns = columns
              

                return (df)
                            
            except:
                    print('Failed to download the file') 