#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import settings
from pymongo import Connection
from LinkedInParser import LinkedinPageParser

class LinkedinCrawler:

    def __init__(self):
        self.name = 'LinkedinCrawler'
        self.region = None
        self.url = None
        self.delay = None

        # Private Property
        self.dataParser = None

    def get_data(self):

        if not self.dataParser:
            self.dataParser = LinkedinPageParser()

        # Feed the parser
        self.dataParser.data = self._get_page()

        # Check if the person work in the target regions
        if self.region:
            page_region = self.dataParser.get_region()
            if page_region not in self.region:
                print 'Person not in target region, no data return, no further network return.'
                return None

        print 'Getting data from :', self.url
        print
        education = self.dataParser.get_education_info()
        work = self.dataParser.get_work_info()
        skills = self.dataParser.get_skill_info()
        network = self.dataParser.get_network()

        p_dict = {'edu': education,
                  'work': work,
                  'skills': skills,
                  'network': network,
                  'url': self.url}
        return p_dict

    def _get_page(self):

        if self.url:
            r = requests.get(self.url, timeout=30)
            return r.text

        else:
            print self.name, ' Method: _get_page: Error - No url is given for page'


if __name__ == '__main__':


    con = Connection()
    db = con.linkedinDB
    profile = db.profile

    if profile:
        counter = profile.count()

    seeds = settings.SEED_PROFILES # seed queue to start with
    jobs = db.job  # job queue
    dones = db.done # finished jobs

    c = LinkedinCrawler()
    c.region = ['Hong Kong'] #only crawl people from Hong Kong

    while seeds or jobs.count():

        # start with a seed profile if job queue is empty
        if not jobs.count():
            url = seeds.pop(0)

            # Check whether seed is in job queue or finished jobs already
            print 'Seed url = ', url
            url_trim = url.split('?')[0]
            in_jobs = jobs.find({'url': {'$regex': url_trim}}).limit(1).count()
            in_dones = dones.find({'url': {'$regex': url_trim}}).limit(1).count()

            if in_jobs or in_dones:
                print 'Seed has already been used.'
                continue
            else:
                print 'Seed is okay. Ready for crawling.'
                pass

        else:
            first_job = jobs.find()[0:1][0]
            url = first_job['url']
            jobs.remove({'_id': first_job['_id']})

        now = str(datetime.datetime.now())
        c.url = url
        dones.insert({'url': url, 'timestamp': now})

        try:
            data = c.get_data()
        except:
            print 'Connection error for ', url
            continue


        if data:

            data['timestamp'] = now
            network = data['network']

            # add new profiles into job queue
            if network:
                for n in network:
                    in_jobs = jobs.find({'url': n}).limit(1).count()
                    in_dones = dones.find({'url': n}).limit(1).count()

                    if not in_jobs and not in_dones:
                        # print 'Found new job: ', n
                        jobs.insert({'url': n, 'timestamp': now})

            # add profile to db only when education and work experience are present
            if data['edu'] and data['work']:
                profile.insert(data)
                counter += 1
                print 'Profile collected: ', counter
