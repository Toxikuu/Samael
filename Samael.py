# import libraries
import math, time, os, sys, configparser, re, threading, requests
from datetime import datetime; from dhooks import Webhook

# variables
version = '5.0.6'
discord = "https://discord.gg/N3rVjjVEsv"
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
config_file = f'{script_directory}/config.ini'
config_ini = configparser.ConfigParser()
# if i ever decide to implement it, user can be automatically gotten with getpass.getuser() using import getpass

# colors
class c:
    Default      = "\033[39m"
    Black        = "\033[30m"
    Red          = "\033[31m"
    Green        = "\033[32m"
    Yellow       = "\033[33m"
    Blue         = "\033[34m"
    Magenta      = "\033[35m"
    Cyan         = "\033[36m"
    LightGray    = "\033[37m"
    Pink         = "\033[38m"
    DarkGray     = "\033[90m"
    LightRed     = "\033[91m"
    LightGreen   = "\033[92m"
    LightYellow  = "\033[93m"
    LightBlue    = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan    = "\033[96m"
    White        = "\033[97m"

    bgDefault      = "\033[49m"
    bgBlack        = "\033[40m"
    bgRed          = "\033[41m"
    bgGreen        = "\033[42m"
    bgYellow       = "\033[43m"
    bgBlue         = "\033[44m"
    bgMagenta      = "\033[45m"
    bgCyan         = "\033[46m"
    bgLightGray    = "\033[47m"
    bgPink         = "\033[48m"
    bgDarkGray     = "\033[100m"
    bgLightRed     = "\033[101m"
    bgLightGreen   = "\033[102m"
    bgLightYellow  = "\033[103m"
    bgLightBlue    = "\033[104m"
    bgLightMagenta = "\033[105m"
    bgLightCyan    = "\033[106m"
    bgWhite        = "\033[107m"

    stBold               = "\033[1m"
    allDefault           = "\033[0m"

tDanger = f'{c.White}{c.bgRed}DANGER{c.allDefault}'
tRisky = f'{c.Yellow}Risky{c.allDefault}'
tSafe = f'{c.White}Safe{c.allDefault}'

prevOpponents = []

# config
def readcfg():
    with open(config_file, 'r') as file_object:
        config_ini.read_file(file_object)
        global cfg
        class cfg:
            # [apikey]
            apikey = config_ini.get('apikey', 'apikey')

            # [user]
            samaeluser = config_ini.get('user', 'username')
            nick = config_ini.get('user', 'nick')

            # [devmode]
            devmode = config_ini.getboolean('devmode', 'dev')

            # [paths]
            blacklist = config_ini.get('paths', 'blacklist')
            safelist = config_ini.get('paths', 'safelist')
            weirdlist = config_ini.get('paths', 'weirdlist')
            record = config_ini.get('paths',  'record')
            chat = config_ini.get('paths', 'chat')
            notes = config_ini.get('paths', 'notes')
            hourly = config_ini.get('paths', 'hourly')
            
            # [safenicks]
            safenicks = config_ini.get('safenicks', 'safenicks')
            safenicks = list(safenicks.split(', ')) # fixes formatting

            # [options]
            rounding_precision = config_ini.getint('options', 'rounding_precision')
            show_own_stats = config_ini.getboolean('options', 'show_own_stats')

            # [autolist]
            autosafelist_win_count = config_ini.getint('autolist', 'autosafelist_win_count')
            autoblacklist_loss_count = config_ini.getint('autolist', 'autoblacklist_loss_count')

            # [delimiter]
            delimiter_type = config_ini.getint('delimiter', 'delimiter_type')

            # [stat toggles]
            nwl = config_ini.getboolean('stat toggles', 'nwl')
            
            sw_star = config_ini.getboolean('stat toggles', 'sw_star')
            sw_kdr = config_ini.getboolean('stat toggles', 'sw_kdr')

            bw_star = config_ini.getboolean('stat toggles', 'bw_star')
            bw_fkdr = config_ini.getboolean('stat toggles', 'bw_fkdr')
            bw_bblr = config_ini.getboolean('stat toggles', 'bw_bblr')
            bw_kdr = config_ini.getboolean('stat toggles', 'bw_kdr')
            bw_fksperstar = config_ini.getboolean('stat toggles', 'bw_fksperstar')

            sumo_wlr = config_ini.getboolean('stat toggles', 'sumo_wlr')
            sumo_bws = config_ini.getboolean('stat toggles', 'sumo_bws')
            sumo_cws = config_ini.getboolean('stat toggles', 'sumo_cws')

            uhc_wlr = config_ini.getboolean('stat toggles', 'uhc_wlr')
            uhc_kdr = config_ini.getboolean('stat toggles', 'uhc_kdr')

            duels_wlr = config_ini.getboolean('stat toggles', 'duels_wlr')
            duels_wins = config_ini.getboolean('stat toggles', 'duels_wins')
            duels_losses = config_ini.getboolean('stat toggles', 'duels_losses')
            duels_bws = config_ini.getboolean('stat toggles', 'duels_bws')
            duels_cws = config_ini.getboolean('stat toggles', 'duels_cws')

            melee_accuracy = config_ini.getboolean('stat toggles', 'melee_accuracy')
            combo_melee_accuracy = config_ini.getboolean('stat toggles', 'combo_melee_accuracy')

            wh_enabled = config_ini.getboolean('webhook', 'wh_enabled')
            if wh_enabled:
                webhook = config_ini.get('webhook', 'webhook')
                interval = config_ini.getint('webhook', 'interval')

readcfg()
cfg_toggles = ['nwl', 'sw_star', 'sw_kdr', 'bw_star', 'bw_fkdr', 'bw_bblr', 'bw_kdr', 'bw_fksperstar', 'sumo_wlr', 
               'sumo_bws', 'sumo_cws', 'uhc_wlr', 'uhc_kdr', 'duels_wlr', 'duels_wins', 'duels_losses', 'duels_bws', 'duels_cws', 'melee_accuracy',  'combo_melee_accuracy']

# clear hourly
if cfg.wh_enabled:
    with open(cfg.hourly, 'w') as clrhr:
        clrhr.write('')

# delimiter fix
if cfg.delimiter_type == 0:
    delimiter = '▌'
