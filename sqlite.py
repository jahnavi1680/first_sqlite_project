# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 09:16:13 2024

@author: jp042
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sqlite3
conn = sqlite3.connect('reviews.db')
c = conn.cursor()

#dataset = pd.read_csv("C:/Users/jp042/Downloads/Restaurant_Reviews.tsv",
                      #delimiter='\t', quoting=3)

#res = pd.read_csv("C:/Users/jp042/Downloads/result.csv")

#table_name = 'Results'  # Specify the table name
#res.to_sql(table_name, conn, if_exists='replace', index=False)

c.execute('''select profession, sum(Liked=1) as like, sum(Liked=0) as dislike , count(*) as cnt
          from Results
          group by profession''')
          
rows = c.fetchall()
columns = [description[0] for description in c.description]
gbyprof = pd.DataFrame(rows, columns=columns)

c.execute('''select gender,sum(Liked=1) as like, sum(Liked=0) as dislike , count(*) as cnt
          from Results
          group by gender''')
          
rows = c.fetchall()
columns = [description[0] for description in c.description]
gbygender = pd.DataFrame(rows, columns=columns)

c.execute('''select sum(Liked=1) as like, sum(Liked=0) as dislike, 
          'child' as category, count(*) as cnt
          from Results 
          where age between 0 and 15
          union 
          select sum(Liked=1) as like, sum(Liked=0) as dislike, 
                    'teen' as category, count(*) as cnt
                    from Results 
                    where age between 15 and 30
          union 
          select sum(Liked=1) as like, sum(Liked=0) as dislike, 
                    'midlle' as category, count(*) as cnt
                    from Results 
                    where age between 30 and 60
          union
          select sum(Liked=1) as like, sum(Liked=0) as dislike, 
                    'old' as category, count(*) as cnt
                    from Results 
                    where age between 60 and 100
          ''')
          
rows = c.fetchall()
columns = [description[0] for description in c.description]
gbyage = pd.DataFrame(rows, columns=columns)

