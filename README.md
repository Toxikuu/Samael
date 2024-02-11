# ***Samael***
# Intro
    Samael is a terminal-based free and open source duels antisniper. This means you can change whatever you want about the code, make forks, and share it freely.
    It is meant to be used alongside Lilith.
    You're allowed to repurpose any code in Samael into your own projects.
    If someone sold you Samael, you got played lmao.
    If you decide to make a fork of Samael, kindly refrain from adding malware. Also, consider making your forks FOSS aswell!
    Samael is licensed under the MIT License.

# Prerequisites
    To use Samael, you need to have Python installed. It's also recommended that you add Python to path, and that you use an IDE (examples: VSCode, Neovim, IntelliJ, etc.) to modify the code.
    I also highly recommend Windows Terminal to launch it as it makes your life much easier (it fixes weird color and formatting issues).
    Additionally, you need to have the requests python module installed. This can be installed by running "pip install requests" in your terminal.

# Setup
    Create a folder called Samael, and within that another folder called Lists.
    Place your samael.py and config.ini files into the Samael folder.
    Create 5 new files in the Lists folder:
    Safelist.txt, blacklist.txt, weirdlist.txt, record.txt, and notes.txt.

# Config
    Open config.ini. Add in your hypixel apikey and username. You can disable devmode if you don't want debug information. Under paths, set the paths of your lists to their respective paths (should be in the Lists folder from the setup). For chat, locate the latest.log for your client (for lunar, this should be C:/Users/User/.lunarclient/offline/multiver/logs/latest.log). The location of latest.log varies depending on your minecraft client. If you don't want to be notified of specific nicks, you may add their nicks to safenicks. Rounding_precision indicates how many digits after the decimal will be displayed. Show_splash_screen toggles the Samael splashcreen on launch; set show_splash_screen = n to toggle it off. Delimiter type changes the delimiter Samael looks uses to parse names from latest.log. If Samael isn't showing stats, try setting delimiter_type = 1 instead of 0.
    
# Lists
    Blacklist stores UUIDs of players Samael shows as blacklisted.
    Safelist stores UUIDs of players Samael shows as safelisted.
    Weirdlist stores UUIDs of players Samael shows as weirdlisted. (Think of this like a risky tag whereas blacklist is a sniper tag.)
    Record keeps track of who you win and lose to. This is used to automatically safelist or blacklist players.
    Notes stores the notes you make.
 
# Launching
    Once you've set up and configured samael, run it with:
    python <your samael.py path>
    Or create a launch.bat with the python run command.

# Commands
    Samael commands use the following format (typed in Minecraft chat): /fakechat -command argument.
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
    /fakechat -dd ~ fixes list formatting (removes duplicate entries and white space)
    /fakechat -clr ~ wipes record
    /fakechat -filter ~ filters safelist and blacklist entries; ie if a player is both in the safelist and blacklist, they are removed from the safelist. Also runs -dd afterwards, fixing list formatting after removing entries.
    /fakechat -note ign "note ~ allows you to make custom notes for a specific player (open the quote before your note, but do not close it) ~ ex. /fakechat -note toxikuu "sedge alt
    
# Additional Resources
    Discord: https://discord.gg/N3rVjjVEsv
    If you have any issue with the setup, ask in ⁠#help.
    If you want coding help when adding new features or customizing Samael, ask in ⁠#coding-help.
    The latest version of Samael will be available in ⁠#downloads. You do not need to be running the latest version of Samael, since it's all stored locally. Newer versions will just be more up-to-date.
