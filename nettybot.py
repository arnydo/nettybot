from pprint import pprint
import requests
import dns.resolver
import json
import sys
import os
try:
    from flask import Flask
    from flask import request
except ImportError as e:
    print(e)
    print("Looks like 'flask' library is missing.\n"
          "Type 'pip3 install flask' command to install the missing library.")
    sys.exit()

#Cisco Spark Info
baseurl = "https://api.ciscospark.com/v1"

bearer = "NmJiZDUzOWUtMDcxNy00Y2M3LWEwYjYtZjdhM2FlODVmNjFiMzYyM2IxNDAtNGRh"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + bearer
}

me_resp = requests.get(baseurl + '/people/me', headers=headers)
# Check that the Spark access token belongs to a bot
if json.loads(me_resp.text)['type'] != 'bot':
    print('SPARK_ACCESS_TOKEN does not belong to a bot...exiting')
    exit()

expected_messages = {
    "help me": "help",
    "need help": "help",
    "can you help me": "help",
    "ayuda me": "help",
    "help": "help",
    "greetings": "greetings",
    "hello": "greetings",
    "hi": "greetings",
    "how are you": "greetings",
    "what's up": "greetings",
    "what's up doc": "greetings"
}

def send_spark_get(url, payload=None,js=True):

    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request= request.json()
    return request


def send_spark_post(url, data):

    request = requests.post(url, json.dumps(data), headers=headers).json()
    return request


def getIpInfo(ip):
    """
    This method is used for:
        -qerying ipinfo.io's API for basic IP information. Geolocation, Owner, etc.
    """
    r = requests.get("https://ipinfo.io/" +ip +"/json")
    ipInfo = "**IP LOOKUP:**<br/>"
    for i in r.json():
        ipInfo += i +": " +r.json()[i] +"<br/>"
    return ipInfo

def getWhoIs(domain):
    whoIsInfo  = "**WHOIS LOOKUP:**<br/>"
    return whoIsInfo

class nettydns:

    def aRec(domain):
        myResolver = dns.resolver.Resolver()
        dnsInfo = "**A LOOKUP:** " +domain +"<br/>"
        try:
            myAnswer = myResolver.query(domain, "A")
            for rdata in myAnswer:
                dnsInfo += rdata.to_text() +"<br/>"
        except dns.resolver.NoAnswer:
            dnsInfo += "No A record(s) found...sorry!"
        except dns.resolver.NXDOMAIN:
            dnsInfo += "*OOPS!* - Domain doesn't appear to be valid. Typo??"
        return dnsInfo

    def cnameRec(domain):
        myResolver = dns.resolver.Resolver()
        dnsInfo = "**CNAME LOOKUP:** " +domain +"<br/>"
        try:
            myAnswer = myResolver.query(domain, "CNAME")
            for rdata in myAnswer:
                dnsInfo += rdata.to_text() +"<br/>"
        except dns.resolver.NoAnswer:
            dnsInfo += "No CNAME record(s) found...sorry!"
        except dns.resolver.NXDOMAIN:
            dnsInfo += "*OOPS!* - Domain doesn't appear to be valid. Typo??"
        return dnsInfo

    def mxRec(domain):
        myResolver = dns.resolver.Resolver()
        dnsInfo = "**MX LOOKUP:** " +domain +"<br/>"
        try:
            myAnswer = myResolver.query(domain, "MX")
            for rdata in myAnswer:
                dnsInfo += rdata.to_text() +"<br/>"
        except dns.resolver.NoAnswer:
            dnsInfo += "No MX record(s) found...sorry!"
        except dns.resolver.NXDOMAIN:
            dnsInfo += "*OOPS!* - Domain doesn't appear to be valid. Typo??"
        return dnsInfo

    def txtRec(domain):
        myResolver = dns.resolver.Resolver()
        dnsInfo = "**TXT LOOKUP:** " +domain +"<br/>"
        try:
            myAnswer = myResolver.query(domain, "TXT")
            for rdata in myAnswer:
                dnsInfo += rdata.to_text() +"<br/>"
        except dns.resolver.NoAnswer:
            dnsInfo += "No TXT record(s) found...sorry!"
        except dns.resolver.NXDOMAIN:
            dnsInfo += "*OOPS!* - Domain doesn't appear to be valid. Typo??"
        return dnsInfo

    def soaRec(domain):
        myResolver = dns.resolver.Resolver()
        dnsInfo = "**SOA LOOKUP:** " +domain +"<br/>"
        try:
            myAnswer = myResolver.query(domain, "SOA")
            for rdata in myAnswer:
                dnsInfo += rdata.to_text() +"<br/>"
        except dns.resolver.NoAnswer:
            dnsInfo += "No SOA record(s) found...sorry!"
        except dns.resolver.NXDOMAIN:
            dnsInfo += "*OOPS!* - Domain doesn't appear to be valid. Typo??"
        return dnsInfo

    def srvRec(domain):
        myResolver = dns.resolver.Resolver()
        dnsInfo = "**SRV LOOKUP:** " +domain +"<br/>"
        try:
            myAnswer = myResolver.query(domain, "SRV")
            for rdata in myAnswer:
                dnsInfo += rdata.to_text() +"<br/>"
        except dns.resolver.NoAnswer:
            dnsInfo += "No SRV record(s) found...sorry!"
        except dns.resolver.NXDOMAIN:
            dnsInfo += "*OOPS!* - Domain doesn't appear to be valid. Typo??"
        return dnsInfo

