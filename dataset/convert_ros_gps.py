import numpy as np

date_time = "20230619_184246"
gps_file = np.loadtxt("ros_data/"+date_time+"/gps_log_" + date_time + ".csv", delimiter=",", skiprows=1)
out_fn = "ros_data/"+date_time+"/gps_to_kfgins_" + date_time + ".txt"

if __name__ == "__main__":

    out_data = np.zeros((len(gps_file), 7))

    # convert unix epoch time to gnss week time
    # week = (gps_file[:, 0] - 315964800) // 604800
    out_data[:, 0] = (gps_file[:, 0] - 315964800) % 604800
    out_data[:, 1] = gps_file[:, 1] # latitude
    out_data[:, 2] = gps_file[:, 2] # longitude
    out_data[:, 3] = gps_file[:, 3] # altitude
    out_data[:, 4] = gps_file[:, 4]*10
    out_data[:, 5] = gps_file[:, 8]*10
    out_data[:, 6] = gps_file[:, 12]*10
    # out_data[:, 7] = week.astype(int)

    np.savetxt(out_fn, out_data, delimiter=" ", fmt="%.13f")