elif cfg.delimiter_type == 1:
    delimiter = '?'
    
if cfg.devmode: print(f'Delimiter type: {delimiter}')

# main lists
samael_lists = [cfg.blacklist, cfg.safelist, cfg.weirdlist]

# devmode
if cfg.devmode:
    print('Launching in devmode\n\n')
    with open(config_file, 'r') as file_object_dev:
        config_data_dev = file_object_dev.read()
    print(config_data_dev)

# some functions
def getInfo(call):
    r = requests.get(call)
    return r.json()

def igntouuid(ign):
    try:
        pdb = getInfo(f"https://playerdb.co/api/player/minecraft/{ign}")
        uuid = pdb["data"]["player"]["raw_id"]
        return uuid
    except:
        print(f'\n{c.LightRed} >> {c.bgRed}{c.Black} Failed to access uuid for {ign}! {c.allDefault}{c.LightRed} <<{c.allDefault}')

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.04)
            continue
        yield line

def countOf(list, x):
    count = 0
    for element in list:
        if element == x:
            count += 1
    return count

def filter_lists():
    with open(cfg.safelist, 'r') as slist:
        s_lines = slist.readlines()

    for s_line in s_lines:
        s_line = s_line.strip()
        b_count = count_specific_strings_in_file(cfg.blacklist, s_line)
        w_count = count_specific_strings_in_file(cfg.weirdlist, s_line)

        if b_count > 0 or w_count > 0:
            print(f"> Filtering {s_line}")
            with open(f"{cfg.safelist}", "r") as findsl:
                data = findsl.read()
                data = data.replace(s_line, '\n')
            with open(f"{cfg.safelist}", "w") as findsl:
                findsl.write(data)

def remove_element(lst, element_to_remove):
    return [item for item in lst if item != element_to_remove]

def write_list_to_txt(lst, filename):
    with open(filename, 'w') as file:
        for item in lst:
            file.write(str(item) + '\n')

def remove_empty_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Remove empty lines
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    with open(filename, 'w') as file:
        file.writelines('\n'.join(non_empty_lines))

def remove_none(filename):
    with open(filename, 'r') as f:
        filedata = f.read()
        filedata = filedata.replace('None', '')
    with open(filename, 'w') as f:
        f.write(filedata)

def set_all_true_in_section(section):
    for option in config_ini.options(section):
        config_ini.set(section, option, 'True')
        with open(config_file, 'w') as file_object:
            config_ini.write(file_object)

def set_all_false_in_section(section):
    for option in config_ini.options(section):
        config_ini.set(section, option, 'False')
        with open(config_file, 'w') as file_object:
            config_ini.write(file_object)

# dd fixes file formatting (removes None, \n, and duplicate uuids)
def dd(file):
    remove_none(file)
    with open(file, 'r') as input:
        lines = input.readlines()
        lines = list(dict.fromkeys(lines))
        write_list_to_txt(lines, file)
    remove_empty_lines(file)
    with open(file, 'a') as f:
        f.write('\n')

def omgnick():
    print(f"\n\n{c.bgDefault}{c.LightMagenta}      -----------------------------    ")
    print(f"{c.LightMagenta} >> {c.bgMagenta}{c.Black} NICK OMG WTF DODGE NICK DODGE!! {c.bgDefault}{c.LightMagenta} <<")
    print(f"{c.bgDefault}{c.LightMagenta}      -----------------------------    {c.White}")

# Hourly dependencies
if cfg.wh_enabled:

    uuid = igntouuid(cfg.samaeluser)
    url = f"https://api.hypixel.net/player?key={cfg.apikey}&uuid={uuid}"
    data = getInfo(url)
    webhook = Webhook(cfg.webhook)

    def count_specific_strings_in_file(file_path, target_string):
        with open(file_path, 'r') as file:
            content = file.read()
            # Split the content into words based on whitespace
            words = content.split()
            # Count the number of occurrences of the target string
            num_occurrences = words.count(target_string)
            return num_occurrences

    def hourlystats():
        starttime = datetime.now()
        time.sleep(cfg.interval)

        hourlywins = count_specific_strings_in_file(cfg.hourly, 'W')
        hourlylosses = count_specific_strings_in_file(cfg.hourly, 'L')

        endtime = datetime.now()

        hourlywlr = round(hourlywins/max(hourlylosses,1), cfg.rounding_precision)

        hourlywlr = hourlywins/round(max(hourlylosses,1), cfg.rounding_precision)
        webhookdata = f"# Stats for {cfg.samaeluser} over the last {cfg.interval} seconds\nStart: {starttime}\nEnd: {endtime}\n-----\n- Hourly wins: {hourlywins}\n- Hourly losses: {hourlylosses}\n- Hourly wlr: {hourlywlr}"

        print(webhookdata)
        webhook.send(webhookdata)

        with open(cfg.hourly, 'w') as hourlyreset:
            hourlyreset.write('')


# splash screen
print("\n")
print(f"{c.Red}███████╗ █████╗ ███╗   ███╗ █████╗ ███████╗██╗     ")
print(f"{c.Red}██╔════╝██╔══██╗████╗ ████║██╔══██╗██╔════╝██║     ")
print(f"{c.Red}███████╗███████║██╔████╔██║███████║█████╗  ██║     ")
print(f"{c.Red}╚════██║██╔══██║██║╚██╔╝██║██╔══██║██╔══╝  ██║     ")
print(f"{c.Red}███████║██║  ██║██║ ╚═╝ ██║██║  ██║███████╗███████╗")
print(f"{c.Red}╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝")
                                                                                                        

print(f"{c.bgDefault}{c.White}\n {c.stBold}>>> Version {version}{c.allDefault}")
print(f"{c.bgDefault}{c.White} > Use alongside Lilith")
print(f"{c.bgDefault}{c.White} > Made by Toxikuu, Hollow, & Scycle")
print(f"{c.bgDefault}{c.White} > Special thanks to:")
print(f"{c.bgDefault}{c.White}     > Nolqk, Zani, Sedged, Yhuvko, Praxzz, Virse, Plonk, i5tar, Nea, Nuclear")
print(f"{c.bgDefault}{c.White} > Join the Discord! {discord}")

