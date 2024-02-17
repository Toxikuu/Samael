# ***Samael***
# Intro
    Samael is a terminal-based free and open source duels antisniper.
    This means you can change whatever you want about the code, make forks, and share it freely.
    It is meant to be used alongside Lilith.
    You're allowed to repurpose any code in Samael into your own projects.
    If someone sold you Samael, you got played lmao.
    If you decide to make a fork of Samael, kindly refrain from adding malware.
    Also, consider making your forks FOSS aswell!
    Samael is licensed under the MIT License.

# Prerequisites
    I recommend windows terminal.
    The default command prompt doesn't show colors for some people.

# Installation
    Run SamaelInstall.bat.

# Config
    You'll have to edit the config.ini after running the install script.
    See the comments within the file for more information.
    
# Lists
    Blacklist stores UUIDs of players Samael shows as blacklisted.
    Safelist stores UUIDs of players Samael shows as safelisted.
    Weirdlist stores UUIDs of players Samael shows as weirdlisted. (Think of this like a risky tag whereas blacklist is a sniper tag.)
    Notes stores the notes you make.
    Record keeps track of who you win and lose to.
    This is used to automatically safelist or blacklist players.
 
# Launching
    Once you've set up and configured Samael, run it with:
    python your/samael/path/samael.py
    (or you can double click samael.py)
    I'll upload a Samael.bat to launch Samael from its default directory soonish.

# Commands
    Samael commands use the following format (typed in Minecraft chat): /fakechat -command argument.
    Additionally, ^ or ^^ may be used in place of an ign to target the previous or previous previous opponent.
    Ex. /fakechat -note ^ "might be cheating ~ will make that note of the last opponent you fought.
    Samael adds the following commands:
    /fakechat -s ign ~ safelists a player ~ ex. /fakechat -s toxikuu
    /fakechat -b ign ~ blacklists a player ~ ex. /fakechat -b toxikuu
    /fakechat -w ign ~ weirdlists a player  ~ ex. /fakechat -w toxikuu
    /fakechat -rs ign ~ removes a player from safelist ~ ex. /fakechat -rs toxikuu
    /fakechat -rb ign ~ removes a player from blacklist ~ ex. /fakechat -rb toxikuu
    /fakechat -rs ign ~ removes a player from safelist ~ ex. /fakechat -rs toxikuu
    /fakechat -rw ign ~ removes a player from weirdlist ~ ex. /fakechat -rw toxikuu
    /fakechat -api apikey ~ replaces the apikey in the config with the apikey argument ~ ex. /fakechat -api 681e5ab5-e6b6-4d13-9550-4e6e26af1cc9
    /fakechat -refresh ~ reloads the config
    /fakechat -reload ~ alias of -refresh
    /fakechat -dd ~ fixes list formatting (removes duplicate entries and white space)
    /fakechat -filter ~ filters safelist and blacklist entries; ie if a player is both in the safelist and blacklist, they are removed from the safelist. Also runs -dd afterwards, fixing list formatting after removing entries.
    /fakechat -note ign "note ~ allows you to make custom notes for a specific player (open the quote before your note, but do not close it) ~ ex. /fakechat -note toxikuu "sedge alt
    /fakechat -nick nick ~ adds your nick to the config ~ ex. /fakechat -nick Maria687
    /fakechat -delimiter 0 ~ changes delimiter type to 0; other valid argument is 1
    /fakechat -dev ~ toggles devmode
    /fakechat -toggle stat ~ toggles a Samael stat (view stat toggles in the config for a list of valid arguments) (allon and alloff are also arguments)
    /fakechat -show_own_stats ~ toggles show_own_stats
    
# Additional Resources
    Discord: https://discord.gg/N3rVjjVEsv
    If you have any issue with the setup, ask in ⁠#help.
    If you want coding help when adding new features or customizing Samael, ask in ⁠#coding-help.
    The latest version of Samael will be available in ⁠#downloads.
    You do not need to be running the latest version of Samael, since it's all stored locally.
    Newer versions will just be more up-to-date.
