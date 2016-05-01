""" Presentation """

from login import Login
import sys
import logging
from easygui import ynbox, ccbox, choicebox



log = Login()
user = log.getUser()
client = log.getClient()
logger = logging.getLogger()

class Presentation:
    """ class responsible for the presentation """

    def __init__(self):
        self.degrees_names, self.degrees_ids = log.getDegrees()
        data = log.client.get_person(log.user)
        self.degree_name = data['roles'][0]['registrations'][0]['name']
        self.degree_id = self.degrees_ids[self.degrees_names.index(self.degree_name)]
        logger.info("degree_name: {0}".format(self.degree_name))


        self.loop()

    def loop(self):
        """ Presentation loop"""
        while 1:

            msg = "Are you already registered in this year courses?"
            registered = ynbox(msg)
            if registered:
                self.runUserIsRegistered()
            else:
                self.runUserIsNotRegistered()

            msg = "Do you want to continue?"
            title = "Please Confirm"
            if ccbox(msg, title):     # show a Continue/Cancel dialog
                pass  # user chose Continue
            else:
                sys.exit(0)           # user chose Cancel

    def runUserIsRegistered(self):
        ''' Flow of action when user is registered'''
        pass

    def runUserIsNotRegistered(self):
        ''' Flow of action when user is not registered'''

        semester = choicebox("Which semester do you want to search?", choices=["1st", "2nd"])


    def changeDegree(self):
        """ Change degree option"""
        self.degree_name = choicebox("Which degree are you taking?", "", choices=self.degrees_names)
        self.degree_id = self.degrees_ids[self.degrees_names.index(self.degree_name)]
