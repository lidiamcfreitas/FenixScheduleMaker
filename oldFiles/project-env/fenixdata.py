import fenixedu
import urlparse
import urllib
import urllib2
import webbrowser

config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')

client = fenixedu.FenixEduClient(config)

url = client.get_authentication_url()

print(client.get_authentication_url())

webbrowser.open('https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=851490151333916&redirect_uri=http://web.ist.utl.pt/ist178559')
#parsed = urlparse.urlparse(url)
#print urlparse.parse_qs(parsed.query)['code']

#user = client.get_user_by_code(CODE)
