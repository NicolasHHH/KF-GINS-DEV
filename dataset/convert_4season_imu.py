import numpy as np

# input format : unix epoch =  frame_id, (angular velocity (w_x, w_y, w_z), linear accel (a_x, a_y, a_z)).
# target format : weeksecond, d_roll, d_pitch, d_yaw, ax, ay, az

imu_file = np.loadtxt("4season_data/imu_gnss_office_loop/imu.txt", delimiter=" ")
out_fn = "4season_data/imu_to_kfgins_office_loop.txt"


if __name__ == "__main__":

    # create output template
    out_data = np.zeros((len(imu_file)-1, 7))

    # time
    # convert unix epoch time to gnss week time
    imu_file[:, 0] /= 1e9
    # week = (imu_file[:-1, 0] - 315964800) // 604800
    out_data[:, 0] = (imu_file[:-1, 0] - 315964800) % 604800
    # out_data[:, 7] = week.astype(int)
    diff_ts = np.diff(imu_file[:, 0])
    print("mean imu freq: ", 1/np.mean(diff_ts))

    # incremental angles

    out_data[:, 1] = np.diff(imu_file[:, 2]) * diff_ts
    out_data[:, 2] = np.diff(imu_file[:, 1]) * diff_ts
    out_data[:, 3] = - np.diff(imu_file[:, 3]) * diff_ts

    # incremental velocities
    out_data[:, 4] = imu_file[:-1, 5] * diff_ts  # ax
    out_data[:, 5] = imu_file[:-1, 4] * diff_ts

    mean_g = np.mean(imu_file[:, 6])
    print("mean gravity: ", mean_g)
    out_data[:, 6] = - imu_file[:-1, 6] * diff_ts

    np.savetxt(out_fn, out_data, delimiter=" ")
