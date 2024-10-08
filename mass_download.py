import os
import sys
import numpy as np
from data_class import *
from obspy import UTCDateTime
from obspy.clients.fdsn.mass_downloader import GlobalDomain, Restrictions, MassDownloader

init_event_num = {
    2010: 32020,
    2011: 33872,
    2012: 36100,
    2013: 38386,
    2014: 40514,
    2015: 42977,
    2016: 45149,
    2017: 47388,
    2018: 49525,
    2019: 51795,
    2020: 54224,
    2021: 56611,
    2022: 59459,
    2023: 62117,
    2024: None
}

def download_event(downloader, origin_time, init_year=None, network=None, station=None, save_path=".", skip_existing_folder=False):
    origin_time.precision = 3
    fn_starttime_full = lambda srctime: srctime - 0.5 * 60 * 60
    fn_endtime_full = lambda srctime: srctime + 2 * 60 * 60 + 1

    # Circular domain around the epicenter. This will download all data between
    # 70 and 90 degrees distance from the epicenter. This module also offers
    # rectangular and global domains. More complex domains can be defined by
    # inheriting from the Domain class.
    # domain = CircularDomain(latitude=37.52, longitude=143.04,
    #                         minradius=70.0, maxradius=90.0)
    domain = GlobalDomain()

    restrictions = Restrictions(
        # Get data from 5 minutes before the event to one hour after the
        # event. This defines the temporal bounds of the waveform data.
        starttime=fn_starttime_full(origin_time),
        endtime=fn_endtime_full(origin_time),
        # You might not want to deal with gaps in the data. If this setting is
        # True, any trace with a gap/overlap will be discarded.
        reject_channels_with_gaps=True,
        # And you might only want waveforms that have data for at least 95 % of
        # the requested time span. Any trace that is shorter than 95 % of the
        # desired total duration will be discarded.
        minimum_length=0.99,
        # No two stations should be closer than 10 km to each other. This is
        # useful to for example filter out stations that are part of different
        # networks but at the same physical station. Settings this option to
        # zero or None will disable that filtering.
        minimum_interstation_distance_in_m=10E3,
        # Only HH or BH channels. If a station has HH channels, those will be
        # downloaded, otherwise the BH. Nothing will be downloaded if it has
        # neither. You can add more/less patterns if you like.
        channel_priorities=["LH[ZNE12]"],
        # Location codes are arbitrary and there is no rule as to which
        # location is best. Same logic as for the previous setting.
        location_priorities=["", "00", "10"],

        # customized
        # exclude_networks=("AM", "SY")
        network=network,
        station=station
        )

    save_path = f"{save_path}/{f'{init_year}/' if init_year else ''}{origin_time}"
    if skip_existing_folder and os.path.exists(save_path): return

    # The data will be downloaded to the ``./waveforms/`` and ``./stations/``
    # folders with automatically chosen file names.
    downloader.download(domain, restrictions, mseed_storage=f"{save_path}/waveforms",
                        stationxml_storage=f"{save_path}/stations")


if __name__ == '__main__':
    if len(sys.argv) < 2: raise ValueError("year is required in args")

    # No specified providers will result in all known ones being queried.
    mdl = MassDownloader(["IRIS"])

    if str(sys.argv[1]).split('.')[-1] == 'npy':
        events = np.load(str(sys.argv[1]), allow_pickle=True)
        for event in events:
            station = ",".join([station.labelsta['name'] for station in event.stations])
            download_event(mdl, event.srctime, station=station, save_path=f"./rawdata_{str(sys.argv[1]).split('.')[-2]}", skip_existing_folder=True)

    else:
        events = np.load('./gcmt_mw.npy', allow_pickle=True)
        # origin_time = UTCDateTime(2011, 3, 11, 5, 47, 32)
        # origin_time = UTCDateTime("2011-01-01T01:56:07.800000Z")
        network = 'AF,AU,BI,BR,C,C8,CB,CD,CK,CN,CR,DK,DW,G,GE,GT,HG,IA,IC,ID,II,IM,IN,IU,MM,MN,MP,MY,NZ,PS,SR,TJ'

        
        for event in events[init_event_num[int(sys.argv[1])]:init_event_num[int(sys.argv[1])+1]]: 
            if event.magnitude < 5.5: continue
            download_event(mdl, event.srctime, int(sys.argv[1]), network=network, save_path="./rawdata_catalog_mass", skip_existing_folder=True)