def help_me():

    return "Sure! I can help. Below are the commands that I understand:<br/>" \
           "`Help me` - I will display what I can do.<br/>" \
           "`IP | X.X.X.X` - I will provide information about a particular IP address.<br/>" \
           "`A | domain` - I will provide A records of a given domain.<br/>" \
           "`MX | domain` - I will provide MX records of a given domain.<br/>" \
           "`TXT | domain` - I will provide TXT records of a given domain.<br/>" \
           "`SOA | domain` - I will provide SOA records of a given domain.<br/>" \
           "`SRV | domain` - I will provide SRV records of a given domain.<br/>"

def greetings():

    return "Hi my name is %s.<br/>" \
            "Type `Help me` to see what I can do." % bot_name
    



app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def spark_webhook():
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        print(webhook)
        if webhook['data']['personEmail']!= bot_email:
            pprint(webhook)
        if webhook['resource'] == "memberships" and webhook['data']['personEmail'] == bot_email:
            send_spark_post("https://api.ciscospark.com/v1/messages",
                            {
                                "roomId": webhook['data']['roomId'],
                                "markdown": (greetings() +
                                             "**Note This is a group room and you have to call "
                                             "me specifically with `@%s` for me to respond**" % bot_name)
                            }
                            )
        msg = None
        if "@sparkbot.io" not in webhook['data']['personEmail']:
            result = send_spark_get(
                'https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name.lower() + " ", '')
            if in_message in expected_messages and expected_messages[in_message] is "help":
                msg = help_me()
            elif in_message in expected_messages and expected_messages[in_message] is "greetings":
                msg = greetings()
            elif in_message.startswith('ip |'):
                data = in_message.split("|")
                ip = data[1].lstrip()
                msg = getIpInfo(ip)
            elif in_message.startswith('a |'):
                data = in_message.split("|")
                domain = data[1].lstrip()
                msg = nettydns.aRec(domain)
            elif in_message.startswith('cname |'):
                data = in_message.split("|")
                domain = data[1].lstrip()
                msg = nettydns.cnameRec(domain)
            elif in_message.startswith('mx |'):
                data = in_message.split("|")
                domain = data[1].lstrip()
                msg = nettydns.mxRec(domain)
            elif in_message.startswith('txt |'):
                data = in_message.split("|")
                domain = data[1].lstrip()
                msg = nettydns.txtRec(domain)
            elif in_message.startswith('soa |'):
                data = in_message.split("|")
                domain = data[1].lstrip()
                msg = nettydns.soaRec(domain)
            elif in_message.startswith('srv |'):
                data = in_message.split("|")
                domain = data[1].lstrip()
                msg = nettydns.srvRec(domain)
            elif in_message.startswith('whois |'):
                data = in_message.split("|")
                domain = data[1].lstrip()
                msg = getWhoIs(domain)
            elif in_message.startswith("repeat after me"):
                message = in_message.split('repeat after me ')[1]
                if len(message) > 0:
                    msg = "{0}".format(message)
                else:
                    msg = "I did not get that. Sorry!"
            else:
                msg = "Sorry, but I did not understand your request. Type `Help me` to see what I can do"
            if msg != None:
                send_spark_post("https://api.ciscospark.com/v1/messages",
                                {"roomId": webhook['data']['roomId'], "markdown": msg})
        return "true"
    elif request.method == 'GET':
        message = "<center><img src=\"https://cdn0.iconfinder.com/data/icons/thin-analytics/57/thin-360_hierarchy_diagram_structure-512.png\" alt=\"NettyBot\" style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>HEY! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
                  "<center><b><i>Don't forget to create Webhooks to start receiving events from Cisco Spark!</i></b></center>" % bot_name
        return message

def main():
    global bot_email, bot_name
    if len(bearer) != 0:
        test_auth = send_spark_get("https://api.ciscospark.com/v1/people/me", js=False)
        if test_auth.status_code == 401:
            print("Looks like the provided access token is not correct.\n"
                  "Please review it and make sure it belongs to your bot account.\n"
                  "Do not worry if you have lost the access token. "
                  "You can always go to https://developer.ciscospark.com/apps.html "
                  "URL and generate a new access token.")
            sys.exit()
        if test_auth.status_code == 200:
            test_auth = test_auth.json()
            bot_name = test_auth.get("displayName","")
            bot_email = test_auth.get("emails","")[0]
    else:
        print("'bearer' variable is empty! \n"
              "Please populate it with bot's access token and run the script again.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.ciscospark.com/apps.html "
              "URL and generate a new access token.")
        sys.exit()

    if "@sparkbot.io" not in bot_email:
        print("You have provided an access token which does not relate to a Bot Account.\n"
              "Please change for a Bot Account access toekneview it and make sure it belongs to your bot account.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.ciscospark.com/apps.html "
              "URL and generate a new access token for your Bot.")
        sys.exit()
    else:
        app.run(host='0.0.0.0', port=10010)

if __name__ == "__main__":
    main()
