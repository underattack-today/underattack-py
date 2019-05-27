This is the official repository for the Underattack.Today Python module.

### Underattack.Today

Underattack is a free security intelligence platform.

For more information please visit https://underattack.today

### API

Underattack provides a free API described here: https://portal.underattack.today/api/docs

To use it you should register to the portal, it's free :)

### The Python module

The module can be both imported in your own project or used as a command line tool.

##### As a module

    >>> import underattack
    >>> u = underattack.UnderattackAPIConnector('user', 'password')
    >>> print(u.get_daily_feeds_yesterday())
    {'count': 1203, 'indicators': ['1.4.247.114', '1.52.153.158', ... ]}
    >>> print(u.get_daily_feeds_yesterday(['iot', 'botnet']))
    {'count': 1203, 'indicators': ['1.4.247.114', ... ]}
    >>> print(u.lookup_ip('138.246.253.5')
    {'count': 31, 'events': [{'asn_org': 'Leibniz-Rechenzentrum', 'country_name': 'Germany', 'end': '2018-08-21T22:34:20.534000', 'tags': ['http/https'], 'indicator': '138.246.253.5', 'start': '2018-08-21T22:34:20.534000', 'asn': 12816}, ...]}
    >>> print(u.get_tags_list())
    {'tags': ['http/https', 'mongodb', 'ftp', 'upnp', ... ]}

##### As a tool

    user@localhost:~$ ./underattack.py --help
    usage: underattack.py [-h] [--version] --username USERNAME --password PASSWORD
                          [--file-name FILE_NAME | --stdout] [--debug | --quiet]
                          (--lookup-ip LOOKUP_IP | --feeds-yesterday | --tags-list)
                          [--tags TAGS]

    Underattack.Today API Client. Visit https://portal.underattack.today/api/docs

    optional arguments:
      -h, --help            show this help message and exit
      --version, -v         show program's version number and exit
      --file-name FILE_NAME, -f FILE_NAME
                            path of log file
      --stdout, -s          log in stdout
      --debug, -d           show more verbose logging
      --quiet, -q           disable logging
      --lookup-ip LOOKUP_IP, -ip LOOKUP_IP
                            get information about an IP
      --feeds-yesterday, -fy
                            get yesterday's feeds
      --tags-list, -tl      get list of all available tags
      --tags TAGS, -t TAGS  when calling -fy list here the tags to retrieve in csv
                            format, gets ignored in other cases

    Authentication:
      --username USERNAME, -u USERNAME
      --password PASSWORD, -p PASSWORD


Lookup IP

    user@localhost:~$ ./underattack.py -u user -p password -ip 138.246.253.5
    {
        "count": 31,
        "events": [
            {
                "asn": 12816,
                "asn_org": "Leibniz-Rechenzentrum",
                "country_name": "Germany",
                "end": "2018-08-21T22:34:20.534000",
                "indicator": "138.246.253.5",
                "start": "2018-08-21T22:34:20.534000",
                "tags": [
                    "http/https"
                ]
            },
            ...
        ]
    }

Daily feeds

    user@localhost:~$ ./underattack.py -u user -p password -fy
    {
        "count": 1197,
        "indicators": [
            "1.4.247.114",
            "1.52.153.158",
            "1.179.146.156",
            ...
        ]
    }

Daily feeds with tags

    user@localhost:~$ ./underattack.py -u user -p password -fy -t iot,botnet,ssh
    {
        "count": 1197,
        "indicators": [
            "1.4.247.114",
            "1.179.146.156",
            ...
        ]
    }

Tags list

    user@localhost:~$ ./underattack.py -u user -p password -tl
    {
        "tags": [
            "http/https",
            "mongodb",
            "ftp",
            ...
            "CVE-2018-10561",
            "CVE-2019-3396",
            "CVE-2017-12615"
        ]
    }