print("\n\n")

# clears record on start
with open(cfg.record, 'w') as clrrec:
    clrrec.write('')

if cfg.wh_enabled:
    # Hourly stats
    def hourly_function():
        while True:
            hourlystats()
            

    # Create a thread for the hourly function
    hourly_thread = threading.Thread(target=hourly_function)
    # Set the thread as a daemon so it will terminate when the main program terminates
    hourly_thread.daemon = True
    # Start the thread
    hourly_thread.start()


# read chat
def readchat():
    while True:


        chatlines = follow(open(cfg.chat, 'r'))
        for line in chatlines:

            # mysterybox fix
            if "[Client thread/INFO]: [CHAT] ? " in line and "found a" in line and "Mystery Box" in line:
                pass

            # mysterydust fix
            if "[Client thread/INFO]: [CHAT] ? You earned " in line and "Mystery Dust!" in line:
                pass

            # nicks
            if f"[Client thread/INFO]: [CHAT] Lilith > Found" in line and " likely nicked players: Possibly " in line:

                nickstart = line.index("Possibly ")
                nickend = line.index('\n', nickstart+1)
                name_nick = line[nickstart+9:nickend]
                name_nick = name_nick.strip(', ')
                if cfg.devmode: print(f'Nick found: {name_nick}')

                try: 
                    if name_nick != '':
                        antisniper(name_nick, '[NICK?]')
                    else:
                        if cfg.devmode: print(f'Skipped antisniper() since name_nick = <{name_nick}>')
                except: 
                    if name_nick != '' and name_nick not in cfg.safenicks:
                        omgnick()

            # /sc name isolation
            elif f"[Client thread/INFO]: [CHAT] {delimiter}" in line and f"[Client thread/INFO]: [CHAT] {delimiter} W/L: " not in line and "Lvl:" in line:

                isolation1start = line.index('[CHAT]')
                isolation1end = line.index('Lvl:')
                isolation1 = line[isolation1start+7:isolation1end]
                isolation1 = f"{isolation1}$"

                if cfg.devmode: print("\n$\nIsolation1:", isolation1)
                if '[' and ']' in isolation1:
                    isolationnamestart = isolation1.index('] ')
                    isolationnameend = isolation1.index('$')
                    isolationname = isolation1[isolationnamestart+2:isolationnameend]
                    isolationname = isolationname.strip()
                    if cfg.devmode: print("Isolated name:", isolationname)

                    isolationrankstart = isolation1.index('[')
                    isolationrankend = isolation1.index(']')
                    isolationrank = isolation1[isolationrankstart:isolationrankend+1]
                    if '§' in isolationrank:
                        isolationrank = re.sub('§.', '', isolationrank)
                    if cfg.devmode: print("Isolated rank:", isolationrank)

                    if cfg.show_own_stats:
                        antisniper(isolationname, isolationrank)
                    else:
                        if isolationname != cfg.samaeluser:
                            antisniper(isolationname, isolationrank)

                else:
                    isolationnonstart = isolation1.index(delimiter)
                    isolationnonend = isolation1.index('$')
                    isolationnon = isolation1[isolationnonstart+1:isolationnonend]
                    isolationnon = isolationnon.strip()
                    if cfg.devmode: print("Isolated non:", isolationnon)

                    if cfg.show_own_stats:
                        antisniper(isolationnon, '[NON]')
                    else:
                        if isolationnon != cfg.samaeluser:
                            antisniper(isolationnon, '[NON]')

            # Write record
            if "[Client thread/INFO]: [CHAT]   " in line and "WINNER!  " in line:
                iso1start = line.index('WINNER!')
                iso1end = line.index('\n')
                iso1 = (line[iso1start+7:iso1end]).strip()

                if '[' and ']' in iso1:
                    iso1 = f'{iso1}$'
                    iso2start = iso1.index(']')
                    iso2end = iso1.index('$')
                    iso2 = iso1[iso2start+2:iso2end]
                    won_opponent = iso2
                else:
                    won_opponent = iso1
                
                print(f"\n [i] You won against {won_opponent}")
                won_uuid = igntouuid(won_opponent)
                if cfg.devmode: print(f"\nUUID: {won_uuid}")

                with open(cfg.record, 'a') as wrec:
                    wrec.write(f"Won against {won_uuid}\n")

                with open(cfg.hourly, 'a') as whr:
                    whr.write(f"{datetime.now()} >> W\n")            

            elif "[Client thread/INFO]: [CHAT]   " in line and "WINNER!\n" in line:
                isol1start = line.index(cfg.nick)
                isol1end = line.index('WINNER!')
                isol1 = (line[isol1start+len(cfg.nick):isol1end]).strip()

                if '[' and ']' in isol1:
                    isol1 = f'{isol1}$'
                    isol2start = isol1.index(']')
                    isol2end = isol1.index('$')
                    isol2 = isol1[isol2start+2:isol2end]
                    lost_opponent = isol2
                else:
                    lost_opponent = isol1

                print(f"\n [i] You lost to {lost_opponent}")
                lost_uuid = igntouuid(lost_opponent)
                if cfg.devmode: print(f"\nUUID: {lost_uuid}")

                with open(cfg.record, 'a') as wrec:
                    wrec.write(f"Lost to {lost_uuid}\n")
            
                with open(cfg.hourly, 'a') as whr:
                    whr.write(f"{datetime.now()} >> L\n")

            if "[Client thread/INFO]: [CHAT]   " in line and "Opponent:" in line:
                iso1s = line.index("Opponent:")
                iso1e = line.index('\n')
                iso1_ = f"{(line[iso1s+10:iso1e]).strip()}$"
                if cfg.devmode: print(f"Previous opponent iso1: {iso1_}")

                if '[' and ']' in iso1_:
                    iso2s = iso1_.index(']')
                    iso2e = iso1_.index('$')
                    prevOpponent = (iso1_[iso2s+2:iso2e]).strip()
                else:
                    prevOpponent = iso1_.strip(' $')

                if cfg.devmode: print(f"Previous opponent iso2: {prevOpponent}")

                # previous opponents list
                prevOpponents.append(prevOpponent)

                if len(prevOpponents) > 2:
                    del prevOpponents[0]

                if len(prevOpponents) > 1:
                    _2prevOpponent = prevOpponents[-2]                    

            # commands
            addcommands = ['b', 's', 'w']
            for addcommand in addcommands:
                if f"[Client thread/INFO]: [CHAT] -{addcommand} " in line:
                    start = line.index(f'-{addcommand}')
                    end = line.index('\n', start+1)
                    name = line[start+3:end]

                    def addtolist(_name):
                        print(f'> Fetching uuid for {_name}')
                        try:
                            uuid = igntouuid(_name)

                            if addcommand == 'b':
                                print(f"> Blacklisting", uuid)
                                with open(f"{cfg.blacklist}", "a") as bl:
                                    bl.write(f"\n{uuid}\n")
                                print(f"> Added {_name} to blacklist\n")


                            elif addcommand == 's':
                                print(f"> Safelisting", uuid)
                                with open(f"{cfg.safelist}", "a") as sl:
                                    sl.write(f"\n{uuid}\n")
                                print(f"> Added {_name} to safelist\n")


                            elif addcommand == 'w':
                                print(f"> Weirdlisting", uuid)
                                with open(f"{cfg.weirdlist}", "a") as wl:
                                    wl.write(f"\n{uuid}\n")
                                print(f"> Added {_name} to weirdlist\n")


                        except KeyError:
                            print("Error: invalid ign")

                    if name == '^':
                        print("> Listing previous opponent")
                        addtolist(prevOpponent)
                    elif name == '^^':
                        print("> Listing previous previous opponent")
                        addtolist(_2prevOpponent)
                    else:
                        addtolist(name)


            removecommands = ['rb', 'rs', 'rw']
            for removecommand in removecommands:
                if f"[Client thread/INFO]: [CHAT] -{removecommand} " in line:
                    start = line.index(f'-{removecommand}')
                    end = line.index('\n', start+1)
                    name = line[start+4:end]

                    def removefromlist(_name):
                        print("> Fetching uuid for", _name)
                        try:
                            uuid = igntouuid(_name)

                            if removecommand == 'rb':
                                print(f"> Removing {uuid} from blacklist")
                                with open(f"{cfg.blacklist}", "r") as findbl:
                                    data = findbl.read()
                                    data = data.replace(uuid, '\n')
                                with open(f"{cfg.safelist}", "w") as findbl:
                                    findbl.write(data)
                                print(f"> Removed {_name} from blacklist\n")

                            elif removecommand == 'rs':
                                print(f"> Removing {uuid} from safelist")
                                with open(f"{cfg.safelist}", "r") as findsl:
                                    data = findsl.read()
                                    data = data.replace(uuid, '\n')
                                with open(f"{cfg.safelist}", "w") as findsl:
                                    findsl.write(data)
                                print(f"> Removed {_name} from safelist\n")

                            elif removecommand == 'rw':
                                print(f"> Removing {uuid} from weirdlist")
                                with open(f"{cfg.weirdlist}", "r") as findwl:
                                    data = findwl.read()
                                    data = data.replace(uuid, '\n')
                                with open(f"{cfg.weirdlist}", "w") as findwl:
                                    findwl.write(data)
                                print(f"> Removed {_name} from weirdlist\n")

                        except KeyError:
                            print("Error: invalid ign")

                    if name == '^':
                        print("> Unlisting previous opponent")
                        removefromlist(prevOpponent)
                    elif name == '^^':
                        print("> Unlisting previous previous opponent")
                        removefromlist(_2prevOpponent)
                    else:
                        removefromlist(name)

            if "[Client thread/INFO]: [CHAT] -api" in line:
                start = line.index('-api')
                end = line.index('\n', start+1)
                apikey = line[start+5:end]

                print(f"\n> Updating api key")

                config_ini.read(config_file)
                config_ini.set('apikey', 'apikey', apikey)

                with open(config_file, 'w') as file_object:
                    config_ini.write(file_object)
                print(f"> Successfully updated")
                readcfg()


            if "[Client thread/INFO]: [CHAT] -refresh" in line or "[Client thread/INFO]: [CHAT] -reload" in line:
                readcfg()
                print('Reloaded config!')

            if "[Client thread/INFO]: [CHAT] -dd" in line:
                for samael_list in samael_lists:
                    dd(samael_list)
                print('Fixed list formatting!')

            if "[Client thread/INFO]: [CHAT] -filter" in line:

                filter_lists()
                print('Filtered lists')

                for samael_list in samael_lists:
                    dd(samael_list)
                print('Fixed list formatting!')

            if "[Client thread/INFO]: [CHAT] -clr" in line:
                with open(cfg.record, 'w') as clrrec:
                    clrrec.write('')
                print('Cleared record!')

            if "[Client thread/INFO]: [CHAT] -note" in line:
                if cfg.devmode: print(line)
                namestart = line.index('-note')
                nameend = line.index(' "', namestart+1)
                name = line[namestart+6:nameend]
                print(f' [n] Target: {name}')
                notestart = line.index(' "')
                noteend = line.index('\n', notestart+1)
                note = line[notestart+2:noteend]

                if name == '^':
                    if cfg.devmode: print('NOTE ^ FLAG')
                    name = prevOpponent
                elif name == '^^':
                    name = _2prevOpponent
                print(f' [n] Note: {note}')
                print(f" [n] Grabbing {name}'s uuid")
                try:
                    note_uuid = igntouuid(name)

                    print(f" [n] UUID: {note_uuid}")
                    print(f" [n] Taking notes")
                    with open(cfg.notes, 'a') as nappend:
                        nappend.write(f'Target: {name} UUID: {note_uuid} Note: "{note}"\n')
                    print(f" [n] Noted {name}")
                except:
                    print(f" [n] Note error")

            if "[Client thread/INFO]: [CHAT] -delimiter " in line:
                argstart = line.index('-delimiter')
                argend = line.index('\n',argstart+1)
                arg = line[argstart+11:argend]

                if arg == '1' or '0':
                    config_ini.read(config_file)
                    config_ini.set('delimiter', 'delimiter_type', arg)

                    with open(config_file, 'w') as file_object:
                        config_ini.write(file_object)

                    print(f'[c] Set delimiter type to {arg}')
                    readcfg()

                else:
                    print(f'[c] Invalid argument for delimiter type! (Valid arguments are 0 and 1)')

            if "[Client thread/INFO]: [CHAT] -dev" in line:
                config_ini.read(config_file)
                if cfg.devmode:
                    config_ini.set('devmode', 'dev', 'False')
                else:
                    config_ini.set('devmode', 'dev', 'True')

                with open(config_file, 'w') as file_object:
                    config_ini.write(file_object)
                readcfg()
                print(f'[c] Set devmode to {cfg.devmode}')

            if "[Client thread/INFO]: [CHAT] -toggle " in line:
                argstart = line.index('-toggle')
                argend = line.index('\n',argstart+1)
                arg = line[argstart+8:argend]

                if arg in cfg_toggles:
                    config_ini.read(config_file)
                    if config_ini.getboolean('stat toggles', arg):
                        config_ini.set('stat toggles', arg, 'False')
                    else:
                        config_ini.set('stat toggles', arg, 'True')

                    with open(config_file, 'w') as file_object:
                        config_ini.write(file_object)

                    readcfg()
                    status = config_ini.getboolean('stat toggles', arg)
                    print(f' [c] Toggled {arg} to {status}')
                
                elif arg == 'allon':
                    set_all_true_in_section('stat toggles')
                    readcfg()
                    print(' [c] Toggled all on')

                elif arg == 'alloff':
                    set_all_false_in_section('stat toggles')
                    readcfg()
                    print(' [c] Toggled all off')

                else:
                    print(f' [c] Invalid argument: {arg}')

            if "[Client thread/INFO]: [CHAT] -nick " in line:
                argstart = line.index('-nick')
                argend = line.index('\n', argstart+1)
                arg = (line[argstart+6:argend]).strip()

                config_ini.read(config_file)
                config_ini.set('user', 'nick', arg)

                with open(config_file, 'w') as file_object:
                    config_ini.write(file_object)
                readcfg()
                print(f' [c] Changed nick to {arg}')
                if cfg.devmode: print(f'cfg.nick: {cfg.nick}')

            if "[Client thread/INFO]: [CHAT] -show_own_stats" in line:
                config_ini.read(config_file)
                if cfg.show_own_stats:
                    config_ini.set('options', 'show_own_stats', 'False')
                else:
                    config_ini.set('options', 'show_own_stats', 'True')

                with open(config_file, 'w') as file_object:
                    config_ini.write(file_object)
                readcfg()
                print(f'[c] Set show_own_stats to {cfg.show_own_stats}')


