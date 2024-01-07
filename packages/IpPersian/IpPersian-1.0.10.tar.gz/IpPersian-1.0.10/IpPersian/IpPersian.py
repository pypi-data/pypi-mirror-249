import requests


class IpPersian():
    def api_url(self, type='https'):
        if type == 'https':
            return "https://lssc.ir/api/ip/"
        elif type == 'http':
            return "http://lssc.ir/api/ip/"

    def __init__(self, ip=None):
        try:
            get_ip = ""
            if ip != None:
                get_ip = ip
            keys = {'ip': get_ip}
            result = requests.post(url=self.api_url(), params=keys)
            self.ip_info = result.json()
        except:
            try:
                get_ip = ""
                if ip != None:
                    get_ip = ip
                keys = {'ip': get_ip}
                result = requests.post(
                    url=self.api_url(), params=keys, verify=False)
                self.ip_info = result.json()
            except:
                get_ip = ""
                if ip != None:
                    get_ip = ip
                keys = {'ip': get_ip}
                result = requests.post(
                    url=self.api_url(type='http'), params=keys)
                self.ip_info = result.json()
            else:
                result = None
                self.ip_info = {}

    def ip(self):
        try:
            return self.ip_info['query']
        except:
            return '0.0.0.0'

    def asn(self):
        try:
            return self.ip_info['asn']
        except:
            return None

    def asnName(self):
        try:
            return self.ip_info['asnName']
        except:
            return None

    def asnOrg(self):
        try:
            return self.ip_info['asnOrg']
        except:
            return None

    def city(self):
        try:
            return self.ip_info['city']
        except:
            return None

    def continent(self):
        try:
            return self.ip_info['continent']
        except:
            return None

    def country(self):
        try:
            return self.ip_info['country']
        except:
            return None

    def countryCode(self):
        try:
            return self.ip_info['countryCode']
        except:
            return None

    def isp(self):
        try:
            return self.ip_info['isp']
        except:
            return None

    def lat(self):
        try:
            return self.ip_info['lat']
        except:
            return None

    def lon(self):
        try:
            return self.ip_info['lon']
        except:
            return None

    def org(self):
        try:
            return self.ip_info['org']
        except:
            return None

    def region(self):
        try:
            return self.ip_info['region']
        except:
            return None

    def timezone(self):
        try:
            return self.ip_info['timezone']
        except:
            return None

    def utcOffset(self):
        try:
            return self.ip_info['utcOffset']
        except:
            return None

    def __str__(self):
        s = f"IP address : {self.ip()}\n"
        s += f"asn : {self.asn()}\n"
        s += f"asnName : {self.asnName()}\n"
        s += f"asnOrg : {self.asnOrg()}\n"
        s += f"city : {self.city()}\n"
        s += f"continent : {self.continent()} \t country : {self.country()} \t countryCode : {self.countryCode()}\n"
        s += f"isp : {self.isp()}\n"
        s += f"lat : {self.lat()} \t lon : {self.lon()}\n"
        s += f"org : {self.org()}\n"
        s += f"region : {self.region()}\n"
        s += f"timezone : {self.timezone()}\n"
        s += f"utcOffset : {self.utcOffset()}\n"
        return s
