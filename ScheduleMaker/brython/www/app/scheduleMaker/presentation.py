""" Presentation """

from login import Login
import sys
import logging
from pprint import pprint
from easygui import ynbox, choicebox
from datetime import datetime


class Presentation:
    """ class responsible for the presentation """

    def __init__(self):
        self.log = Login()
        self.user = self.log.getUser()
        self.client = self.log.getClient()
        logger = logging.getLogger()

        self.degrees_names, self.degrees_ids = self.log.getDegrees()
        data = self.log.client.get_person(self.log.user)
        self.degree_name = data['roles'][0]['registrations'][0]['name']
        self.degree_id = self.degrees_ids[self.degrees_names.index(self.degree_name)]
        logger.info("degree_name: {0}".format(self.degree_name))

        self.loop()

    def loop(self):
        """ Presentation loop"""
        # while 1:

        msg = "Are you already registered in this year courses?"
        registered = ynbox(msg)
        if registered:
            self.runUserIsRegistered()
        else:
            self.runUserIsNotRegistered()

        # msg = "Do you want to continue?"
        # title = "Please Confirm"
        # if ccbox(msg, title):     # show a Continue/Cancel dialog
        #     pass  # user chose Continue
        # else:
        #     sys.exit(0)           # user chose Cancel

    def runUserIsRegistered(self):
        ''' Flow of action when user is registered'''
        self.courses_urls, self.courses_ids = self.log.getCoursesUrls()
        pprint(self.courses_urls)


    def runUserIsNotRegistered(self):
        ''' Flow of action when user is not registered'''
        year = datetime.now().year
        choices = []
        for semester in ("1 Semestre ", "2 Semestre "):
            choices += [semester + "{0}/{1}".format(str(year), str(year+1))]
        for semester in ("1 Semestre ", "2 Semestre "):
            choices += [semester + "{0}/{1}".format(str(year-1), str(year))]

        semester = choicebox("Which semester do you want to search?", choices=choices)



    def changeDegree(self):
        """ Change degree option"""
        self.degree_name = choicebox("Which degree are you taking?", "", choices=self.degrees_names)
        self.degree_id = self.degrees_ids[self.degrees_names.index(self.degree_name)]


if __name__ == '__main__':
    Presentation()
