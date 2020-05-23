E4S_IoT_D-R

This Project uses the MPU-6050 module to track a user's acceleration and to identify a fall. Should a fall event be detected, an email is sent from the project's email account to the caregiver's email. Depending on the user's mobility, the Thresholds may need to be changed. The program continuously is reading data from the accelerometer as long as the script is running. 

The program was compiled on a Raspberry Pi running the Raspberian OS and had the following connections: VCC -> Pin #4, GND
-> Pin #34, SCL -> Pin #5, SDA -> Pin #3.

Line 108 requires email credentials that need to be entered
