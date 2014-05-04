#!/usr/bin/env python
# -*- coding: utf-8 -*-

# We look for five aspects of a profile:
# 1. education
# 2. work experience
# 3. skill set
# 4. people also viewed (used as next crawling target)
# 5. region where the person work at

from pattern import web
import HTMLParser

class LinkedinPageParser:

    def __init__(self):
        self.name = 'LinkedinPageParser'
        self.data = None

    def get_education_info(self):

        if self.data:

            dom = web.Element(self.data)
            h = HTMLParser.HTMLParser()

            # Get Education
            education_section = dom.by_tag('div#profile-education')

            if education_section:
                education_section = education_section[0].by_tag('div.content vcalendar')[0].by_tag('div.position')
            else:
                print 'No education profile found'
                return None #Return None if no education is available

            education_hist = []
            for edu in education_section:
                school = u''
                degree = u''
                major = u''
                period_start = u''
                period_end = u''

                school_wrapper = edu.by_tag('h3.summary fn org')[0].children
                if len(school_wrapper) == 1:
                    school = str(edu.by_tag('h3.summary fn org')[0].children[0]).strip()
                else:
                    school = edu.by_tag('h3.summary fn org')[0].children[1].content.strip()

                program_details = edu.by_tag('h4.details-education')
                if program_details:
                    program_details = program_details[0]
                #print program_details

                degree_section = program_details.by_tag('span.degree')
                if degree_section:
                    degree = degree_section[0].content.strip()

                major_section = program_details.by_tag('span.major')
                if major_section:
                    major = major_section[0].content.strip()

                period_section = edu.by_tag('p.period')
                if period_section:
                    period_details = period_section[0].by_tag('abbr')

                    if len(period_details) == 2 :
                        period_start = period_details[0].content.strip()
                        period_end = period_details[1].content.strip()
                    elif len(period_details) == 1:
                        period_end = period_details[0].content.strip()

#                 print
#                 print 'School: ', h.unescape(school)
#                 print 'Degree: ', h.unescape(degree)
#                 print 'Major: ', h.unescape(major)
#                 print 'Period_start: ', period_start
#                 print 'Period_end: ', period_end

                school = h.unescape(school)
                degree = h.unescape(degree)
                major = h.unescape(major)
                edu_dict = {'school': school,
                            'degree': degree,
                            'major': major,
                            'period_start': period_start,
                            'period_end': period_end}

                education_hist.append(edu_dict)
            return education_hist

        else:
            print self.name, ' get_education_info Error - no page given.'


    def get_work_info(self):

        if self.data:

            dom = web.Element(self.data)
            h = HTMLParser.HTMLParser()

            # Get Work
            work_section = dom.by_tag('div#profile-experience')

            if work_section:
                work_section = work_section[0].by_tag('div.content vcalendar')[0].by_tag('div.position')
            else:
                print 'No work profile found'
                return None #Return None if no work profile is available

            work_hist = []
            for work in work_section:
                title = u''
                company = u''
                period_start = u''
                period_end = u''
                location = u''
                industry = u''

                title_section = work.by_tag('span.title')
                if title_section:
                    title = title_section[0].content.strip()

                company_section = work.by_tag('span.org summary')
                if company_section:
                    company = company_section[0].content.strip()


                period_section = work.by_tag('p.period')
                if period_section:
                    period_details = period_section[0].by_tag('abbr')

                    if len(period_details) == 2 :
                        period_start = period_details[0].content.strip()
                        period_end = period_details[1].content.strip()
                    elif len(period_details) == 1:
                        period_end = period_details[0].content.strip()

                location_section = work.by_tag('span.location')
                if location_section:
                    location = location_section[0].content.strip()

                industry_section = work.by_tag('p.organization-details')
                if industry_section:
                    industry = industry_section[0].content.strip().split(';')[-1].strip()

#                 Uncomment if you want to log information during parsing
#                 print 'Title: ', h.unescape(title)
#                 print 'Company: ', h.unescape(company)
#                 print 'Period_start: ', period_start
#                 print 'Period_end: ', period_end
#                 print 'Location: ', location
#                 print 'Industry: ', industry

                title = h.unescape(title)
                company = h.unescape(company)
                location = h.unescape(location)
                industry = h.unescape(industry)

                work_dict = {'title': title,
                            'company': company,
                            'location': location,
                            'industry': industry,
                            'period_start': period_start,
                            'period_end': period_end}

                work_hist.append(work_dict)
            return work_hist

        else:
            print self.name, ' get_work_info Error - no page given.'

    def get_skill_info(self):

        if self.data:

            dom = web.Element(self.data)
            h = HTMLParser.HTMLParser()

            skills_section = dom.by_tag('ol#skills-list')
            if skills_section:

                skills_list = []
                for skill in skills_section[0].by_tag('span.jellybean'):
                    skills_list.append(h.unescape(skill.content.strip()))

                return skills_list

        else:
            print self.name, ' get_skill_info Error - no page given.'

    def get_network(self):

        if self.data:

            dom = web.Element(self.data)
            network_section = dom.by_tag('div.leo-module mod-util browsemap')

            if network_section:

                network = []
                for p in network_section[0].by_tag('li'):
                    network.append(p.by_tag('a')[0].attrs['href'].strip())

                return network

        else:
            print self.name, ' get_network Error - no page given'

    def get_region(self):

        if self.data:

            dom = web.Element(self.data)
            h = HTMLParser.HTMLParser()

            locality_section = dom.by_tag('span.locality')
            if locality_section:
                region = h.unescape(locality_section[0].content.strip())
                return region
        else:
            print self.name, 'get_region Error - no page given'
