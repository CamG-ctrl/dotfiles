#~/bin/env bash

# Options with JetBrains Nerd Font icons
lock=" : Lock"
logout="󰍃 : Logout"
sleep="󰤄 : Sleep"
reboot=" : Reboot"
shutdown="⏻ : Shutdown"

# Combined choices
options="$lock\n$logout\n$sleep\n$reboot\n$shutdown"

# Run Rofi with a clean, grid style configuration
chosen=$(echo -e "$options" | rofi -dmenu \
    -i \
    -p "Power" \
    -theme-str 'window {width: 250px;} listview {lines: 5;}')

# Execute action based on choice
case "$chosen" in
    "$lock")
        loginctl lock-session
        ;;
    "$logout")
        qtile cmd-obj -o cmd -f shutdown
        ;;
    "$sleep")
        systemctl suspend
        ;;
    "$reboot")
        systemctl reboot
        ;;
    "$shutdown")
        systemctl poweroff
        ;;
esac

