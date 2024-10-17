## GENERAL
* OS installation is crucial, as any errors during this stage can have serious consequences.
* The error when building WiringPi library often occurs due to missing packages or files in the Linux system. This may happen during the OS installation or if the file system wasn’t updated properly during a system update.if so,
    * try reinstalling OS
    * if make is present in system (installing make)
        https://www.makeuseof.com/how-to-fix-make-command-not-found-error-ubuntu/

## PERIPHERALS
* UART in python and c: https://www.electronicwings.com/raspberry-pi/raspberry-pi-uart-communication-using-python-and-c
* Enabling UART for battery monitoring: https://www.electronicwings.com/raspberry-pi/raspberry-pi-uart-communication-using-python-and-c        
* Default state of gpio pins in raspberry pi : https://roboticsbackend.com/raspberry-pi-gpios-default-state/

## NETWORKS
* how to ON/OFF ethernet/wlan: https://stackoverflow.com/questions/23487728/ethernet-disabling-in-raspberry-pi
* issue: IP V4 is not assigning to ethernet(V6 is present): https://www.freshblurbs.com/blog/2022/08/07/fix-eth0-rpi-ubuntu.html
* Add wifi credentials and ethernet details to the existing system
    * sudo vim  /etc/netplan/50-cloud-init.yaml
    * Add the following content to the file (use Vim editor to make sure consistent indentation)
``` bash
network:
    ethernets:
        eth0:
            dhcp4: true
            optional: true
    version: 2
    wifis:
        wlan0:
            dhcp4: true
            optional: true
            access-points:
                "wifi_name":
                        password: "password"

 ``` 	

    * Then run ,to know if it is working
	    * sudo netplan generate
        * sudo netplan apply	


