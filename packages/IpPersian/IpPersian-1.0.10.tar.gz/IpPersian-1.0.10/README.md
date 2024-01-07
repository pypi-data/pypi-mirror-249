## Ip Lookup Persian

The IpPersian library can give you complete information about the requester's IP. If you want to check the IP address of the person using yours application or site, in which country and city, use this library. These are not the only facilities available, are continue...

---

### **Install Library IpPersian**

```python
pip install IpPersian
```

### **Import Library to module**

```python
from IpPersian import IpPersian
```

### Use Library in module

If you want to check a person's default IP, do the following...

```python
from IpPersian import IpPersian
ip = IpPersian()
```

If you want all the IP information to be displayed to you, do the following...

```python
from IpPersian import IpPersian
ip = IpPersian()
print(ip)
__________ output __________
IP : xx:xx:xx:xx
asn : x
country : x   city: x
...
```

If you want to check a specific IP, just send it to the library.

```python
from IpPersian import IpPersian
ip = IpPersian("xx.xx.xx.xx")
print(ip)
__________ output __________
IP : xx.xx.xx.xx
asn : x
country : x   city: x
...
```

### Receive information in a separate form

If you want to get the IP information separately, use the table below...

| function      | call type | description                                                  |
| ------------- | --------- | ------------------------------------------------------------ |
| ip()          | abject    | return IP                                                    |
| asn()         | abject    | return number asn by type string                             |
| asnName()     | abject    | returns name asn                                             |
| asnOrg()      | abject    | returns the name of the company that registered the asn      |
| city()        | abject    | returns the name of the city where the ip is used            |
| continent()   | abject    | returns the name of the continent on which the IP is located |
| country()     | abject    | returns the name of the country in which the IP is located   |
| countryCode() | abject    | returns the global country code of the ip                    |
| isp()         | abject    | returns the name of the IP Internet provider                 |
| lat()         | abject    | return number lat by type string, for location               |
| lon()         | abject    | return number lon by type string, for location               |
| org()         | abject    | returns the IP provider company name                         |
| region()      | abject    | returns the name of the province in which the IP is used     |
| timezone()    | abject    | returns the time zone of the ip                              |
| utcOffset()   | abject    | returns the time point of the ip                             |

---

### **Changes made**

- Version 1.0.10
  - bug fixed

- Version 1.0.9
  - secure ip token
  - compatibility to Django (install requires = requests library)

---

The great scientific and educational collection of the [**SARZAMIN DANESH**](https://lssc.ir) thanks you.
