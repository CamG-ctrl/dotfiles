#!/bin/sh
picom &
dunst &
nm-applet &
flameshot &
blueman-applet &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
xss-lock --transfer-sleep-lock -- ~/.config/qtile/lock.sh &
feh --no-fehbg --bg-fill ~/Pictures/wallpaper.png &
xrandr --output DP-0 --mode 2560x1440 --rate 180 --primary --output DP-4 --mode 1920x1080 --rate 100 --left-of DP-0 --rotate left
