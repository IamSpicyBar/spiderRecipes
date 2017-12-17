# spiderRecipes

Project catalog:

    recipesData/
        scrapy.cfg          //configuration file automatically created    
        singleton.py
        config.py           //Database configuration
        utils.py            //Help create log
        main.py             //Select and run spider here
        getdata.py          //Read from database and write csv files
        recipesData/
            //crawling setting files
            __init__.py
            items.py
            middlewares.py
            settings.py
            spiders/
                //spiders
                    __init__.py
                    user.py             //collect active user data
                    user_new.py         //collect random user data
                    recipe.py           //collect recipe list of each user
                    recipe_detail.py    //collect recipe details
        log/
            //log stored here


## How to run?
First change database configuration in config.py

Then run main.py, execute each Scrapy command one by one

Crawling speed is set in settings.py

If you want to output csv files, use getdata.py

The last part of getdata.py is to translate unique ingredients list to English, delete them
#### Created by Yichen, updated on 12/17/2017
