#!/usr/bin/python

import re
import time
import urllib

import requests
s = requests.Session()

# Get reservation form page (for 'sx-tab-identifier' value)
resp = s.get('http://www.sixt.de/php/reservation/start_lkw?ctyp=L')

# <input type="hidden" id="sx-tab-identifier"     name="tab_identifier" value="1435398301" />
match = re.search('id="sx-tab-identifier".*?value="(\d+)"', resp.text)
if match:
    tab_identifier = match.group(1)
else:
    print("Could not find sx-tab-identifier, exiting.")
    exit(1)

# Reservation config
pickup_station = "1234"
pickup_time = "hh:mm"
pickup_date = "dd.mm.yyyy"
return_station = "1234"
return_time = "hh:mm"
return_date = "dd.mm.yyyy"


get_params = {
    "_": time.time(),
    "posl": "DE",
    "rci": return_station,
    "rda": return_date,
    "rli": "DE",
    "rti": return_time,
    "tab_identifier": tab_identifier,
    "uci": pickup_station,
    "uda": pickup_date,
    "uli": "DE",
    "uti": pickup_time,
    "wants_coi": "0",
    "wants_uk_col": "0",
    "wants_uk_del": "0"
}
# AJAX-Request
resp = s.get('http://www.sixt.de/php/reservation/offer.request', params=get_params)

params = {"has_social_login": "",
        "is_corpcust": "",
        "layout": "list",
        "posl": "DE",
        "rci": return_station, 
        "rda": return_date,
        "rli": "DE",
        "rti": return_time,
        "tab_identifier": tab_identifier,
        "uci": pickup_station,
        "uda": pickup_date,
        "uli": "DE",
        "uti": pickup_time}
# Normal HTTP request, displays result page.
resp = s.post("http://www.sixt.de/php/reservation/offerselect", data=params)

#<p>Mittlerer LKW bis 3,5t (S)</p>
#<span class="sx-gc-debug">DEU2V000(P75)=S/S/81<br/>46002,62374,64430,64449,64389,64470,64329,64349,64369,64409</span>
#</div>
#<div class="sx-res-offerlist-offerprice">
#<p><strong>&euro; 138,98</strong></p>

state = 0
for line in resp.text.splitlines():
    if state == 0 and "Mercedes-Benz Sprinter 313 L / 316 L" in line:
        state = 1
    elif state == 1 and '<div class="sx-res-offerlist-offerprice">' in line:
        state = 2
    elif state == 2:
        match = re.search("(\d+,\d+)", line)
        if match:
            print(match.group(1))
            exit(0)

print("Could not find price")
exit(2)

