# import libraries
import math, os, sys, configparser, re, shutil, yaml, asyncio
from tox_assets import *

# initialization variables
version = '5.1.3'
discord = "https://discord.gg/N3rVjjVEsv"

home_dir = os.path.expanduser('~')
samael_dir = os.path.join(home_dir, 'Samael')
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
old_tox_assets_dir = os.path.join(script_directory, 'tox_assets.py')
new_tox_assets_dir = os.path.join(samael_dir, 'tox_assets.py')
samael_py = os.path.basename(__file__)
correct_samael_py_path = os.path.join(samael_dir, samael_py)
lists_directory = os.path.join(samael_dir, 'Lists')
config_file = os.path.join(samael_dir, 'config.ini')
config_ini = configparser.ConfigParser()

lunarlatestlog = os.path.join(home_dir, '.lunarclient', 'offline', 'multiver', 'logs', 'latest.log')
blacklist = os.path.join(lists_directory, 'Blacklist.log')
safelist = os.path.join(lists_directory, 'Safelist.log')
weirdlist = os.path.join(lists_directory, 'Weirdlist.log')
record = os.path.join(lists_directory, 'Record.log')
notes = os.path.join(lists_directory, 'Notes.log')
s_logs = [blacklist, safelist, weirdlist, record, notes]
yaml_dir = os.path.join(samael_dir, 'stat_settings.yaml')

# creates samael folder in the home directory
if not os.path.isdir(samael_dir):
    os.makedirs(samael_dir)
    print(f'Creating samael directory: {samael_dir}')

# moves samael.py & tox_assets.py to that folder
if script_directory != samael_dir:
    shutil.move(__file__, correct_samael_py_path)
    print(f'Moved {samael_py} to {correct_samael_py_path}')
    shutil.move(old_tox_assets_dir, new_tox_assets_dir)
    print(f'Moved tox_assets.py to {new_tox_assets_dir}')

# build lists
if not os.path.isdir(lists_directory):
    os.makedirs(lists_directory)
    print(f'Created lists directory: {lists_directory}')
    for s_log in s_logs:
        with open(s_log, 'x'): 
            print(f'Created {s_log}')

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

tDodge = f'{c.White}{c.bgBlue}DODGE{c.allDefault}'
tDanger = f'{c.White}{c.bgRed}DANGER{c.allDefault}'
tRisky = f'{c.Yellow}Risky{c.allDefault}'
tSafe = f'{c.White}Safe{c.allDefault}'
mcchat = '[Client thread/INFO]: [CHAT]'

prevOpponents = []

# config
def readcfg():
    with open(config_file, 'r') as file_object:
        config_ini.read_file(file_object)
        global cfg
        class cfg:
            # [apikey]
            apikey = config_ini.get('apikey', 'apikey')
            if apikey == 'your apikey':
                apikey = input('Enter your apikey: ')

            # [user]
            samaeluser = config_ini.get('user', 'username')
            if samaeluser == 'your username':
                samaeluser = input('Enter your minecraft username: ')
            
            nick = config_ini.get('user', 'nick')
            if nick.strip() == 'your nick':
                isNicked = input('Are you nicked (y/n): ')
                if isNicked == 'n': nick = samaeluser
                elif isNicked == 'y': nick = input('Enter your nick: ')

            if nick.strip() == '':
                nick = samaeluser

            # [devmode]
            devmode = config_ini.getboolean('devmode', 'dev')

            # [paths]
            chat = config_ini.get('paths', 'chat')
            if chat == r'C:\Users\User\.lunarclient\offline\multiver\logs\latest.log':
                chat = lunarlatestlog
                print(f'Using lunar client chat path by default: {lunarlatestlog}')
            
            # [safenicks]
            safenicks = config_ini.get('safenicks', 'safenicks')
            safenicks = list(safenicks.split(', ')) # fixes formatting

            # [nameflags]
            nameflags = config_ini.get('nameflags', 'nameflags')
            nameflags = list(nameflags.split(', ')) # fixes formatting

            # [options]
            rounding_precision = config_ini.getint('options', 'rounding_precision')
            show_own_stats = config_ini.getboolean('options', 'show_own_stats')
            clear = config_ini.getboolean('options', 'clear')
            show_stat_values = config_ini.getboolean('options', 'show_stat_values')
            show_safe = config_ini.getboolean('options', 'show_safe')
            show_risky = config_ini.getboolean('options', 'show_risky')
            show_danger = config_ini.getboolean('options', 'show_danger')
            show_dodge = config_ini.getboolean('options', 'show_dodge')
            show_verdict_score = config_ini.getboolean('options', 'show_verdict_score')


            # [autolist]
            autosafelist_win_count = config_ini.getint('autolist', 'autosafelist_win_count')
            autoblacklist_loss_count = config_ini.getint('autolist', 'autoblacklist_loss_count')
            autososafe_win_count = config_ini.getint('autolist', 'autososafe_win_count')

            # [delimiter]
            delimiter_type = config_ini.getint('delimiter', 'delimiter_type')
    print(' [c] Updated config')

