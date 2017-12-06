# -*- coding: utf-8 -*-

from sqlhelper import SqlHelper
import config
import csv

if __name__ == '__main__':

    csvFile1 = open('user_recipe.csv','w')
    csvFile2 = open('recipe_source.csv','w')
    writer1 = csv.writer(csvFile1)
    writer1.writerow(['user_id', 'item_id'])
    writer2 = csv.writer(csvFile2)
    writer2.writerow(['recipe_id', 'source_id'])
    
    sql = SqlHelper()

    command = "SELECT user_id, item_id FROM {}".format(config.item_list_table)
    data = sql.query(command)

    for i, recipe in enumerate(data):
        writer1.writerow([recipe[0], recipe[1]])

    csvFile1.close()

    command = "SELECT recipe_id, source_id FROM {}".format(config.item_detail_table)
    data2 = sql.query(command)

    for i, source in enumerate(data2):
        writer2.writerow([source[0], source[1]])

    csvFile2.close()    

    