# antisniper
def antisniper(name, rank):
        print(f"\n\n{c.stBold}Checking: {rank} {name}{c.allDefault}")   

        uuid = igntouuid(name)
        if uuid != None:
            url = f"https://api.hypixel.net/player?key={cfg.apikey}&uuid={uuid}"
            data = getInfo(url)

            # BEDWARS
            try: stat_bedwars_star = data["player"]["achievements"]["bedwars_level"]
            except KeyError: stat_bedwars_star = 0

            try: stat_bedwars_final_kills = data["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
            except KeyError: stat_bedwars_final_kills = 0

            try: stat_bedwars_final_deaths = data["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
            except KeyError: stat_bedwars_final_deaths = 0

            try: stat_bedwars_beds_broken = data["player"]["stats"]["Bedwars"]["beds_broken_bedwars"]
            except KeyError: stat_bedwars_beds_broken = 0

            try: stat_bedwars_beds_lost = data["player"]["stats"]["Bedwars"]["beds_lost_bedwars"]
            except KeyError: stat_bedwars_beds_lost = 0

            try: stat_bw_kills = data["player"]["stats"]["Bedwars"]["kills_bedwars"]
            except KeyError: stat_bw_kills = 0

            try: stat_bw_deaths = data["player"]["stats"]["Bedwars"]["deaths_bedwars"]
            except KeyError: stat_bw_deaths = 0
            
            stat_bblr = round((stat_bedwars_beds_broken/max(stat_bedwars_beds_lost,1)),cfg.rounding_precision)
            stat_fkdr = round((stat_bedwars_final_kills/max(stat_bedwars_final_deaths,1)), cfg.rounding_precision)
            stat_bw_kdr = round(stat_bw_kills/max(stat_bw_deaths,1), cfg.rounding_precision)
            stat_bw_fksperstar = round(stat_bedwars_final_kills/max(stat_bedwars_star,1), cfg.rounding_precision)


            # SKYWARS
            try: stat_level_formatted = data["player"]["stats"]["SkyWars"]["levelFormatted"]
            except KeyError: stat_level_formatted = "xx0x"

            try: stat_skywars_kills = data["player"]["stats"]["SkyWars"]["kills"]
            except KeyError: stat_skywars_kills = 0

            try: stat_skywars_deaths = data["player"]["stats"]["SkyWars"]["deaths"]
            except KeyError: stat_skywars_deaths = 0

            stat_skywars_kdr = round((stat_skywars_kills/max(stat_skywars_deaths,1)), cfg.rounding_precision)
            swstar = stat_level_formatted[2:-1]+" ☆"
            intswstar = int(stat_level_formatted[2:-1])


            # SUMO
            try: stat_sumo_duel_wins = data["player"]["stats"]["Duels"]["sumo_duel_wins"]
            except KeyError: stat_sumo_duel_wins = 0

            try: stat_sumo_duel_losses = data["player"]["stats"]["Duels"]["sumo_duel_losses"]
            except KeyError: stat_sumo_duel_losses = 0  

            try: stat_sumo_bws = data["player"]["stats"]["Duels"]["best_sumo_winstreak"]
            except KeyError: stat_sumo_bws = 0

            try: stat_sumo_cws = data["player"]["stats"]["Duels"]["current_sumo_winstreak"]
            except KeyError: stat_sumo_cws = 0

            sumowlr = round((stat_sumo_duel_wins/max(stat_sumo_duel_losses, 1)), cfg.rounding_precision)


            # UHC DUELS
            try: stat_uhc_duel_wins = data["player"]["stats"]["Duels"]["uhc_duel_wins"]
            except KeyError: stat_uhc_duel_wins = 0

            try: stat_uhc_duel_losses = data["player"]["stats"]["Duels"]["uhc_duel_losses"]
            except KeyError: stat_uhc_duel_losses = 0

            uhcwlr = round((stat_uhc_duel_wins/max(stat_uhc_duel_losses, 1)), cfg.rounding_precision)


            # REAL UHC
            try: stat_UHC_kills = data["player"]["stats"]["UHC"]["kills_solo"] + data["player"]["stats"]["UHC"]["kills"]
            except KeyError: stat_UHC_kills = 0

            try: stat_UHC_deaths = data["player"]["stats"]["UHC"]["deaths_solo"] + data["player"]["stats"]["UHC"]["deaths"]
            except KeyError: stat_UHC_deaths = 0

            uhckdr = round((stat_UHC_kills/max(stat_UHC_deaths, 1)), cfg.rounding_precision)


            # GENERAL DUELS
            try: stat_duels_wins = data["player"]["stats"]["Duels"]["wins"]
            except KeyError: stat_duels_wins = 0

            try: stat_duels_losses = data["player"]["stats"]["Duels"]["losses"]
            except KeyError: stat_duels_losses = 0

            try: stat_duels_bws = data["player"]["stats"]["Duels"]["best_overall_winstreak"]
            except KeyError: stat_duels_bws = 0

            try: stat_duels_cws = data["player"]["stats"]["Duels"]["current_winstreak"]
            except KeyError: stat_duels_cws = 0

            wlr = round((stat_duels_wins/max(stat_duels_losses, 1)), cfg.rounding_precision)

            # MELEE
            try: stat_duels_melee_hits = data["player"]["stats"]["Duels"]["melee_hits"]
            except KeyError: stat_duels_melee_hits = 0

            try: stat_duels_melee_swings = data["player"]["stats"]["Duels"]["melee_swings"]
            except KeyError: stat_duels_melee_swings = 0

            try: stat_duels_combo_melee_hits = data["player"]["stats"]["Duels"]["combo_duel_melee_hits"]
            except KeyError: stat_duels_combo_melee_hits = 0

            try: stat_duels_combo_melee_swings = data["player"]["stats"]["Duels"]["combo_duel_melee_swings"]
            except KeyError: stat_duels_combo_melee_swings = 0

            nocombomeleehits = stat_duels_melee_hits-stat_duels_combo_melee_hits
            nocombomeleeswings = stat_duels_melee_swings-stat_duels_combo_melee_swings
            stat_melee_accuracy = round((nocombomeleehits/max(nocombomeleeswings,1)*100), cfg.rounding_precision)
            stat_combo_melee_accuracy = round((stat_duels_combo_melee_hits/max(stat_duels_combo_melee_swings,1)*100), cfg.rounding_precision)

            # NWL
            try: hypixelxp = data["player"]["networkExp"]
            except KeyError: hypixelxp = 0

            nwl = round(((math.sqrt((2 * hypixelxp) + 30625) / 50) - 2.5), cfg.rounding_precision)


            # DISPLAY STATS
            print(f"{c.bgDefault}{c.DarkGray}UUID:", uuid)
            print(f"{c.bgDefault}{c.White}------------------------------------")
            if cfg.nwl:
                if 15 < nwl < 100:
                    print(f"{tSafe}    ||   NWL: {nwl}") 
                elif (100 < nwl < 200) or (5 < nwl < 15):
                    print(f"{tRisky}   ||   NWL: {c.Yellow}{nwl}")
                elif nwl < 5:
                    print(f"{tDanger}  ||   NWL: {c.Red}{nwl}")
                else:
                    print(f"{tDanger}  ||   NWL: {c.Red}{nwl}")

            if cfg.sw_star:
                if 0 < intswstar < 10:
                    print(f"{tSafe}    ||   SW star: {swstar}")
                elif intswstar < 15 or intswstar == 0:
                    print(f"{tRisky}   ||   SW star: {c.Yellow}{swstar}")
                elif intswstar > 15:
                    print(f"{tDanger}  ||   SW star: {c.Red}{swstar}")

            if cfg.sw_kdr:
                if stat_skywars_kdr < 1:
                    print(f"{tSafe}    ||   SW kdr: {stat_skywars_kdr}")
                elif stat_skywars_kdr > 1 and stat_skywars_kdr < 2:
                    print(f"{tRisky}   ||   SW kdr: {c.Yellow}{stat_skywars_kdr}")
                elif stat_skywars_kdr > 2:
                    print(f"{tDanger}  ||   SW kdr: {c.Red}{stat_skywars_kdr}")

            if cfg.bw_star:
                if stat_bedwars_star < 200 and stat_bedwars_star != 0:
                    print(f"{tSafe}    ||   BW star: {stat_bedwars_star} ☆")
                elif stat_bedwars_star > 200 and stat_bedwars_star < 350:
                    print(f"{tRisky}   ||   BW star: {c.Yellow}{stat_bedwars_star} ☆")
                elif stat_bedwars_star > 350 or stat_bedwars_star == 0:
                    print(f"{tDanger}  ||   BW star: {c.Red}{stat_bedwars_star} ☆")

            if cfg.bw_fkdr:
                if stat_fkdr < 2 and stat_fkdr != 0:
                    print(f"{tSafe}    ||   FKDR: {stat_fkdr}")
                elif stat_fkdr > 2 and stat_fkdr < 3.5:
                    print(f"{tRisky}   ||   FKDR: {c.Yellow}{stat_fkdr}")
                elif stat_fkdr > 3.5:
                    print(f"{tDanger}  ||   FKDR: {c.Red}{stat_fkdr}")
                else:
                    print(f"{tRisky}   ||   FKDR: {c.Yellow}{stat_fkdr}")

            if cfg.bw_bblr:
                if stat_bblr < 1.4 and stat_bblr != 0:
                    print(f"{tSafe}    ||   BBLR: {stat_bblr}")
                elif stat_bblr > 1.4 and stat_bblr < 2.8:
                    print(f"{tRisky}   ||   BBLR: {c.Yellow}{stat_bblr}")
                elif stat_bblr > 2.8:
                    print(f"{tDanger}  ||   BBLR: {c.Red}{stat_bblr}")
                else:
                    print(f"{tRisky}   ||   BBLR: {c.Yellow}{stat_bblr}")    
            
            if cfg.bw_kdr:
                if stat_bw_kdr < 1.2 and stat_bw_kdr != 0:
                    print(f"{tSafe}    ||   BW kdr: {stat_bw_kdr}")
                elif stat_bw_kdr > 1.2 and stat_bw_kdr < 2.4:
                    print(f"{tRisky}   ||   BW kdr: {c.Yellow}{stat_bw_kdr}")
                elif stat_bw_kdr > 2.4:
                    print(f"{tDanger}  ||   BW kdr: {c.Red}{stat_bw_kdr}")
                else:
                    print(f"{tRisky}   ||   BW kdr: {c.Yellow}{stat_bw_kdr}")
            if cfg.bw_fksperstar:
                if stat_bw_fksperstar < 25:
                    print(f"{tSafe}    ||   BW fks/star: {stat_bw_fksperstar}")
                elif stat_bw_fksperstar > 25 and stat_bw_fksperstar < 50:
                    print(f"{tRisky}   ||   BW fks/star: {c.Yellow}{stat_bw_fksperstar}")
                elif stat_bw_fksperstar > 50:
                    print(f"{tDanger}  ||   BW fks/star: {c.Red}{stat_bw_fksperstar}")

            if cfg.sumo_wlr:    
                if sumowlr < 1.1:
                    print(f"{tSafe}    ||   Sumo wlr: {sumowlr}")
                elif sumowlr > 1.1 and sumowlr < 1.6:
                    print(f"{tRisky}   ||   Sumo wlr: {c.Yellow}{sumowlr}")
                elif sumowlr > 1.6:
                    print(f"{tDanger}  ||   Sumo wlr: {c.Red}{sumowlr}")   
            
            if cfg.sumo_bws:
                if stat_sumo_bws < 10 and stat_sumo_bws != 0:
                    print(f"{tSafe}    ||   Sumo bws: {stat_sumo_bws}")
                elif stat_sumo_bws > 10 and stat_sumo_bws < 25:
                    print(f"{tRisky}   ||   Sumo bws: {c.Yellow}{stat_sumo_bws}")
                elif stat_sumo_bws > 25 or (stat_sumo_bws == 0 and stat_sumo_duel_wins > 0):
                    print(f"{tDanger}  ||   Sumo bws: {c.Red}{stat_sumo_bws}")
                else:
                    print(f"{tRisky}   ||   Sumo bws: {c.Yellow}{stat_sumo_bws}")

            if cfg.sumo_cws:
                if stat_sumo_cws < 5:
                    print(f"{tSafe}    ||   Sumo cws: {stat_sumo_cws}")
                elif stat_sumo_cws > 5 and stat_sumo_cws < 10:
                    print(f"{tRisky}   ||   Sumo cws: {c.Yellow}{stat_sumo_cws}")
                elif stat_sumo_cws > 10:
                    print(f"{tDanger}  ||   Sumo cws: {c.Red}{stat_sumo_cws}")
                else:
                    print(f"{tSafe}    ||   Sumo cws: {stat_sumo_cws}")
            
            if cfg.uhc_wlr:
                if uhcwlr < 1:
                    print(f"{tSafe}    ||   UHCD wlr: {uhcwlr}")
                elif uhcwlr > 1 and uhcwlr < 2.5:
                    print(f"{tRisky}   ||   UHCD wlr: {c.Yellow}{uhcwlr}")
                elif uhcwlr > 2.5:
                    print(f"{tDanger}  ||   UHCD wlr: {c.Red}{uhcwlr}")
            
            if cfg.uhc_kdr:
                if uhckdr < 0.5:
                    print(f"{tSafe}    ||   UHC kdr: {uhckdr}")
                elif uhckdr > 0.5 and uhckdr < 1.5:
                    print(f"{tRisky}   ||   UHC kdr: {c.Yellow}{uhckdr}")
                elif uhckdr > 1.5:
                    print(f"{tDanger}  ||   UHC kdr: {c.Red}{uhckdr}")

            if cfg.duels_wlr:
                if wlr < 1.5 or (wlr == 0 and stat_duels_losses > 0):
                    print(f"{tSafe}    ||   Wlr: {wlr}")
                elif wlr > 1.5 and wlr < 2.5:
                    print(f"{tRisky}   ||   Wlr: {c.Yellow}{wlr}")
                elif wlr > 2.5 or (wlr == 0 and stat_duels_losses == 0):
                    print(f"{tDanger}  ||   Wlr: {c.Red}{wlr}")      
            
            if cfg.duels_wins:
                if stat_duels_wins > 10 and stat_duels_wins < 10000:
                    print(f"{tSafe}    ||   Wins: {stat_duels_wins}")
                elif (stat_duels_wins > 3 and stat_duels_wins < 10) or (stat_duels_wins > 10000 and stat_duels_wins < 20000):
                    print(f"{tRisky}   ||   Wins: {c.Yellow}{stat_duels_wins}")
                elif (stat_duels_wins < 3 and (stat_duels_losses < 4 * stat_duels_wins)) or (stat_duels_wins > 20000):
                    print(f"{tDanger}  ||   Wins: {c.Red}{stat_duels_wins}")
                else:
                    print(f"{tSafe}    ||   Wins: {stat_duels_wins}")       

            if cfg.duels_losses:
                if stat_duels_losses > 10:
                    print(f"{tSafe}    ||   Losses: {stat_duels_losses}")
                elif stat_duels_losses > 3 and stat_duels_losses < 10:
                    print(f"{tRisky}   ||   Losses: {c.Yellow}{stat_duels_losses}")
                elif stat_duels_losses < 3:
                    print(f"{tDanger}  ||   Losses: {c.Red}{stat_duels_losses}")
                else:
                    print(f"{tSafe}    ||   Losses: {stat_duels_losses}")  
            
            if cfg.duels_bws:
                if stat_duels_bws < 25 and stat_duels_bws != 0:
                    print(f"{tSafe}    ||   Bws: {stat_duels_bws}")
                elif stat_duels_bws > 25 and stat_duels_bws < 50:
                    print(f"{tRisky}   ||   Bws: {c.Yellow}{stat_duels_bws}")
                elif stat_duels_bws > 50 or stat_duels_bws == 0:
                    print(f"{tDanger}  ||   Bws: {c.Red}{stat_duels_bws}")
 
            if cfg.duels_cws:
                if stat_duels_cws < 5:
                    print(f"{tSafe}    ||   Cws: {stat_duels_cws}")
                elif stat_duels_cws > 5 and stat_duels_cws < 15:
                    print(f"{tRisky}   ||   Cws: {c.Yellow}{stat_duels_cws}")
                elif stat_duels_cws > 15:
                    print(f"{tDanger}  ||   Cws: {c.Red}{stat_duels_cws}")
                else:
                    print(f"{tSafe}    ||   Cws: {stat_duels_cws}")
            
            if cfg.melee_accuracy:
                if stat_melee_accuracy < 50 and stat_melee_accuracy != 0:
                    print(f"{tSafe}    ||   mAccuracy: {stat_melee_accuracy} %")
                elif stat_melee_accuracy > 50 and stat_melee_accuracy < 70:
                    print(f"{tRisky}   ||   mAccuracy: {c.Yellow}{stat_melee_accuracy} %")
                elif stat_melee_accuracy > 70 or stat_melee_accuracy == 0:
                    print(f"{tDanger}  ||   mAccuracy: {c.Red}{stat_melee_accuracy} %")
            
            if cfg.combo_melee_accuracy:
                if stat_combo_melee_accuracy < 75:
                    print(f"{tSafe}    ||   Combo mAcc: {stat_combo_melee_accuracy} %")
                elif stat_combo_melee_accuracy > 75 and stat_combo_melee_accuracy < 100:
                    print(f"{tRisky}   ||   Combo mAcc: {c.Yellow}{stat_combo_melee_accuracy} %{c.Default}")
                elif stat_combo_melee_accuracy > 100:
                    print(f"{tDanger}  ||   Combo mAcc: {c.Red}{stat_combo_melee_accuracy} %{c.Default}")
                else:
                    print(f"{tSafe}    ||   Combo mAcc: {stat_combo_melee_accuracy} %")

            # STATS END
            print(f"{c.bgDefault}{c.White}------------------------------------")


            # LISTS START
            # Api off
            if stat_duels_bws == 0 and stat_duels_bws == stat_duels_cws and stat_duels_wins > 5:
                print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} WS API OFF {c.bgDefault}{c.LightYellow} << {c.Default}")
                api_on = True
            else:
                api_on = False

            # Read blacklist
            with open(cfg.blacklist, 'r') as bl:
                for line in bl.readlines():
                    line = line.strip()
                    if line == uuid:
                        if api_on == False: print('')
                        print(f"{c.LightBlue} >> {c.bgBlue}{c.Black} BLACKLISTED! {c.bgDefault}{c.LightBlue} << {c.Default}")

            # Read safelist
            with open(cfg.safelist, 'r') as sl:
                for line in sl.readlines():
                    line = line.strip()
                    if line == uuid:
                        if api_on == False: print('')
                        print(f"{c.LightGreen} >> {c.bgGreen}{c.Black} SAFELISTED! {c.bgDefault}{c.LightGreen} << {c.Default}")

            # Read weirdlist
            with open(cfg.weirdlist, 'r') as wl:
                for line in wl.readlines():
                    line = line.strip()
                    if line == uuid:
                        if api_on == False: print('')
                        print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} WEIRD! {c.bgDefault}{c.LightYellow} << {c.Default}")

            # Read notes
            with open(cfg.notes, 'r') as rnotes:
                for nline in rnotes.readlines():
                    if uuid in nline:
                        if cfg.devmode: print(nline)
                        start = nline.index('Note: "')
                        end = nline.index('"\n', start+1)
                        note = nline[start+7:end]
                        print(f' {c.White}>>{c.allDefault} {c.bgLightBlue}{c.Black} Note: {note} {c.allDefault} {c.White}<<{c.allDefault} ')

            # Read record
            rec_lost_uuids = []
            rec_won_uuids = []
            autobl_list = []
            autosl_list = []
            with open(cfg.record, 'r') as rrec:
                for line in rrec.readlines():
                    if 'Lost to' in line:
                        rec_lost_uuid = line.replace('Lost to ', '')
                        rec_lost_uuids.append(rec_lost_uuid)

                    elif 'Won against' in line:
                        rec_won_uuid = line.replace('Won against ', '')
                        rec_won_uuids.append(rec_won_uuid)

                for uuid_ in rec_lost_uuids:
                    uuidcount = countOf(rec_lost_uuids, uuid_)
                    if uuidcount > cfg.autoblacklist_loss_count-1:
                        autobl_list.append(uuid_)

                for uuid_ in rec_won_uuids:
                    uuidcount = countOf(rec_won_uuids, uuid_)
                    if uuidcount > cfg.autosafelist_win_count-1:
                        autosl_list.append(uuid_)

                for _uuid in autobl_list:
                    uuidcount = countOf(autobl_list, _uuid)
                    if uuidcount > 1:
                        uuidindex = autobl_list.index(_uuid)
                        autobl_list.pop(uuidindex)
                
                for _uuid in autosl_list:
                    uuidcount = countOf(autosl_list, _uuid)
                    if uuidcount > 1:
                        uuidindex = autosl_list.index(_uuid)
                        autosl_list.pop(uuidindex)
            if cfg.devmode:
                print(f'Auto blacklist list: {autobl_list}')
                print(f'Auto safelist list: {autosl_list}')

            if len(autobl_list) > 0:
                autobl_list.clear()
                if cfg.devmode: print(f'Cleared autobl_list')
            
            if len(autosl_list) > 0:
                autosl_list.clear()
                if cfg.devmode: print(f'Cleared autosl_list')

            # Autolist
            if cfg.autoblacklist_loss_count > 0:
                with open(cfg.blacklist, 'a') as abl:
                    for autobl_uuid in autobl_list:
                        abl.write(f'{autobl_uuid}\n')
                dd(cfg.blacklist)

            if cfg.autosafelist_win_count > 0:
                with open(cfg.safelist, 'a') as asl:
                    for autosl_uuid in autosl_list:
                        asl.write(f'{autosl_uuid}\n')
                dd(cfg.safelist)


readchat()

