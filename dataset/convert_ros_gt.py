import numpy as np

date_time = "20230619_184246"
imu_file = np.loadtxt("ros_data/"+date_time+ "/imu_log_" + date_time + ".csv", delimiter=",", skiprows=1)
out_fn = "ros_data/"+date_time+ "/imu_to_kfgins_"+ date_time +".txt"


def quaternion_to_euler_angle(xyzw):
    x, y, z, w = xyzw

    euler_angle = [np.arctan2(2*(w*x + y*z), 1 - 2*(x**2 + y**2)),
                   np.arcsin(2*(w*y - z*x)),
                   np.arctan2(2*(w*z + x*y), 1 - 2*(y**2 + z**2))]

    return euler_angle


if __name__ == "__main__":

    out_data = np.zeros((len(imu_file), 7))
    print(len(imu_file))
    yaws = [quaternion_to_euler_angle(imu_file[i, 1:5])[2] for i in range(len(imu_file))]
    yaws = np.diff(yaws)
    rolls = [quaternion_to_euler_angle(imu_file[i, 1:5])[0] for i in range(len(imu_file))]
    rolls = np.diff(rolls)
    pitches = [quaternion_to_euler_angle(imu_file[i, 1:5])[1] for i in range(len(imu_file))]
    pitches = np.diff(pitches)
    yaws = np.insert(yaws, 0, 0) / np.pi*180
    rolls = np.insert(rolls, 0, 0) / np.pi*180
    pitches = np.insert(pitches, 0, 0)/ np.pi*180


    # convert unix epoch time to gnss week time
    # week = (imu_file[:, 0] - 315964800) // 604800
    out_data[:, 0] = (imu_file[:, 0] - 315964800.0) % 604800.0
    out_data[:, 1] = pitches
    out_data[:, 2] = rolls
    out_data[:, 3] = -yaws

    out_data[:, 4] = imu_file[:, 9] * 0.01 # ax
    out_data[:, 5] = imu_file[:, 8] * 0.01
    mean_g = np.mean(imu_file[:, 10])
    print("mean gravity: ", mean_g)
    out_data[:, 6] = -imu_file[:, 10] * 0.01
    # out_data[:, 7] = week.astype(int)

    # convert quaternion to euler angle

    x, y, z, w = imu_file[0, 1:5]
    euler_angle = [np.arctan2(2*(w*x + y*z), 1 - 2*(x**2 + y**2)),
                   np.arcsin(2*(w*y - z*x)),
                   np.arctan2(2*(w*z + x*y), 1 - 2*(y**2 + z**2))]

    print("initial pose: ", euler_angle)

    np.savetxt(out_fn, out_data, delimiter=" ", fmt="%.12f")
