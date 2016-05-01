"""this module makes the connection to fenixedu information and ScheduleMaker"""

import webbrowser
from datetime import datetime
import fenixedu


class Login():
    """ Login - asks authorization from user and his code"""

    def __init__(self):
        config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')

        self.client = fenixedu.FenixEduClient(config)
        self.year = datetime.now().hour

        url = self.client.get_authentication_url()

        webbrowser.open_new(url)

        code = input("please insert the code that is presented to you on the browser:")
        self.user = self.client.get_user_by_code(code)

    def getClient(self):
        """returns login's client"""
        return self.client

    def getUser(self):
        """returns login's user"""
        return self.user

    def getCoursesUrls(self):
        """ get courses list of urls and of it's ids """
        data = self.client.get_person_courses(self.user)
        urls = []
        ids = []
        for i in range(len(data['enrolments'])):
            urls += [data['enrolments'][i]['url']]
            ids += [data['enrolments'][i]['id']]

        return (urls, ids)

    def getDegrees(self):
        """ returns a tuple consisting of offered degrees and it's ids """
        data = self.client.get_degrees()
        degrees = []
        ids = []
        for i in range(len(data)):
            degrees += [data[i]['name']]
            ids += [data[i]['id']]

        return (degrees, ids)
