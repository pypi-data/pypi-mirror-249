import requests
class IpPersian():
        def api_url(self):
                return "https://lssc.ir/api/ip/"
        def __init__(self, ip = None):
                get_ip = ""
                if ip != None:
                        get_ip =  ip
                keys ={'ip' : get_ip}
                result = requests.post(url = self.api_url(), params = keys)
                self.ip_info = result.json()
        def ip(self):
                return self.ip_info['query']
        def asn(self):
                return self.ip_info['asn']
        def asnName(self):
                return self.ip_info['asnName']
        def asnOrg(self):
                return self.ip_info['asnOrg']
        def city(self):
                return self.ip_info['city']
        def continent(self):
                return self.ip_info['continent']
        def country(self):
                return self.ip_info['country']
        def countryCode(self):
                return self.ip_info['countryCode']
        def isp(self):
                return self.ip_info['isp']
        def lat(self):
                return self.ip_info['lat']
        def lon(self):
                return self.ip_info['lon']
        def org(self):
                return self.ip_info['org']
        def region(self):
                return self.ip_info['region']
        def timezone(self):
                return self.ip_info['timezone']
        def utcOffset(self):
                return self.ip_info['utcOffset']
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
