# ![ic.ico](https://raw.githubusercontent.com/amannirala13/Crack-Detection-System/main/img/ic.ico) Crack-Detection-System

This project aims at designing railway track crack detection using an Arduino and Raspberry Pi and Arduino as development boards, which is further connected with a sensor, either an Ultrasonic or IR sensor (in our project it is an ultrasonic sensor module HC-SR04). The purpose is that it detects the distance between objects by using the physical phenomenon of echo, high frequency sound waves are emitted from the sensor which on striking an object bounces back to the receiver in the sensor. In the case of IR sensors, an infra-red blaster is used to emit infrared waves which travel and strike the surface, bounce back to an infra-red sensor. The time taken for the ultrasonic wave or the infra-red wave is used to calculate the distance between the object’s surface which gives us information about any abnormality on the surface of the object.

## Arduino Module:

<img src="https://github.com/amannirala13/Crack-Detection-System/blob/main/img/circuit.png" alt="Arduino Module Circuit Diagram" height="400" width="500">

## Download release:

> #### You can get the latest release for Windows from [**here**](https://github.com/amannirala13/Crack-Detection-System/releases).

## How to use:

There are multiple ways to run the software interface.

### Use installer:

- There are multiple ways to run the software interface. If you are on Windows, the recommended way is to use the download the installer from [**here**](https://github.com/amannirala13/Crack-Detection-System/releases).
  After downloading the installer, install it normally and execute the application.

  > **Note:** Always execute the application as an administrator.

### Build from Script:

- The other way is to use build executables from the source. To build executables from the source you need go to the **`src`** folder and use the **`build.sh`** to build the executables from the source code. Here are few options and examples on how you can use **`build.sh`**.

  > **Note**: For this method the basic requirement is that you need to have **python** and **pip** installed on your computer

  **Options:**

  ```sh
    options:--------------------------------------------------------------------------------------
        -e     : Setup env with just pip      [ build.sh -e ]
        -e -v  : Setup env with specific version of pip       [build.sh -e -v <version_number>]
        -b     : Build executable       [ build.sh -b <python file path> ]
        -f     : Full install with plugin(needs config)     [ build.sh -f -b <python file path> ]
        -m     : Move plugin scripts to build       [ build.sh -m ]
        -h     : Show options      [ build.sh -h ]
    ----------------------------------------------------------------------------------------------

    usage:----------------------------------------------------------------------------------------
    [ build.sh -e ]
    [build.sh -e -v 3]
    [ build.sh -b <python file path> ]
    [ build.sh -f -b <python file path> ]
    [ build.sh -h ]
    ----------------------------------------------------------------------------------------------
  ```

  **Example**

  - To full build (app + plugins) + setup environment packages using python3 and pip3 use the command:

    ```sh
    ./build.sh -e -v 3 -f -b app.py
    ```

    This will create 2 folder in your pwd namely **`./build`** and **`./dist`**. The main executable file is in the dist folder as **`app.exe`** or an executable as per your operating system. Just execute the file to start the application.

- The last option is to execute the source script itself. Since the interface is written in python, if the host system is the python environment with required packages, you can just go to the **`src`** folder and execute the **`app.py`** with the command **`python app.py`** or **`python3 app.py`**. In case your python packages are not setup and you have python and pip installed, you can use the **`build.sh`** script to setup the environment. If you are using python2 just execute the script as **`build.sh -e`** and if you are using python3 with pip3 execute the script with **`build.sh -e -v 3`**.

> **Note**: If **`build.sh`** failed to install the packages,you can do it manually by using pip commands and going through the python scripts in the **`src`** folder to check for the packages used.

---

## Using the application:

The application has a simple interface with minimum options. Lets see what all options do we need to setup.

- The first option is **`COM Port`** which defines which serial port your arduino is connect to.
- The second option is **`Baud Rate`** which defines at what rate the data is transferred through the serial port. With Arduino the standard rate is **`9600`**.
- The third option is **`Depth Sensitivity (cm)`** which defines the magnitude of abnormality on the surface level data above the surface normal (normal level) the interface can tolerate and not classify as a detection. Any value above surface normal + depth sensitivity is classified as a crack.
- The fourth option is **`Max depth allowed (cm)`** which defines what is the maximum surface level value that we will detect. This is to ensure that extreme noisy readings from the sensor don't populate the data and are just discarded.
- The last and final option is **`Calibration Time (s)`** which defines the initial time period for which the system will collect data for calibrating itself for the normal surface level.

With all these options we have provided few action buttons that are self explanatory.

- The **`Calibrate`** button calibrate the system.

- The **`Start/Stop detection`** button is used to start or stop detection.

  > **Note:** Previous data log gets erased as soon as detection start. So make sure to make a backup of **`log.data`** file if you want to use the data for further analysis.

- The **`Show Graph`** button is used to open the live graph of the data collected in realtime.
- The **`Save COM Config`** button is used to save the present COM port and Baud-rate so that you don't need to enter if every time you start the application.
