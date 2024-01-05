#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:09:21 2024

@author: javicolors
"""
import firebase_admin
from firebase_admin import credentials, auth
import os

class Authentication():
    
    def __init__(self):
        
        try: 
            firebase_admin.get_app()  

        except ValueError:
            json = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serviceAccountKey.json')
            cred = credentials.Certificate(json)
            firebase_admin.initialize_app(cred, {
                'databaseURL': "https://flybasedownloads-default-rtdb.firebaseio.com/"
            })
        
        

    def get_user(self, email):
        i = 0
        while(i < 3):
            try:
                try:
                    user = auth.create_user(email = email)
                    print("usuario creado")
                    return user.uid
                except:
                    user = auth.get_user_by_email(email=email)
                    print("usuario encontrado")
                    return user.uid
            except:
                print("email incorrecto")
                email = input("Ingrese su email")
                i += 1
        return None



        


