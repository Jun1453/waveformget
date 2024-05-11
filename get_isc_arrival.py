import time
import requests
import numpy as np
from obspy import UTCDateTime

class Event():
    def __init__(self, time: UTCDateTime, lat, lon, dep, mag=None):
        self.srctime = time
        self.srcloc = (lat, lon, dep)
        self.magnitude = mag
        self.stations = []
    def __eq__(self, target):
        return (self.srctime == target.srctime) & (self.srcloc == target.srcloc)
    def __ne__(self, target):
        return not self.__eq__(target)
    def __len__(self):
        return len(self.stations)
    def _findstation(self, target):
        for station in self.stations:
            if station == target: return station
        return None
    def appendstation(self, station):
        self.stations.append(station)
    def __repr__(self):
        return f"{self.srctime} magnitude {self.magnitude} at lat. {self.srcloc[0]} lon. {self.srcloc[1]}"

ev_cat = list(np.load('./gcmt_mw.npy', allow_pickle=True))
print("catalog loaded.")

# for i in range(100):
#     if ev_cat[32020+i].magnitude > 5.5:
#         print(i, ev_cat[32020+i])

for event in ev_cat[32020:42977]:
    if event.magnitude < 5.5: continue
    print(f"requesting for {event} ...", end='')
    starttime = event.srctime - 2 * 60
    endtime = event.srctime + 1 * 60
    request_link = f"https://www.isc.ac.uk/cgi-bin/web-db-run?iscreview=on&out_format=QuakeML&ttime=on&ttres=on&tdef=on&amps=on&phaselist=P&sta_list=&stnsearch=GLOBAL&stn_ctr_lat=&stn_ctr_lon=&stn_radius=&max_stn_dist_units=deg&stn_top_lat=&stn_bot_lat=&stn_left_lon=&stn_right_lon=&stn_srn=&stn_grn=&bot_lat=&top_lat=&left_lon=&right_lon=&searchshape=CIRC&ctr_lat={event.srcloc[0]}&ctr_lon={event.srcloc[1]}&radius=1&max_dist_units=deg&srn=&grn=&start_year={starttime.year}&start_month={starttime.month}&start_day={starttime.day:02d}&start_time={starttime.hour:02d}%3A{starttime.minute:02d}%3A{starttime.second:02d}&end_year={endtime.year}&end_month={endtime.month}&end_day={endtime.day:02d}&end_time={endtime.hour:02d}%3A{endtime.minute:02d}%3A{endtime.second:02d}&min_dep=&max_dep=&min_mag=5.5&max_mag=&req_mag_type=Any&req_mag_agcy=Any&include_links=on&request=STNARRIVALS"
    resp = requests.get(request_link)
    print("status_code:", resp.status_code)
    # print(resp.text)
    with open(f"./quakeml/P/{event.srctime}.xml", "w") as text_file:
        text_file.write(resp.text)
    time.sleep(0.5)