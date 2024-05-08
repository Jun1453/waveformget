import numpy as np
from data_class import *
from obspy import UTCDateTime
from obspy.clients.fdsn.mass_downloader import GlobalDomain, Restrictions, MassDownloader

def download_event(origin_time):
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
        network='AF,AU,BI,BR,C,C8,CB,CD,CK,CN,CR,DK,DW,G,GE,GT,HG,IA,IC,ID,II,IM,IN,IU,MM,MN,MP,MY,NZ,PS,SR,TJ'
        )

    # No specified providers will result in all known ones being queried.
    mdl = MassDownloader()

    # The data will be downloaded to the ``./waveforms/`` and ``./stations/``
    # folders with automatically chosen file names.
    mdl.download(domain, restrictions, mseed_storage=f"/volume1/seismic/rawdata_catalog_mass/{origin_time}/waveforms",
                stationxml_storage=f"/volume1/seismic/rawdata_catalog_mass/{origin_time}/stations")


if __name__ == '__main__':
    events = np.load('./gcmt_mw.npy', allow_pickle=True)
    # origin_time = UTCDateTime(2011, 3, 11, 5, 47, 32)
    # origin_time = UTCDateTime("2011-01-01T01:56:07.800000Z")
    # for event in events[33872:36100]: # year 2011
    # for event in events[36100:38386]: # year 2012
    # for event in events[38386:40514]: # year 2013
    for event in events[40514:42977]: # year 2014
    # for event in events[42977:45149]: # year 2015
    # for event in events[45149:47388]: # year 2016
    # for event in events[47388:49525]: # year 2017
    # for event in events[49525:51795]: # year 2018
    # for event in events[51795:54224]: # year 2019
    # for event in events[54224:56611]: # year 2020
    # for event in events[56611:59459]: # year 2021
    # for event in events[59459:62117]: # year 2022
    # for event in events[62117:]: # year 2023
        if event.magnitude < 5.5: continue
        download_event(event.srctime)