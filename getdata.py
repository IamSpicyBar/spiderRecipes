# -*- coding: utf-8 -*-

from sqlhelper import SqlHelper
import config
import csv
from googletrans import Translator

if __name__ == '__main__':

    translator = Translator()
    
    csvFile1 = open('user_recipe.csv','w')
    csvFile2 = open('recipe_source.csv','w')
    csvFile3 = open('recipe_name.csv','w')
    csvFile4 = open('source_name.csv','w')
    
    writer1 = csv.writer(csvFile1)
    writer1.writerow(['user_id', 'item_id'])
    writer2 = csv.writer(csvFile2)
    writer2.writerow(['recipe_id', 'source_id'])
    writer3 = csv.writer(csvFile3)
    writer3.writerow(['recipe_id', 'recipe_name'])
    writer4 = csv.writer(csvFile4)
    writer4.writerow(['source_id', 'source_name'])
    
    sql = SqlHelper()

    command = "SELECT user_id, item_id FROM {}".format(config.item_list_table)
    data = sql.query(command)

    for i, recipe in enumerate(data):
        writer1.writerow([recipe[0], recipe[1]])

    csvFile1.close()
        
    command = "SELECT item_id, name FROM {}".format(config.item_list_table)
    data1 = sql.query(command)

    for i, item in enumerate(data1):
 #       name_en = translator.translate(item[1]).text
        writer3.writerow([item[0], item[1].encode('utf8')])
    
    csvFile3.close()
  

    command = "SELECT recipe_id, source_id FROM {}".format(config.item_detail_table)
    data2 = sql.query(command)

    for i, source in enumerate(data2):
        writer2.writerow([source[0], source[1]])

    csvFile2.close()

    command = "SELECT source_id, source_name FROM distinct_name"
    data3 = sql.query(command)
    

    for i, source in enumerate(data3):
        if source[0] != 5252 and source[0] != 5451:
            source_en = translator.translate(source[1]).text
        if source[0] == 1227:
            source_en = 'chicken gizzards'
        if source[0] == 1516:
            source_en = 'water bamboo'
        if source[0] == 2348:
            source_en = 'salted black beans'
        if source[0] == 2459:
            source_en = 'sea salt'
        if source[0] == 2629:
            source_en = 'beef brisket slice'
        if source[0] == 2688:
            source_en = 'sea urchin'
        if source[0] == 5252:
            source_en = 'pork loin'
        if source[0] == 5451:
            source_en = 'dried fruit'
            
        print(source_en)
        writer4.writerow([source[0], source_en])

    csvFile4.close()       
