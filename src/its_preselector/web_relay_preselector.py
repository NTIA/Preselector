from its_preselector.preselector import Preselector
import requests


class WebRelayPreselector(Preselector):

    def set_rf_path(self, i):
        key = str(i)
        if key in self.config:
            switches = self.config[str(i)].split(',')
            if self.base_url:
                for i in range(len(switches)):
                    command = self.base_url + switches[i]
                    print(command)
                    requests.get(command)
        else:
            raise Exception("RF path " + key + " configuration does not exist.")
