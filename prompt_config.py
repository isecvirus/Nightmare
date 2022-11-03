from prompt_toolkit.styles import Style

prompt_style = Style.from_dict({
    'prompt': '#6600ff bold',
    # 'rprompt': 'fg:grey bold',

    'bottom-toolbar': 'fg:#000000',

    'completion-menu.completion': 'bg:#9800ff #ffffff', # All background of the completion menu
    # 'completion-menu.meta.completion': 'bg:#03919e #ffffff', # Don't know

    'completion-menu.completion.current': 'bg:#86659a #ffffff', # Current stand on option in the completion menu
    'completion-menu.meta.completion.current': 'bg:#86659a #ffffff',

    'scrollbar.background': 'bg:#7f0092',
    'scrollbar.button': 'bg:#86659a',
    'scrollbar.arrow': 'bg:#974cb3',

    # "username": "#aaaaaa italic",
    # "path": "#ffffff bold",
    # "current-module": "#04ff00 bg:#666666",
    # "current-tool": "#fff200 bg:#666666",
    # "tool-last-modification-date": "#002345 bg:#666666",
    # "left-part": "bg:#444444",
    # "right-part": "bg:#444444",
    # "padding": "bg:#444444",
    #
    'auto-suggestion': '#8c7389 bg:default noreverse noitalic nounderline noblink',  # '#de8d00',

    "aborting": "#888888 bg:default noreverse noitalic nounderline noblink",
    "exiting": "#888888 bg:default noreverse noitalic nounderline noblink",

    # 'control-character': 'ansiblue',
    # 'search': 'ansiblue',

    # "command1-style": "#00a11a bold",
    # "argument1-style": "#ff00f2",
    # "argument2-style": "#00cfc4",
    # "search-command-style": "#00a11a bold",
    # "search-for-style": "grey",

    # "module-set-style": "#04ff00 bold",
    # "tool-set-style": "#fff200 bold",

    # "tool-opt-arg1-style": "#00636e bold",
    # "option-set-style": "gold bold", # #ffffff is white (pure white)

    # "true-opt-style": "#086e00 bold",
    # "false-opt-style": "#a81919 bold",

    # "arg1-command-style": "#00a11a bold",
    # "arg2-command-style": "#00cfc4",

    # "ip-style": "yellow",
    # "python3-code-style": "#ffbf00 bold",

    # "cmd-user-style": "#eb3496 bold",
    # "cmd-root-style": "#ebae34 bold",
    # "comment-style": "grey bold",

    # "trailing-input": "#ff1500 bold",  # wrong input color Background & Foreground
})