# read yaml
with open(yaml_dir, 'r') as file:
    y = yaml.safe_load(file)
def read_yaml():
    with open(yaml_dir, 'r') as file:
        y = yaml.safe_load(file)
        print(' [c] Updated yaml')
    return y
readcfg()

# delimiter fix
if cfg.delimiter_type == 0:
    delimiter = '▌'
elif cfg.delimiter_type == 1:
    delimiter = '?'
    
if cfg.devmode: print(f'Delimiter type: {delimiter}')

# main lists
samael_lists = [blacklist, safelist, weirdlist]

# devmode
if cfg.devmode:
    print('Launching in devmode\n\n')
    with open(config_file, 'r') as file_object_dev:
        config_data_dev = file_object_dev.read()
    print(config_data_dev)

# some functions
def divide(value1, value2):
    if value2 == 0: value2 = 1
    return round(value1/value2, cfg.rounding_precision)

def S_igntouuid(ign):
    try:
        pdb = getInfo(f"https://playerdb.co/api/player/minecraft/{ign}")
        uuid = pdb["data"]["player"]["raw_id"]
        return uuid
    except:
        print(f'\n{c.LightRed} >> {c.bgRed}{c.Black} Failed to access uuid for {ign}! {c.allDefault}{c.LightRed} <<{c.allDefault}')

def filter_lists():
    remove_blacklisted_ids(safelist, blacklist, weirdlist)
    print(f"> Filtered!")

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

clear()
# splash screen
Samael_text(c.Red)                                                                                         
print(f"{c.bgDefault}{c.White}\n {c.stBold}>>> Version {version}{c.allDefault}")
print(f"{c.bgDefault}{c.White} > Use alongside Lilith")
print(f"{c.bgDefault}{c.White} > Made by Toxikuu, Hollow, & Scycle")
print(f"{c.bgDefault}{c.White} > Special thanks to:")
print(f"{c.bgDefault}{c.White}     > Nolqk, Zani, Sedged, Yhuvko, Praxzz, Virse, Plonk, i5tar, Nea, Nuclear")
print(f"{c.bgDefault}{c.White} > Join the Discord! {discord}")
print("\n\n")

# clears record on start
with open(record, 'w') as clrrec:
    clrrec.write('')

# removes duplicate notes and empty lines
with open(notes, 'r') as input:
    lines = input.readlines()
    lines = list(dict.fromkeys(lines))
    write_list_to_txt(lines, notes)
remove_empty_lines(notes)
with open(notes, 'a') as n:
    n.write('\n')

