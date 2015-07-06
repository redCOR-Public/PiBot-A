INSTALLATION PIBOT-A

1. Installiere einen Web-Server (z. B. lighttpd)

2. Autorisiere den WWW-User in /etc/sudoers fuer robot.sh:
   www-data ALL=NOPASSWD: /home/pi/robot/robot.sh

3. Entpacke den Tarball in einem Temporaerverzeichnis

4. Kopiere die Dateien wie folgt (Zielverzeichnisse
   ggf. vorher anlegen):
   a) led0 => /home/pi/io
   b) robot.php, robot.css, logo.png => /var/www
   c) alle anderen => /home/pi/robot

5. Installiere die Pololu-Software in /home/pi/robot von:
   https://github.com/pololu/drv8835-motor-driver-rpi

6. Starte button-py in /etc/rc.local als Daemon:
   /home/pi/robot/button.py <&- >/dev/null 2>&1 &

7. Reboot

TEST:

Fuer einen ersten Test kann man robot-rt.py benutzen.
Sensoren sind nicht anzuschliessen, der Roboter faehrt
immerfort Rechts-Links-Kurven:

1. cd /home/pi/robot
2. sudo ./robot.sh rt
3. sudo ./robot.sh start

Thomas Schoch - www.retas.de - Version: 2015-06-06
