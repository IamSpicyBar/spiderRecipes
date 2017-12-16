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