# read chat
def readchat():
    while True:


        chatlines = follow(open(cfg.chat, 'r'))
        for line in chatlines:

            # mysterybox fix
            if f"{mcchat} ? " in line and "found a" in line and "Mystery Box" in line:
                pass

            # mysterydust fix
            if f"{mcchat} ? You earned " in line and "Mystery Dust!" in line:
                pass

            # nicks
            if f"{mcchat} Lilith > Found" in line and " likely nicked players: Possibly " in line:

                nickstart = line.index("Possibly ")
                nickend = line.index('\n', nickstart+1)
                name_nick = line[nickstart+9:nickend]
                name_nick = name_nick.strip(', ')
                if cfg.devmode: print(f'Nick found: {name_nick}')

                try: 
                    if name_nick != '':
                        statslol('[?]', name_nick)
                    else:
                        if cfg.devmode: print(f'Skipped statslol() since name_nick = <{name_nick}>')
                except: 
                    if name_nick != '' and name_nick not in cfg.safenicks:
                        omgnick()

            # /sc name isolation
            elif f"{mcchat} {delimiter}" in line and f"{mcchat} {delimiter} W/L: " not in line and "Lvl:" in line:

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
                        statslol(isolationrank, isolationname)
                    else:
                        if isolationname != cfg.samaeluser:
                            statslol(isolationrank, isolationname)

                else:
                    isolationnonstart = isolation1.index(delimiter)
                    isolationnonend = isolation1.index('$')
                    isolationnon = isolation1[isolationnonstart+1:isolationnonend]
                    isolationnon = isolationnon.strip()
                    if cfg.devmode: print("Isolated non:", isolationnon)

                    if cfg.show_own_stats:
                        statslol('[NON]', isolationnon)
                    else:
                        if isolationnon != cfg.samaeluser:
                            statslol('[NON]', isolationnon)

            # Write record
            if f"{mcchat}   " in line and "WINNER!  " in line:
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
                won_uuid = S_igntouuid(won_opponent)
                if cfg.devmode: print(f"\nUUID: {won_uuid}")

                with open(record, 'a') as wrec:
                    wrec.write(f"Won against {won_uuid}\n")     

            elif f"{mcchat}   " in line and "WINNER!\n" in line:
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
                lost_uuid = S_igntouuid(lost_opponent)
                if cfg.devmode: print(f"\nUUID: {lost_uuid}")

                with open(record, 'a') as wrec:
                    wrec.write(f"Lost to {lost_uuid}\n")

            if f"{mcchat}   " in line and "Opponent:" in line:
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
                if f"{mcchat} -{addcommand} " in line:
                    start = line.index(f'-{addcommand}')
                    end = line.index('\n', start+1)
                    name = line[start+3:end]

                    def addtolist(_name):
                        print(f'> Fetching uuid for {_name}')

                        def alist(uuid, listdir, listname):
                            print(f"> {listname}ing {uuid}")
                            with open(listdir, 'a') as al:
                                al.write(f"\n{uuid}\n")
                            print(f"> Added {_name} to {listname}\n")
                            remove_empty_lines(listdir)

                        try:
                            uuid = S_igntouuid(_name)
                        except KeyError:
                            print("Error: invalid ign")
                        
                        if uuid != None:    
                            if addcommand == 'b':
                                alist(uuid, blacklist, 'blacklist')
                            elif addcommand == 's':
                                alist(uuid, safelist, 'safelist')
                            elif addcommand == 'w':
                                alist(uuid, weirdlist, 'weirdlist')

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
                if f"{mcchat} -{removecommand} " in line:
                    start = line.index(f'-{removecommand}')
                    end = line.index('\n', start+1)
                    name = line[start+4:end]

                    def removefromlist(_name):
                        print("> Fetching uuid for", _name)

                        def rlist(uuid, listdir, listname):
                            print(f"> removing {uuid} from {listname}")
                            with open(listdir, 'r') as rl:
                                listdata = rl.read()
                                listdata = listdata.replace(uuid, '\n')
                            with open(listdir, 'w') as rl:
                                rl.write(listdata)
                            print(f" Removed {_name} from {listname}\n")

                        try:
                            uuid = S_igntouuid(_name)
                        except KeyError:
                            print("Error: invalid ign")

                        if uuid != None:
                            if removecommand == 'rb':
                                rlist(uuid, blacklist, 'blacklist')
                            elif removecommand == 'rs':
                                rlist(uuid, safelist, 'safelist')
                            elif removecommand == 'rw':
                                rlist(uuid, weirdlist, 'weirdlist')

                    if name == '^':
                        print("> Unlisting previous opponent")
                        removefromlist(prevOpponent)
                    elif name == '^^':
                        print("> Unlisting previous previous opponent")
                        removefromlist(_2prevOpponent)
                    else:
                        removefromlist(name)

            if f"{mcchat} -api" in line:
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


            if f"{mcchat} -refresh" in line or f"{mcchat} -reload" in line:
                readcfg()
                read_yaml()

            if f"{mcchat} -dd" in line:
                for samael_list in samael_lists:
                    dd(samael_list)
                print('> Fixed list formatting!')

            if f"{mcchat} -filter" in line:
                filter_lists()

                for samael_list in samael_lists:
                    dd(samael_list)
                print('> Fixed list formatting!')

            if f"{mcchat} -sosafe " in line:
                namestart = line.index('-sosafe')
                nameend = line.index('\n')
                name = (line[namestart+8:nameend]).strip()

                if name == '^': name = prevOpponent
                if name == '^^': name = _2prevOpponent
                uuid = S_igntouuid(name)

                if uuid != None:
                    with open(safelist, 'a') as ss:
                        print(f'> Sosafing {name}')
                        ss.write(f'\n[SOSAFE] {uuid}\n')
                        print(f'> Sosafed {uuid}')
                
            if f"{mcchat} -note" in line:
                if cfg.devmode: print(line)
                namestart = line.index('-note')
                nameend = line.index(' "', namestart+1)
                name = line[namestart+6:nameend]
                print(f' [n] Target: {name}')
                notestart = line.index(' "')
                noteend = line.index('\n', notestart+1)
                note = line[notestart+2:noteend]

                if name == '^':
                    name = prevOpponent
                elif name == '^^':
                    name = _2prevOpponent
                print(f' [n] Note: {note}')
                print(f" [n] Grabbing {name}'s uuid")
                try:
                    note_uuid = S_igntouuid(name)

                    print(f" [n] UUID: {note_uuid}")
                    print(f" [n] Taking notes")
                    with open(notes, 'a') as nappend:
                        nappend.write(f'Target: {name.lower()} UUID: {note_uuid} Note: "{note}"\n')
                    print(f" [n] Noted {name}")
                except:
                    print(f" [n] Note error")

                with open(notes, 'r') as input: 
                    lines = (input.readlines())
                    lines = list(dict.fromkeys(lines))
                    write_list_to_txt(lines, notes)

            if f"{mcchat} -delimiter " in line:
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

            if f"{mcchat} -dev" in line:
                config_ini.read(config_file)
                if cfg.devmode:
                    config_ini.set('devmode', 'dev', 'False')
                else:
                    config_ini.set('devmode', 'dev', 'True')

                with open(config_file, 'w') as file_object:
                    config_ini.write(file_object)
                readcfg()
                print(f'[c] Set devmode to {cfg.devmode}')

            # if "[Client thread/INFO]: [CHAT] -toggle " in line:
            #     argstart = line.index('-toggle')
            #     argend = line.index('\n',argstart+1)
            #     arg = line[argstart+8:argend]

            #     if arg in cfg_toggles:
            #         config_ini.read(config_file)
            #         if config_ini.getboolean('stat toggles', arg):
            #             config_ini.set('stat toggles', arg, 'False')
            #         else:
            #             config_ini.set('stat toggles', arg, 'True')

            #         with open(config_file, 'w') as file_object:
            #             config_ini.write(file_object)

            #         readcfg()
            #         status = config_ini.getboolean('stat toggles', arg)
            #         print(f' [c] Toggled {arg} to {status}')
                
            #     elif arg == 'allon':
            #         set_all_true_in_section('stat toggles')
            #         readcfg()
            #         print(' [c] Toggled all on')

            #     elif arg == 'alloff':
            #         set_all_false_in_section('stat toggles')
            #         readcfg()
            #         print(' [c] Toggled all off')

            #     else:
            #         print(f' [c] Invalid argument: {arg}')

            if f"{mcchat} -nick " in line:
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

            if f"{mcchat} -show_own_stats" in line:
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
def statslol(rank, name):
    if cfg.clear: clear()
    print(f"\n\n{c.stBold}Checking: {rank} {name}{c.allDefault}")   
    target_uuid = S_igntouuid(name)
    if target_uuid == None: return None
    print(f"{c.bgDefault}{c.DarkGray}UUID: {target_uuid}{c.allDefault}")

    async def guildxd():
        gdata = get_guild_data(cfg.apikey, target_uuid)
        return gdata
    
    async def hyxd():
        hy = get_hypixel_stats(cfg.apikey, target_uuid)
        return hy

    async def bilocate():
        gdata, hy = await asyncio.gather(guildxd(), hyxd())
        return gdata, hy
    
    async def asyxd():
        return await bilocate()

    xdresult = asyncio.run(asyxd())
    gdata, hy = xdresult

    # Get guild info
    inGuild = check_if_guild_is_null(gdata)
    if inGuild:
        gname = get_guild_name(gdata)
        print(f"Guild: {gname}")
        g_uuids = get_uuids_in_guild(gdata)
    else:
        print(f"Guild: None")
    print(f"{c.bgDefault}{c.White}------------------------------------")


    # Get hypixel stats


    print(f"{c.bgDefault}{c.White}------------------------------------")

    # Labelling function
    def get_category(section, value):
            value = float(value)
            try: thresholds = y['Thresholds'][section]
            except KeyError: thresholds = None
            if thresholds != None:
                for category, (start, end) in thresholds.items():
                    if start == None: start = 0
                    if end == None: end = float('inf')

                    if start <= value < end:
                        return category
                return "Danger"

    def get_value_from_json(json_obj, path):
        # Split the path into individual keys
        keys = path.split('.')

        # Iterate through the keys to traverse the JSON object
        current = json_obj
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                current = 0

        return current

    # hypath shortcuts
    sw_hypath = 'player.stats.SkyWars'
    bw_hypath = 'player.stats.Bedwars'
    d_hypath = 'player.stats.Duels'
    uhc_hypath = 'player.stats.UHC'
    sg_hypath = 'player.stats.HungerGames'
    pit_hypath = 'player.stats.Pit.pit_stats_pt1'
    ww_hypath = 'player.stats.WoolGames.wool_wars.stats'

    # hypaths dictionary
    hypaths = {
        'NWL' : 'player.networkExp',
        'SW star' : f'{sw_hypath}.levelFormattedWithBrackets',
        'SW kills' : f'{sw_hypath}.kills',
        'SW deaths' : f'{sw_hypath}.deaths',
        'SW wins' : f'{sw_hypath}.wins',
        'SW losses' : f'{sw_hypath}.losses',
        'BW star' : 'player.achievements.bedwars_level',
        'BW fks' : f'{bw_hypath}.final_kills_bedwars',
        'BW fds' : f'{bw_hypath}.final_deaths_bedwars',
        'Beds lost' : f'{bw_hypath}.beds_lost_bedwars',
        'Beds broken' : f'{bw_hypath}.beds_broken_bedwars',
        'BW kills' : f'{bw_hypath}.kills_bedwars',
        'BW deaths' : f'{bw_hypath}.deaths_bedwars',
        'Sumo wins' : f'{d_hypath}.sumo_duel_wins',
        'Sumo losses' : f'{d_hypath}.sumo_duel_losses',
        'Sumo bws' : f'{d_hypath}.best_sumo_winstreak',
        'Sumo cws' : f'{d_hypath}.current_sumo_winstreak',
        'UHCD wins' : f'{d_hypath}.uhc_duel_wins',
        'UHCD losses': f'{d_hypath}.uhc_duel_losses',
        'UHCD bws': f'{d_hypath}.best_uhc_winstreak',
        'UHCD cws': f'{d_hypath}.current_uhc_winstreak',
        'UHC kills' : f'{uhc_hypath}.kills',
        'UHC kills2' : f'{uhc_hypath}.kills_solo',
        'UHC deaths' : f'{uhc_hypath}.deaths',
        'UHC deaths2' : f'{uhc_hypath}.deaths_solo',
        'UHC wins' : f'{uhc_hypath}.wins',
        'UHC games' : f'{uhc_hypath}.games_played',
        'Duels wins' : f'{d_hypath}.wins',
        'Duels losses' : f'{d_hypath}.losses',
        'Duels bws' : f'{d_hypath}.best_overall_winstreak',
        'Duels cws' : f'{d_hypath}.current_winstreak',
        'Duels swings' : f'{d_hypath}.melee_swings',
        'Duels hits' : f'{d_hypath}.melee_hits',
        'Combo swings' : f'{d_hypath}.combo_duel_melee_swings',
        'Combo hits' : f'{d_hypath}.combo_duel_melee_hits',
        'NDB wins' : f'{d_hypath}.potion_duel_wins',
        'NDB losses' : f'{d_hypath}.potion_duel_losses',
        'OP wins' : f'{d_hypath}.op_duel_wins',
        'OP losses' : f'{d_hypath}.op_duel_losses',
        'MWD wins' : f'{d_hypath}.mw_duel_wins',
        'MWD losses' : f'{d_hypath}.mw_duel_losses',
        'Blitzd wins' : f'{d_hypath}.blitz_duel_wins',
        'Blitzd losses' : f'{d_hypath}.blitz_duel_losses',
        'SG wins' : f'{sg_hypath}.wins',
        'SG games' : f'{sg_hypath}.games_played',
        'SG kills' : f'{sg_hypath}.kills',
        'SG deaths' : f'{sg_hypath}.deaths',
        'Pit kills' : f'{pit_hypath}.kills',
        'Pit deaths' : f'{pit_hypath}.deaths',
        'Pit max streak' : f'{pit_hypath}.max_streak',
        'WW wins' : f'{ww_hypath}.wins',
        'WW games' : f'{ww_hypath}.games_played',
        'WW kills' : f'{ww_hypath}.kills',
        'WW deaths' : f'{ww_hypath}.deaths'
    }

    # converts hypaths to stats
    hystats = {key: get_value_from_json(hy, value) for key, value in hypaths.items()}

    # Fixing Hypixel's shitty api
    hystats['NWL'] = round(((math.sqrt((2 * hystats['NWL']) + 30625) / 50) - 2.5), 4)
    if hystats['SW star'] == 0:
        hystats['SW star'] = '[0*]'
    if cfg.devmode: print('Raw SW star:', hystats['SW star'])
    sw_star_in = hystats['SW star']
    sw_star_out = re.sub(r'§.', '', sw_star_in)
    sw_star_out = sw_star_out.strip('[] ')
    sw_star_out = sw_star_out[:-1]
    if cfg.devmode: print('Cleaned SW star:', sw_star_out)
    hystats['SW star'] = sw_star_out
    hystats['SW kdr'] = divide(hystats['SW kills'], hystats['SW deaths'])
    hystats['SW wlr'] = divide(hystats['SW wins'], hystats['SW losses'])
    hystats['BW fkdr'] = divide(hystats['BW fks'], hystats['BW fds'])
    hystats['BW bblr'] = divide(hystats['Beds broken'], hystats['Beds lost'])
    hystats['BW kdr'] = divide(hystats['BW kills'], hystats['BW deaths'])
    hystats['BW fksperstar'] = divide(hystats['BW fks'], hystats['BW star'])
    hystats['Sumo wlr'] = divide(hystats['Sumo wins'], hystats['Sumo losses'])
    hystats['UHCD wlr'] = divide(hystats['UHCD wins'], hystats['UHCD losses'])
    hystats['UHC kills'] = hystats['UHC kills'] + hystats['UHC kills2']
    hystats['UHC deaths'] = hystats['UHC deaths'] + hystats['UHC deaths2']
    hystats['UHC kdr'] = divide(hystats['UHC kills'], hystats['UHC deaths'])
    hystats['Melee Acc'] = divide(hystats['Duels hits'], hystats['Duels swings'])
    hystats['Combo Melee Acc'] = divide(hystats['Combo hits'], hystats['Combo swings'])
    hystats['NDB wlr'] = divide(hystats['NDB wins'], hystats['NDB losses'])
    hystats['OP wlr'] = divide(hystats['OP wins'], hystats['OP losses'])
    hystats['MWD wlr'] = divide(hystats['MWD wins'], hystats['MWD losses'])
    hystats['Blitzd wlr'] = divide(hystats['Blitzd wins'], hystats['Blitzd losses'])
    hystats['Duels wlr'] = divide(hystats['Duels wins'], hystats['Duels losses'])
    hystats['SG games'] = hystats['SG wins'] + hystats['SG games']
    hystats['SG winrate'] = divide(hystats['SG wins'], hystats['SG games'])
    hystats['SG kdr'] = divide(hystats['SG kills'], hystats['SG deaths'])
    hystats['Pit kdr'] = divide(hystats['Pit kills'], hystats['Pit deaths'])
    hystats['WW winrate'] = divide(hystats['WW wins'], hystats['WW games'])
    hystats['WW kdr'] = divide(hystats['WW kills'], hystats['WW deaths'])

    del hystats['UHC kills2']
    del hystats['UHC deaths2']
    # Error avoidance
    hystats = {key: 0 if (str(value)).strip() == '' else value for key, value in hystats.items()}
    hystats = {key: float(value) if value is not None else 0 for key, value in hystats.items()}
    hystats = {key: int(value) if isinstance(value, float) and value.is_integer() else value for key, value in hystats.items()}

    # Active stats dictionary
    active_keys = [key for key, value in y['Active'].items() if value]
    HyStats = {key: value for key, value in hystats.items() if key in active_keys}

    # Sorting
    active_keys_ordered = list(y['Active'].keys())
    HyStats_ordered = {key: HyStats[key] for key in active_keys_ordered if key in HyStats}

    # PRINT STATS
    verdict_score = 0
    for key, value in HyStats_ordered.items():
        tag = get_category(key, value)
        if tag != None:
            if cfg.show_stat_values:
                if tag == 'Safe' and cfg.show_safe:
                    print(f'{tSafe}   || {key}: {value}')
                if tag == 'Risky' and cfg.show_risky:
                    print(f'{tRisky}  || {key}: {c.Yellow}{value}{c.allDefault}')
                    verdict_score += .5
                if tag == 'Danger' and cfg.show_danger:
                    print(f'{tDanger} || {key}: {c.Red}{value}{c.allDefault}')
                    verdict_score += 3
                if tag == 'Dodge' and cfg.show_dodge:
                    print(f'{tDodge}  || {key}: {c.Blue}{value}{c.allDefault}')
                    verdict_score += 6
            else:
                if tag == 'Safe' and cfg.show_safe:
                    print(f'{tSafe}   || {key}')
                if tag == 'Risky' and cfg.show_risky:
                    print(f'{tRisky}  || {key}')
                    verdict_score += .5
                if tag == 'Danger' and cfg.show_danger:
                    print(f'{tDanger} || {key}')
                    verdict_score += 3
                if tag == 'Dodge' and cfg.show_dodge:
                    print(f'{tDodge}  || {key}')
                    verdict_score += 6

    print(f"{c.bgDefault}{c.White}------------------------------------")

    # LISTS
    isTagged = False

    # Guild Flag
    def guild_check_blacklist(g_uuids):
        g_flag = False
        g_matches = 0
        with open(blacklist, 'r') as f:
            lines_set = set(f)
            lines_set = {line.strip('\n') for line in lines_set}

        for uuid in g_uuids:
            if uuid in lines_set:
                if cfg.devmode: print(f'{gname} member {uuid} in blacklist')
                g_matches += 1
        if g_matches > 0:
            if cfg.devmode: print(f'g_matches: {g_matches}')
            print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} GUILD FLAG {c.bgDefault}{c.LightYellow} << {c.Default}")
            g_flag = True
        return g_flag


    if inGuild: guild_check_blacklist(g_uuids)
    g_flag = guild_check_blacklist
    if g_flag:
        verdict_score += 2


    # Name Flag
    if len(name) < 4:
        print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} NAME FLAG {c.bgDefault}{c.LightYellow} << {c.Default}")
        verdict_score += 3
    for nameflag in cfg.nameflags:
        if nameflag in name:
            print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} NAME FLAG {c.bgDefault}{c.LightYellow} << {c.Default}")
            verdict_score += 3

    # Api off
    if hystats['Duels bws'] == 0 and hystats['Duels wins'] > 5:
        print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} WS API OFF {c.bgDefault}{c.LightYellow} << {c.Default}")
        isTagged = True
        verdict_score += 3

    # Projectiles Off
    if cfg.devmode: print(f"disabledProjectileTrails: {get_value_from_json(hy, 'player.disabledProjectileTrails')}")
    if get_value_from_json(hy, 'player.disabledProjectileTrails'):
        print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} Projectile Trail Disabled {c.bgDefault}{c.LightYellow} << {c.Default}")
        verdict_score += 2
        isTagged = True

    # Read blacklist
    with open(blacklist, 'r') as bl:
        for line in bl.readlines():
            line = line.strip()
            if target_uuid != None:
                if line == target_uuid:
                    print(f"{c.LightBlue} >> {c.bgBlue}{c.Black} BLACKLISTED! {c.bgDefault}{c.LightBlue} << {c.Default}")
                    verdict_score += 10
                    isTagged = True
                if target_uuid in line and '[$] ' in line:
                    print(f"{c.LightBlue} >> {c.bgBlue}{c.Black} [$] BLACKLISTED! {c.bgDefault}{c.LightBlue} << {c.Default}")
                    verdict_score += 8
                    isTagged = True

    # Read safelist
    with open(safelist, 'r') as sl:
        for line in sl.readlines():
            line = line.strip()
            if target_uuid != None:
                if line == target_uuid:
                    print(f"{c.LightGreen} >> {c.bgGreen}{c.Black} SAFELISTED! {c.bgDefault}{c.LightGreen} << {c.Default}")
                    verdict_score -= 5
                    isTagged = True
                if target_uuid in line and '[$]' in line:
                    print(f"{c.LightGreen} >> {c.bgGreen}{c.Black} [$] SAFELISTED! {c.bgDefault}{c.LightGreen} << {c.Default}")
                    verdict_score -= 4
                    isTagged = True
                if target_uuid in line and '[SOSAFE]' in line:
                    print(f"{c.LightGreen} >> {c.bgGreen}{c.Black} SO SAFE! {c.bgDefault}{c.LightGreen} << {c.Default}")
                    verdict_score -= 8
                    isTagged = True


    # Read weirdlist
    with open(weirdlist, 'r') as wl:
        for line in wl.readlines():
            line = line.strip()
            if target_uuid != None:
                if line == target_uuid:
                    print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} WEIRD! {c.bgDefault}{c.LightYellow} << {c.Default}")
                    verdict_score += 3
                    isTagged = True
                if target_uuid in line and '[$] ' in line:
                    print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} [$] WEIRD! {c.bgDefault}{c.LightYellow} << {c.Default}")
                    verdict_score += 2
                    isTagged = True

    # Read notes
    with open(notes, 'r') as rnotes:
        for nline in rnotes.readlines():
            if target_uuid != None:
                if target_uuid in nline:
                    if cfg.devmode: print(nline)
                    start = nline.index('Note: "')
                    end = nline.index('"\n', start+1)
                    note = nline[start+7:end]
                    print(f' {c.White}>>{c.allDefault} {c.bgLightBlue}{c.Black} Note: {note} {c.allDefault} {c.White}<<{c.allDefault} ')
                    isTagged = True

    # VERDICT
    def get_verdict(value):
        verdicts = y["Verdicts"]
        for verdict, (start, end) in verdicts.items():
            if start == None: start = float('-inf')
            if end == None: end = float('inf')
            if start <= value < end:
                return verdict
        return "Error"
    
    verdict = get_verdict(verdict_score)
    if verdict == "You're straight chilling af":
        verdict = f"{c.bgGreen}{c.Black} {verdict} {c.allDefault}"
        verdict_score = f"{c.Green}{verdict_score}{c.allDefault}"
    elif verdict == "Prolly stay":
        verdict = f"{c.bgLightGreen}{c.Black} {verdict} {c.allDefault}"
        verdict_score = f"{c.LightGreen}{verdict_score}{c.allDefault}"
    elif verdict == "Sorta scary":
        verdict = f"{c.bgYellow}{c.Black} {verdict} {c.allDefault}"
        verdict_score = f"{c.Yellow}{verdict_score}{c.allDefault}"
    elif verdict == "Dodge":
        verdict = f"{c.bgRed}{c.Black} {verdict} {c.allDefault}"
        verdict_score = f"{c.Red}{verdict_score}{c.allDefault}"
    elif verdict == "DODGE NOW":
        verdict = f"{c.bgBlue}{c.Black} {verdict} {c.allDefault}"
        verdict_score = f"{c.Blue}{verdict_score}{c.allDefault}"
    elif verdict == "Error":
        verdict = f"{c.bgLightGray}{c.Black} {verdict} {c.allDefault}"
        verdict_score = f"{c.LightGray}{verdict_score}{c.allDefault}"
    else:
        print("lol wtf happened")

    if isTagged: print(f"{c.bgDefault}{c.White}------------------------------------")
    if cfg.show_verdict_score:
        print(f"Verdict score: {verdict_score}")
    print(f"Verdict: {verdict}")
    print(f"{c.bgDefault}{c.White}------------------------------------")

    # Read record
    rec_lost_uuids = []
    rec_won_uuids = []
    autobl_list = []
    autosl_list = []
    autososafe_list = []
    with open(record, 'r') as rrec:
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
            if uuidcount > cfg.autososafe_win_count-1:
                autososafe_list.append(uuid_)

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
        
        for _uuid in autososafe_list:
            uuidcount = countOf(autososafe_list, _uuid)
            if uuidcount > 1:
                uuidindex = autososafe_list.index(_uuid)
                autososafe_list.pop(uuidindex)

    if cfg.devmode:
        print(f'Auto blacklist list: {autobl_list}')
        print(f'Auto safelist list: {autosl_list}')
        print(f'Auto sosafe list: {autososafe_list}')


    # Autolist
    if cfg.autoblacklist_loss_count > 0:
        with open(blacklist, 'a') as abl:
            for uuid in autobl_list:
                abl.write(f'{uuid}\n')
        dd(blacklist)

    if cfg.autosafelist_win_count > 0:
        with open(safelist, 'a') as asl:
            for uuid in autosl_list:
                asl.write(f'{uuid}\n')
        dd(safelist)

    if cfg.autososafe_win_count > 0:
        with open(safelist, 'a') as ass:
            for uuid in autososafe_list:
                ass.write(f'[SOSAFE] {uuid}\n')
        dd(safelist)

    if len(autobl_list) > 1:
        autobl_list.clear()
        if cfg.devmode: print(f'Cleared autobl_list')
    
    if len(autosl_list) > 1:
        autosl_list.clear()
        if cfg.devmode: print(f'Cleared autosl_list')

readchat()

