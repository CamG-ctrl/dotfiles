import os
import subprocess

from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"            # Super / Windows key
font_size = 16          # bar text in pixels; raise it (e.g. 24) on HiDPI screens
bar_height = font_size + 14   # bar grows with the text
terminal = "alacritty"

# Tokyo Night (night) palette
c = {
    "bg": "#1a1b26", "bg_dark": "#16161e", "bg_hl": "#292e42",
    "fg": "#c0caf5", "comment": "#565f89", "blue": "#7aa2f7",
    "cyan": "#7dcfff", "green": "#9ece6a", "magenta": "#bb9af7",
    "orange": "#ff9e64", "red": "#f7768e", "yellow": "#e0af68",
}

keys = [
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "d", lazy.spawn("rofi -show drun")),
    Key([mod, "shift"], "q", lazy.spawn("/home/cam/.config/rofi/powermenu.sh", shell=True)),
    Key([mod], "e", lazy.spawn("thunar")),
    Key([mod], "b", lazy.spawn("firefox")),
    Key([mod], "p", lazy.spawn("flameshot gui")),
    Key([mod, "shift"], "x", lazy.spawn("loginctl lock-session")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "space", lazy.window.toggle_floating()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume -l 1.0 @DEFAULT_AUDIO_SINK@ 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 5%+")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
]

# Workspaces span both monitors: workspace 1 is group "1a" on the main monitor
# and "1b" on the second, and Super + 1 switches both at once.
# With one monitor (the ThinkPad on its own) only the "a" set is used.
workspaces = "123456789"
monitors = "ab"            # one letter per monitor; add "c" for a third
groups = [Group(n + m, label=n, screen_affinity=i)
          for n in workspaces for i, m in enumerate(monitors)]


def go_to(qtile, n):
    for i in range(min(len(qtile.screens), len(monitors))):
        qtile.groups_map[n + monitors[i]].toscreen(i)


def send_to(qtile, n):
    win = qtile.current_window
    if win:
        win.togroup(n + monitors[qtile.current_screen.index])   # stays on its monitor
    go_to(qtile, n)


for n in workspaces:
    keys += [
        Key([mod], n, lazy.function(go_to, n)),
        Key([mod, "shift"], n, lazy.function(send_to, n)),
    ]

borders = dict(border_width=2, margin=6,
               border_focus=c["blue"], border_normal=c["bg_hl"])
layouts = [
    layout.Columns(**borders, border_focus_stack=c["magenta"]),
    layout.Max(**borders),
]
floating_layout = layout.Floating(
    border_width=2, border_focus=c["magenta"], border_normal=c["bg_hl"],
    float_rules=[*layout.Floating.default_float_rules,
                 Match(wm_class="pavucontrol"),
                 Match(wm_class="blueman-manager")],
)

widget_defaults = dict(font="JetBrainsMono Nerd Font", fontsize=font_size, padding=6,
                       background=c["bg"], foreground=c["fg"])
extension_defaults = widget_defaults.copy()


def sep():
    # thin, short divider between widgets
    return widget.Sep(linewidth=1, padding=8, size_percent=50, foreground=c["comment"])


def status_widgets(s):   # s = monitor number, 0 = main
    w = [
        widget.GroupBox(highlight_method="line", highlight_color=[c["bg"], c["bg"]],
                        this_current_screen_border=c["blue"], this_screen_border=c["comment"],
                        other_current_screen_border=c["magenta"], other_screen_border=c["comment"],
                        active=c["fg"], inactive=c["comment"],
                        urgent_border=c["red"], urgent_text=c["red"], disable_drag=True,
                        visible_groups=[n + monitors[s] for n in workspaces]),   # this monitor's 1-9
        widget.CurrentLayout(foreground=c["cyan"]),
        sep(),
        # window icons only; click one to focus it
        widget.TaskList(highlight_method="block", border=c["bg_hl"], urgent_border=c["red"],
                        foreground=c["fg"], rounded=False, icon_size=font_size,
                        parse_text=lambda text: "",
                        txt_floating="", txt_minimized="", txt_maximized="",
                        stretch=False),   # only as wide as its icons
        sep(),
        widget.WindowName(foreground=c["comment"]),   # focused window's title fills the free space
        widget.CPU(format="CPU:{load_percent}%", foreground=c["green"]),
        sep(),
        widget.Memory(format="MEM: {MemPercent}%", foreground=c["yellow"]),
        sep(),
    ]
    if os.path.exists("/sys/class/power_supply/BAT0"):
        w += [widget.Battery(format="bat {percent:2.0%} {char}", foreground=c["orange"],
                             low_foreground=c["red"]),
              sep()]
    w += [
        # PipeWire volume: scroll = +/-5%, left-click = mute, right-click = pavucontrol
        widget.Volume(fmt="VOL: {}", foreground=c["magenta"], update_interval=1,
                      get_volume_command="wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk '{printf \"%.0f%%\", $2 * 100}'",
                      check_mute_command="wpctl get-volume @DEFAULT_AUDIO_SINK@",
                      check_mute_string="[MUTED]",
                      mute_command="wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle",
                      volume_up_command="wpctl set-volume -l 1.0 @DEFAULT_AUDIO_SINK@ 5%+",
                      volume_down_command="wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-",
                      volume_app="pavucontrol"),
        sep(),
        *([widget.Systray(), sep()] if s == 0 else []),   # only one tray allowed: main monitor
        widget.Clock(format="%a %d %b  %H:%M", foreground=c["blue"]),
    ]
    return w


screens = [Screen(top=bar.Bar(status_widgets(s), bar_height, background=c["bg"], margin=[6, 6, 0, 6]))
           for s in range(len(monitors))]   # one bar per monitor

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True           # games go fullscreen properly
focus_on_window_activation = "smart"
wmname = "LG3D"                  # fixes some Java apps


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/autostart.sh")])
