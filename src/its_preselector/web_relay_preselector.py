from its_preselector.preselector import Preselector
import requests


class WebRelayPreselector(Preselector):

    def set_rf_path_on(self, i):
        key = str(i)
        if key in self.config:
            switches = self.config[str(i)].split(',')
            for i in range(len(switches)):
                command = self.base_url + switches[i]
                print(command)
                requests.get(command)

    def set_source(self, key):
        switches = self.config[key].split(',')
        for i in range(len(switches)):
            command = self.config['WEB_RELAY']['base_url'] + switches[i]
            print(command)
            requests.get(command)
