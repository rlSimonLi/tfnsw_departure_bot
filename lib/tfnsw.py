from datetime import datetime
import re
import pytz
from env import Token
import requests


class Transit:
    def __init__(self, location, line_name, destination, departure_timestamp):
        # the station or stop name
        self.location = location
        # line or bus route
        self.line_name = line_name
        # destination
        self.destination = destination
        # this actual or estimated time of departure (whichever is provided)
        self.departure_timestamp = departure_timestamp

    def get_time_until_departure(self):
        """Return time (rounded to the nearest minutes) until departure. -1 indicates already departed"""
        departure_time = datetime.strptime(self.departure_timestamp, '%Y-%m-%dT%H:%M:%SZ')
        difference = (departure_time - datetime.utcnow())
        # return -1 if the train has already departed
        if difference.days == -1:
            return -1
        # return the time delta rounded to the nearest minute
        return int(round(difference.seconds / 60))

    def get_destination_only(self):
        """get the actual destination only, without the via part"""
        return self.destination.split(' via ')[0]

    def get_short_desc(self):
        """short description of departure for bot status display"""
        time_until_departure = self.get_time_until_departure()
        if time_until_departure > 60:
            message = "{} {} | {}h".format(self.line_name, self.get_destination_only(),
                                           int(round(self.get_time_until_departure() / 60)))
        elif time_until_departure < 1:
            message = "{} {} | <1min".format(self.line_name, self.get_destination_only())
        else:
            message = "{} {} | {}min".format(self.line_name, self.get_destination_only(),
                                             self.get_time_until_departure())
        return message

    def get_long_desc(self):
        """long description of departure for bot command"""
        time_until_departure = self.get_time_until_departure()
        if time_until_departure > 120:
            hour_msg = " {} hours".format(time_until_departure // 60)
        elif time_until_departure > 60:
            hour_msg = " 1 hour"
        else:
            hour_msg = ""
        if time_until_departure == 0:
            minute_msg = " <1 minute"
        elif time_until_departure % 60 == 0:
            minute_msg = ""
        elif time_until_departure % 60 == 1:
            minute_msg = " 1 minute"
        else:
            minute_msg = " {} minutes".format(time_until_departure % 60)
        return "**{} {}**:{} Departing in{}{}.".format(self.line_name, self.destination, self.location,
                                                       hour_msg,
                                                       minute_msg)

    def __str__(self):
        return self.get_long_desc()

    @staticmethod
    def is_same_transit_mode(operator, mode):
        """check if the operator id matches one of the transit mode specified"""
        OPERATORS = {
            'train': ('x0000', 'x0001', 'smnw', '711', '710'),
            'ferry': ('112',),
            'light_rail': ('slr',),
            'bus': ('2459', '2441', '2439', '2436'),
        }
        if mode not in ("train", "ferry", "light_rail", "bus"):
            raise ValueError
        return operator.lower() in OPERATORS[mode]

    @staticmethod
    def fetch_departures(stop_id, mode=''):
        """fetch departure from the TfUNSW API"""
        departures = []

        # the API uses UTC time
        current_time = datetime.now(pytz.timezone('Australia/Sydney'))
        URL = 'https://api.transport.nsw.gov.au/v1/tp/departure_mon'
        API_KEY = Token.tfnsw_token
        PARAMS = {
            'outputFormat': 'rapidJSON',
            'coordOutputFormat': 'EPSG:4326',
            'mode': 'direct',
            'type_dm': 'stop',
            'name_dm': stop_id,
            'itdDate': current_time.strftime('%Y%m%d'),  # YYYYmmdd
            'itdTime': current_time.strftime('%H%M'),  # HHMM
            'TfNSWDM': 'true',
            'departureMonitorMacro': 'true'
        }
        HEADERS = {
            'Authorization': 'apikey ' + API_KEY,
        }

        r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
        data = r.json()

        stop_name = data['locations'][0]['disassembledName']

        for departure in data['stopEvents']:
            operator = departure['transportation']['operator']['id']
            if mode != "":
                # skip if the operator is not in the transit mode specified
                if not Transit.is_same_transit_mode(operator, mode):
                    continue
            if 'departureTimeEstimated' in departure:
                departure_timestamp = departure['departureTimeEstimated']
            else:
                departure_timestamp = departure['departureTimePlanned']
            line_name = departure['transportation']['disassembledName']
            # departure location name is "Suburb, Name Station, Platform X"
            try:
                location = " {} |".format(re.match(r'.*(Platform\s\d+)', departure['location']['name']).group(1))
            except AttributeError:
                location = ""
            destination = departure['transportation']['destination']['name']

            new_departure = Transit(location, line_name, destination, departure_timestamp)
            if new_departure.get_time_until_departure() >= 0:
                departures.append(new_departure)

        departures.sort(key=lambda d: d.get_time_until_departure())
        return stop_name, departures
