import numpy as np

date_time = "20230622_012013"
gps_file = np.loadtxt("ros_data/gps_log_" + date_time + ".csv", delimiter=",", skiprows=1)
out_GPS = "ros_data/gps_to_eskf_"+ date_time +".csv"
out_GPS_T = "ros_data/gts_to_eskf_"+ date_time +".csv"


if __name__ == "__main__":

    out_data_gps = np.zeros((len(gps_file), 6))

    out_data_time = np.zeros((len(gps_file), 1))
    out_data_time[:, 0] = gps_file[:, 0]

    out_data_gps[:, 0:3] = gps_file[:, 1:4]
    out_data_gps[:, 3] = np.insert(np.diff(gps_file[:, 1])/np.diff(gps_file[:, 0]), 0, 0)
    out_data_gps[:, 4] = np.insert(np.diff(gps_file[:, 2]) / np.diff(gps_file[:, 0]), 0, 0)

    np.savetxt(out_GPS, out_data_gps, delimiter=",")
    np.savetxt(out_GPS_T, out_data_time, delimiter=",")
