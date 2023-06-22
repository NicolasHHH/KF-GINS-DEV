from pynmeagps import NMEAReader
import numpy as np
import datetime


def unix2gnssweek(unix_time):
    unix_time = np.array(unix_time, dtype=np.float64)
    print(unix_time[0:10], (unix_time[0:10] - 315964800.0) % 604800.0)
    # week = np.array((unix_time - 315964800) // 604800
    return np.array((unix_time - 315964800.0) % 604800.0)


def datetime2unix(date_str, time_str):
    # the space in between is necessary
    datetime_str = f"{date_str} {time_str}"
    if "." not in datetime_str:
        datetime_str += ".00000"
    dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    # set time zone to UTC
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    # Convert the datetime object to a Unix timestamp
    return dt.timestamp()  # float


class GPS:
    def __init__(self):
        self.lat = None
        self.lon = None
        self.timestamp = None
        self.speed = None
        self.heading = None
        self.mode = None
        self.alt = None
        self.quality = None
        self.std_lat = None
        self.std_lon = None
        self.std_alt = None

    def set_gps(self, lon, lat, alt, date_str, time_str, spd, cog, mode, quality, std_lat, std_lon, std_alt):
        self.lat = lat
        self.lon = lon
        self.timestamp = datetime2unix(date_str, time_str)
        self.speed = spd
        self.heading = cog
        self.mode = mode
        self.alt = alt
        self.quality = quality
        self.std_lat = std_lat
        self.std_lon = std_lon
        self.std_alt = std_alt

    def set_RMC(self, lon, lat, time_str, date_str, spd, cog, mode):
        self.lat = lat
        self.lon = lon
        self.timestamp = datetime2unix(date_str, time_str)
        self.speed = spd
        if cog == "":
            cog = 0.0
        self.heading = cog
        self.mode = mode

    def set_GGA(self, alt, quality):
        self.alt = alt
        self.quality = quality

    def set_GST(self, std_lat, std_lon, std_alt):
        self.std_lat = std_lat
        self.std_lon = std_lon
        self.std_alt = std_alt

    def __str__(self):
        return f"GPS(lat={self.lat}, lon={self.lon}, timestamp={self.timestamp}, speed={self.speed}, heading={self.heading}, mode={self.mode}, alt={self.alt}, quality={self.quality}, std_lat={self.std_lat}, std_lon={self.std_lon}, std_alt={self.std_alt})"

    def to_array(self):
        # return [self.timestamp, self.lat, self.lon, self.alt, self.std_lat, self.std_lon, self.std_alt, self.speed, self.quality+0.0]
        return [self.timestamp, self.lat, self.lon, self.alt, self.std_lat, self.std_lon, self.std_alt, self.speed,
                self.heading, self.quality + 0.0]


class GpsParser(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.gps_list = []
        self.parse()

    def parse(self):
        with open(self.file_path, "r") as f:
            res = f.readlines()
            gps = GPS()
            last_msg = "GST"
            for line in res[1:]:
                msg = NMEAReader.parse(line)
                if msg.msgID == "RMC" and last_msg == "GST":
                    gps = GPS()
                    last_msg = "RMC"
                    gps = self.parse_gprmc(gps_obj=gps, msg=msg)
                elif msg.msgID == "GGA" and last_msg == "RMC":
                    last_msg = "GGA"
                    gps = self.parse_gpgga(gps_obj=gps, msg=msg)
                elif msg.msgID == "GST" and last_msg == "GGA":
                    last_msg = "GST"
                    gps = self.parse_gpgst(gps_obj=gps, msg=msg)
                    if gps.quality > 2:
                        self.gps_list.append(gps)

    def parse_gpgga(self, gps_obj, msg):
        gps_obj.set_GGA(
            alt=msg.alt,
            quality=msg.quality
        )
        return gps_obj

    def parse_gpgst(self, gps_obj, msg):
        gps_obj.set_GST(
            std_lat=msg.stdLat,
            std_lon=msg.stdLong,
            std_alt=msg.stdAlt
        )
        return gps_obj

    def parse_gprmc(self, gps_obj, msg):
        gps_obj.set_RMC(
            lon=msg.lon,
            lat=msg.lat,
            time_str=msg.time,
            date_str=msg.date,
            spd=msg.spd,
            cog=msg.cog,
            mode=msg.posMode
        )
        return gps_obj

    def to_array(self):
        return np.array([gps.to_array() for gps in self.gps_list], dtype=np.float64)
