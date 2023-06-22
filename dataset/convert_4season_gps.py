from pynmeagps import NMEAReader
import numpy as np
import datetime
from dataset.dataset_utils import datetime2unix, GpsParser, unix2gnssweek


if __name__ == "__main__":

    nmea_path = "4season_data/imu_gnss_office_loop/septentrio.nmea"
    out_fn = "4season_data/gps_to_kfgins_office_loop.txt"

    with open(nmea_path, "r") as f:
        nmea = f.readlines()

    parsed_msg = []
    for msg in nmea[1:]:
        parsed_msg.append(NMEAReader.parse(msg))
    print(parsed_msg[0])

    gps_array = GpsParser(file_path=nmea_path).to_array()
    print(gps_array[0])
    # timestamp, lat, lon, alt, std_lat, std_lon, std_alt, speed, heading

    gps_valid = []
    for i in range(len(gps_array)):
        if 3 < gps_array[i, 9] < 6:
            gps_valid.append(gps_array[i])
    gps_valid = np.array(gps_valid, dtype=np.float64)
    print(gps_valid.shape)

    for i in range(len(gps_valid)):
        if gps_valid[i, 8] != 0:
            print("initial heading: ", 90 - gps_valid[i, 8])
            break

    print("initial speed: ", gps_valid[0, 7] * np.cos(gps_valid[i, 8] * np.pi / 180.0),
          gps_valid[0, 7] * np.sin(gps_valid[i, 8] * np.pi / 180.0))
    print("initial timestamp: ", gps_valid[0, 0])

    out_data = np.zeros((len(gps_valid), 7))
    out_data[:, 0] = unix2gnssweek(gps_valid[:, 0])  # timestamp
    out_data[:, 1] = gps_valid[:, 1]  # latitude
    out_data[:, 2] = gps_valid[:, 2]  # longitude
    out_data[:, 3] = gps_valid[:, 3]  # altitude

    out_data[:, 4] = gps_valid[:, 4]
    out_data[:, 5] = gps_valid[:, 5]
    out_data[:, 6] = gps_valid[:, 6]

    np.savetxt(out_fn, out_data, delimiter=" ")
