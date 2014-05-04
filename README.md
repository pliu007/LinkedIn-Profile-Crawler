LinkedIn-Profile-Crawler
========================

Description
-----------
It is a quick and dirty implementation of a LinkedIn profile crawler written in Python, using Pattern as HTML parser and MongoDB as local storage. Data collected includes a person's education profile, work experience and skills set.

Requirements of 3rd party libraries
-----------------------------------
*   [Pattern] (http://www.clips.ua.ac.be/pattern)
*   [Requests] (http://docs.python-requests.org/en/latest/)
*   [MongoDB] (https://www.mongodb.org/)

Usage
-----
1. Run a mongoDB server (http://docs.mongodb.org/manual/tutorial/manage-mongodb-processes/)
2. Set the region where you want to crawl in settings.py, e.g. Hong Kong, Taiwan, etc.
3. Get a few seed public profiles from LinkedIn and add them to settings.py, for example:

        ```python
        # settings.py

        CRAWL_REGIONS = ['Hong Kong']
        SEED_PROFILES = ['https://www.linkedin.com/in/simonsiuhk']
        ```
4. Run LinkedInCrawler.py
