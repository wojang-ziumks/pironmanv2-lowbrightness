
import requests
from utils import log

class HomeAssistantSupervisorAPI:

    def __init__(self, url, token):
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }


    def get(self, endpoint):
        try:
            url = f"{self.url}{endpoint}"
            log(msg=f"home assistant get: {url}", level='DEBUG')
            r = requests.get(url, headers=self.headers)
            log(msg="home assistant got: " + r.text, level='DEBUG')
            return r.json()
        except Exception as e:
            log(msg="home assistant get error: " + e, level='DEBUG')


    def get_ip(self):
        IPs = {}
        data = self.get("network/info")
        interfaces = data["data"]["interfaces"]
        for interface in interfaces:
            name = interface['interface']
            ip = interface['ipv4']['address']
            if len(ip) == 0:
                continue
            ip = ip[0]
            if ip == '':
                continue
            if "/" in ip:
                ip = ip.split("/")[0]
            IPs[name] = ip
        return IPs

    def shutdown(self):
        '''shutdown homeassistant host'''
        log(msg="Shutdown home assistant host", level='DEBUG')
        self.get("host/shutdown")

