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

class Station():
    def __init__(self, station, lat, lon, dist, azi, loc=''):
        self.labelsta = {'name': station, 'lat': lat, 'lon': lon, 'dist': dist, 'azi': azi, 'loc': loc}
        self.labelnet = {'code': None}
        self.records = []
        self.isdataexist = False
    def __eq__(self, target):
        return (self.labelsta['name'] == target.labelsta['name'])
    def __ne__(self, target):
        return not self.__eq__(target)
    def __repr__(self):
        return f"observation at station {self.labelsta['name']} of {self.labelnet['code'] or 'UNKNOWN'} network with azimuth angle {(self.labelsta['azi']+180)%360} deg"

class Record():
    def __init__(self, phase, residual, error, ellipcor, crustcor, obstim, calctim):
        self.phase = phase
        self.residual = residual
        self.error = error
        self.ellipcor = ellipcor
        self.crustcor = crustcor
        self.obstim = obstim
        self.calctim = calctim