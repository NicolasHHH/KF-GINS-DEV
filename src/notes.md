
1. 引擎参数初始化 


    GIEngine giengine(options);


2. 构造输出文件 + publishers


    int nav_columns = 11, imuerr_columns = 13, std_columns = 22;
    FileSaver navfile(outputpath + "/KF_GINS_Navresult.txt", nav_columns, FileSaver::TEXT);
    FileSaver imuerrfile(outputpath + "/KF_GINS_IMU_ERR.txt", imuerr_columns, FileSaver::TEXT);
    FileSaver stdfile(outputpath + "/KF_GINS_STD.txt", std_columns, FileSaver::TEXT);

    // publishers :
    // 1. pose -> geometry_msgs::PoseStamped
    // 2. odom -> nav_msgs::Odometry


3.  ~~检查文件是否正确打开~~ -> 订阅话题


    // subscribers
    // 1. imu -> sensor_msgs::Imu
    // 2. gnss -> sensor_msgs::NavSatFix
    // 3. uwb -> uwb_msgs 


4.  初始状态 ： 添加IMU数据到GIEngine中，补偿IMU零偏和比例因子误差


    // add imudata to GIEngine and compensate IMU error
    giengine.addImuData(imu_cur, true);

    // 添加GNSS数据到GIEngine
    // add gnssdata to GIEngine
    giengine.addGnssData(gnss);


5. 主循环
    - 需要添加 imu 和 gnss buffer 吗？
      - 好处：可以应用fixed lag smoother， 以及对时间戳插值，
      - 坏处：增加了复杂度，如何和ros自带的buffer兼容 ？ 
      - 结论：总需要至少一个buffer，要不用IMU消息驱动，但需要存储GNSS信息；要不用主循环驱动，需要存储两者信息。 
    - 消息处理速度太慢怎么办？
      - 可能情况： 丢帧或者消息堆积。 
      - imu丢帧的话，DR就不连续了；增大GNSS的权重？ 
      - gnss丢帧的话，丢就丢了。但有效信息丢失还是一种损失。
      - 解决办法 ？ 
      - 消息堆积： 
      - 停下来？ 或者rebase ？ 



    while (ros::ok()) {

        
        giengine.addGnssData(gnss);
        imu_cur = imufile.next();
        giengine.addImuData(imu_cur);

        giengine.newImuProcess(); // 主要是这里 更新和预测在一起？ 

        // 后面都是些次要的东西。
    }

6. 注释

GNSS的更新与否取决于是否有新的add，这个信息存在变量：`gnssdata.isvalid`里。 每当`add`时`True`， 更新后变为`False`。
如果有新GNSS也就是`isvalid`为`True`时，更新时间戳以GNSS时间戳为准。

`isToUpdate` 用于判断是否需要更新，判断GNSS时间戳和IMU戳的关系。