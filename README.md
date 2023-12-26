# Compatible with Intel's d455 ENVIO odometry

## Build

- This package was tested on **Ubuntu 16.04 (ROS Kinetic)** with **Eigen 3.3.7** for matrix computation and **OpenCV 3.3.1-dev** for image processing in **C++11**.

- We use the catkin build system :

```
cd catkin_ws
catkin_make
```

## Run ([EuRoC](https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets) example)

- Configuration and launch files are prepared in `config/euroc/camchain-imucam-euroc.yaml` and `launch/nesl_envio_euroc.launch`.
- The configuration files are output by [Kalibr](https://github.com/ethz-asl/kalibr) toolbox.
- Filter and image processing parameters are set from the launch file.
- **Please note that our filter implementation requires static state at the beginning to initialize tilt angles, velocity and gyroscope biases.** The temporal window for this process can be set by `num_init_samples` in the launch file.
- As default our package outputs `est_out.txt` that includes estimated states.
- Note forget  ./source/devel/setup.bash

```
roslaunch ensemble_vio nesl_envio_euroc.launch
roslaunch ensemble_vio nesl_envio_rviz.launch
rosbag play rosbag.bag
```

<img src="https://telegraph-image-6yo.pages.dev/file/ff6a66bda4376279253a8.png" alt="image-20231226165349363" style="zoom:67%;" />

## Run your own device

**参考博客https://zhaoxuhui.top/ 感谢前辈的付出**

- this implementation assumes that stereo camera is hardware-synced and the spatio-temporal parameters for cameras and IMU are calibrated as it is a critical step in sensor fusion.
- You can calibrate your visual-inertial sensor using [Kalibr](https://github.com/ethz-asl/kalibr) toolbox and place the output file in `config`.
- The input ROS topics and filter parameters are set in `launch`.
- With low cost IMUs as in EuRoC sensor suite, you can use the default parameters of EuRoC example file.

## Run on my intel d455

### 自动采集制作rosbag

代码文件为d455_stage_dataCollect.py

```python
# coding=utf-8
import os
import sys
import time


def checkPythonVersion():
    return float(sys.version[:3])

if __name__ == '__main__':
    head_str = "gnome-terminal -x bash -c "

    # step 1 启动相机
    step1_com = head_str+r"'roslaunch realsense2_camera rs_camera.launch'"
    print("==> Launching Intel Realsense D435i camera ...")
    os.system(step1_com)

    # step2 关闭红外发射器
    # python2, python3 input()函数不一样,需要分别处理
    python_v = checkPythonVersion()
    if python_v == 3:
        user_input = input("Reconfigure Intel Realsense D455 camera? [y]/n")
    else:
        user_input = raw_input("Reconfigure Intel Realsense D455 camera? [y]/n")
    if user_input == '' or user_input == 'y' or user_input == 'Y':
        step2_com = head_str+r"'rosrun rqt_reconfigure rqt_reconfigure'"
        print("==> Reconfiguring Intel Realsense D435i camera ...")
        os.system(step2_com)
    
        python_v = checkPythonVersion()
        if python_v == 3:
            configure_rst = input("Finished configuration? [y]/n")
        else:
            configure_rst = raw_input("Finished configuration? [y]/n")
        if configure_rst == '' or configure_rst == 'y' or configure_rst == 'Y':
            print("==> Reconfiguration finished.")

    # step3 可视化数据
    step3_1_com = head_str+r"'rqt_image_view /camera/color/image_raw'"
    step3_2_com = head_str+r"'rqt_image_view /camera/aligned_depth_to_color/image_raw'"
    #step3_2_com = head_str+r"'rqt_image_view /camera/infra1/image_rect_raw'"
    step3_3_com = head_str+r"'rqt_image_view /camera/infra2/image_rect_raw'"
    os.system(step3_1_com)
    os.system(step3_2_com)
    os.system(step3_3_com)
    python_v = checkPythonVersion()
    if python_v == 3:
        user_input = input("Visualize images OK? [y]/n")
    else:
        user_input = raw_input("Visualize images OK? [y]/n")
    if user_input == '' or user_input == 'y' or user_input == 'Y':
        print("==> Visualization OK")

    # step4 录制数据
    bag_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+".bag"
    #step4_com = r"rosbag record /camera/color/image_raw /camera/imu /camera/infra1/image_rect_raw /camera/infra2/image_rect_raw -O "+bag_str
    #step4_com = r"rosbag record /camera/imu /camera/infra1/image_rect_raw /camera/infra2/image_rect_raw -O "+bag_str
    step4_com = r"rosbag record /camera/imu /camera/color/image_raw /camera/aligned_depth_to_color/image_raw -O "+bag_str
    python_v = checkPythonVersion()
    if python_v == 3:
        user_input = input("Start recording color, infra(left), infra(red) and IMU stream? [y]/n")
    else:
        user_input = raw_input("Start recording color, infra(left), infra(red) and IMU stream? [y]/n")
    if user_input == '' or user_input == 'y' or user_input == 'Y':
        print("==> Start recording ...")
        os.system(step4_com)

```

### 实时运行采集和里程计

代码文件run.py

```python
# coding=utf-8
import os
import sys
import time


def checkPythonVersion():
    return float(sys.version[:3])

if __name__ == '__main__':
    head_str = "gnome-terminal -- bash -c "

    # step 1 source
    step1_com = head_str+r"'source /home/juo/myenvio_ws/devel/setup.bash'"
    print("==> sourcing ...")
    os.system(step1_com)
    # step 2 启动相机
    step2_com = head_str+r"'roslaunch realsense2_camera rs_camera.launch'"
    print("==> Launching Intel Realsense D455camera ...")
    os.system(step2_com)


    # step3 关闭红外发射器
    # python2, python3 input()函数不一样,需要分别处理
    python_v = checkPythonVersion()
    user_input = input("Reconfigure Intel Realsense D455 camera? [y]/n")
 
    if user_input == '' or user_input == 'y' or user_input == 'Y':
        step3_com = head_str+r"'rosrun rqt_reconfigure rqt_reconfigure'"
        print("==> Reconfiguring Intel Realsense D435i camera ...")
        os.system(step3_com)
    
        python_v = checkPythonVersion()
        print(python_v)
        configure_rst = input("Finished configuration? [y]/n")
        if configure_rst == '' or configure_rst == 'y' or configure_rst == 'Y':
            print("==> Reconfiguration finished.")

    # step 4 启动ENVIO
    step4_com = head_str+r"'roslaunch ensemble_vio nesl_envio_d455.launch'"
    print("==> Launching ENVIO ...")
    os.system(step4_com)
    # step 5 启动RVIZ
    step5_com = head_str+r"'roslaunch ensemble_vio nesl_envio_rviz.launch'"
    print("==> Launching RVIZ ...")
    os.system(step5_com)


```

## 参考资料 感谢前辈的付出

[1]: https://zhaoxuhui.top/blog/2020/09/09/intel-realsense-d435i-installation-and-use.html
[2]: https://www.mouser.cn/applications/getting-started-with-realsense-d455/

[3]: https://zhaoxuhui.top/blog/2021/11/21/script-for-data-collection-and-postprocessing-with-d435i.html

[4]: https://zhaoxuhui.top/blog/2020/09/25/intel-realsense-D435i-ROS-API-notes.html
