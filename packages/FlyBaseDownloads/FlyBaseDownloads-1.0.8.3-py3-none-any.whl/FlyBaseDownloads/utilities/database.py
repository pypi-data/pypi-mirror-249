#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 22:30:36 2024

@author: javicolors
"""

import firebase_admin
from firebase_admin import credentials, db
import random
import os



class RTD():
    
    def __init__(self, uid):
        self.uid = uid
        try:
            # Verifica si ya existe una aplicación de Firebase
            firebase_admin.get_app()
        except ValueError:
            # Si no existe, inicializa la aplicación
            cred = credentials.Certificate("../serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': "https://flybasedownloads-default-rtdb.firebaseio.com/"
            })
    
    def save_reg(self, file_path):
        ref = db.reference("Downloads")
        a = random.randint(10000, 99999)
        registro = {
            a: str(file_path)
            
        }
        ref.child(str(self.uid)).update(registro)
        
    def def_reg(self):
        ref = db.reference("Downloads/" + self.uid)
        datos_user = ref.get()
        if datos_user:
        # Itera sobre cada usuario y sus datos
            for id_, dato in datos_user.items():
                try:
                    os.remove("../" + dato)
                except:
                    pass
            ref.delete()
        
        
