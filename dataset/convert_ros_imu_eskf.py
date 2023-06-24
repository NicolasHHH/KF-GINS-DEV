import numpy as np

date_time = "20230622_012013"
imu_file = np.loadtxt("ros_data/imu_log_" + date_time + ".csv", delimiter=",", skiprows=1)
out_ACC = "ros_data/acc_to_eskf_"+ date_time +".csv"
out_GYRO = "ros_data/gyro_to_eskf_"+ date_time +".csv"
out_TIME = "ros_data/time_to_eskf_"+ date_time +".csv"


if __name__ == "__main__":

    out_data_acc = np.zeros((len(imu_file), 3))
    out_data_gyro = np.zeros((len(imu_file), 3))
    out_data_time = np.zeros((len(imu_file), 1))
    out_data_time[:, 0] = imu_file[:, 0]

    out_data_gyro[:, 0] = imu_file[:, 5]
    out_data_gyro[:, 1] = imu_file[:, 6]
    out_data_gyro[:, 2] = imu_file[:, 7]

    out_data_acc[:, 0] = imu_file[:, 8]
    out_data_acc[:, 1] = imu_file[:, 9]
    out_data_acc[:, 2] = imu_file[:, 10]


    np.savetxt(out_ACC, out_data_acc, delimiter=",")
    np.savetxt(out_GYRO, out_data_gyro, delimiter=",")
    np.savetxt(out_TIME, out_data_time, delimiter=",")
