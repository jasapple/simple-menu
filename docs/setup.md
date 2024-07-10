# Setup process

## Environment

- Hardware: Raspberry pi4 or later (for built in WIFI)
- OS: raspbian

## Steps taken
- cloned the repo into `/opt/simple-menu`
- copied simpleMenu.service to `/etc/systemd/system/gunicorn`
- `sudo systemctl enable gunicorn`
- `sudo systemctl start gunicorn`
- `sudo systemctl set-default graphical.target`

    At this point, the service is up and enabled. the following is for a 'self contained' setup with the pi4 is also driving a display

- configure display resolution
- configure networking if needed
- set default browser to chromium

add the following to start chromium on startup:

edit `/home/$USER/.config/wayfire.ini`

add:
```
[autostart]
chromium= chromium-browser http://localhost --start-fullscreen --noerrors --hide-crash-restore-bubble --disable-infobars
```

### Desktop Shortcut

Add the following to the desktop:
file: open_display.desktop

contents:
```
[Desktop Entry]
Name= Open Display
Type=Link
URL=http://localhost
Icon=text-html
```
### simple backup

add file `menu-backup` to `/etc/cron.daily`

add execution permission:
`sudo chmod +x /etc/cron.daily/menu-backup`

contents
```
/usr/bin/tar -zcfP /home/$USER/Documents/menu_backup.tar /opt/simple-menu/instance/menu.db
```


https://www.raspberrypi.com/tutorials/how-to-use-a-raspberry-pi-in-kiosk-mode/