'''
Descripttion: 
version: 
Author: xp.Zhang
Date: 2023-12-11 16:58:21
LastEditors: xp.Zhang
LastEditTime: 2023-12-11 17:33:22
'''
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

