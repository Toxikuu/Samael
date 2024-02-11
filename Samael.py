# import libraries
import math, time, os, sys, configparser

try:
    import requests
except ModuleNotFoundError:
    os.sys('pip install requests')

# variables
version = '5.0.2'
discord = "https://discord.gg/N3rVjjVEsv"
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
config_file = f'{script_directory}/config.ini'

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

# config
def readcfg():
    config_object = configparser.ConfigParser()
    with open(config_file, 'r') as file_object:
        config_object.read_file(file_object)
        global devmode, blacklist, safelist, weirdlist, record, chat, notes, apikey, safenicks, rounding_precision, show_splash_screen, samaeluser, custom_ranks, autosafelist_win_count, autoblacklist_loss_count, delimiter_type

        devmode = config_object.get('devmode', 'dev')

        blacklist = config_object.get('paths', 'blacklist')
        safelist = config_object.get('paths', 'safelist')
        weirdlist = config_object.get('paths', 'weirdlist')
        record = config_object.get('paths',  'record')
        chat = config_object.get('paths', 'chat')
        notes = config_object.get('paths', 'notes')

        apikey = config_object.get('apikey', 'apikey')

        safenicks = config_object.get('safenicks', 'safenicks')

        rounding_precision = int(config_object.get('options', 'rounding_precision'))
        show_splash_screen = config_object.get('options', 'show_splash_screen')

        samaeluser = config_object.get('user', 'username')

        custom_ranks = config_object.get('ranks', 'custom_ranks')

        autosafelist_win_count = int(config_object.get('autolist', 'autosafelist_win_count'))
        autoblacklist_loss_count = int(config_object.get('autolist', 'autoblacklist_loss_count'))

        delimiter_type = int(config_object.get('delimiter', 'delimiter_type'))

        # fix list formatting
        custom_ranks = list(custom_ranks.split(', '))
        safenicks = list(safenicks.split(', '))

readcfg()


# delimiter fix
if delimiter_type == 0:
    delimiter = '▌'
    print(delimiter)
elif delimiter_type == 1:
    delimiter = '?'

# confirms config validity
checked_cfgvars = [devmode, blacklist, safelist, weirdlist, record, chat,  notes, apikey, rounding_precision, show_splash_screen, samaeluser, autosafelist_win_count, autoblacklist_loss_count] 
cfgerrors = 0
for cfgvar in checked_cfgvars:
    if cfgvar == "":
        cfgerrors += 1

if cfgerrors != 0:  
    print(f"\n{c.bgRed} >> EMPTY VALUE FOR {cfgerrors} VARIABLES IN CONFIG << {c.allDefault}\n")

samael_lists = [blacklist, safelist, weirdlist]

# rnklist
rnklist = ['[MVP++]', '[MVP+]', '[MVP]', '[VIP+]', '[VIP]', '[ADMIN]', '[YOUTUBE]', '§d[? GG]', '§6[KING§c++§6]', '§0[UHC]', '§d[NEA?]', '§0[TOX]', '§0[GOLF§1+++§0]', '§5[ASHLYN]', '§0[LESBIAN]']
if custom_ranks != '':
    rnklist.extend(custom_ranks)

# devmode
if devmode == 'y':
    print('Launching in devmode\n\n')
    with open(config_file, 'r') as file_object_dev:
        config_data_dev = file_object_dev.read()
    print(config_data_dev)
    print(f'rnklist: {rnklist}')

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
        print(f'Failed to access uuid for {ign}!')

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

def filter_safelist_and_blacklist(safelist, blacklist):
    common_elements = set(safelist) & set(blacklist)
    new_safelist = [item for item in safelist if item not in common_elements]
    return new_safelist, blacklist

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

# splash screen
if show_splash_screen == 'y':
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
with open(record, 'w') as clrrec:
    clrrec.write('')

# read chat
def readchat():
    while True:


        chatlines = follow(open(chat, 'r'))
        for line in chatlines:
            
            # sc
            for rnk in rnklist:
                if f"[Client thread/INFO]: [CHAT] {delimiter} {rnk}" in line:
                    if devmode == 'y': print('Name detected')
                    rnklen = len(rnk)
                    start = line.index(rnk)
                    end = line.index('Lvl:',start+1)

                    name = line[start+(rnklen+1):end-1]
                    antisniper(name, rnk)

            # mysterybox fix
            if "[Client thread/INFO]: [CHAT] ? " in line and "found a" in line and "Mystery Box" in line:
                pass

            # nons
            elif f"[Client thread/INFO]: [CHAT] {delimiter} " in line and f"[Client thread/INFO]: [CHAT] {delimiter} [" not in line and f"[Client thread/INFO]: [CHAT] {delimiter} W/L:" not in line:
                if "§" not in line:
                    start = line.index(f'{delimiter} ')
                    end = line.index('Lvl:',start+1)

                    name = line[start+2:end-1]
                    rank = "[NON]"
                    antisniper(name, rank)
                else:
                    pass

            # nicks
            if f"[Client thread/INFO]: [CHAT] Lilith > Found" in line and " likely nicked players: Possibly " in line:

                nickstart = line.index("Possibly ")
                nickend = line.index('\n', nickstart+1)
                name_nick = line[nickstart+9:nickend]
                name_nick = name_nick.strip(', ')
                if devmode == 'y':
                    print(f'Nick found: {name_nick}')

                rank = '[NICK?]'
                try: 
                    antisniper(name_nick, rank)
                except: 
                    for safenick in safenicks:
                        if safenick in line:
                            pass
                        else:
                            if name_nick != '':
                                omgnick()

            # Write record
            if "[Client thread/INFO]: [CHAT]   " in line and "WINNER!  " in line:
                start = line.index('WINNER!  ')
                end = line.index('\n',start+1)

                won_opponent = line[start+9:end]
                for rnk in rnklist:
                    if rnk in won_opponent:
                        won_opponent = won_opponent.replace(rnk, '')
                won_opponent = won_opponent.strip()
                
                print(f"\n [i] You won against {won_opponent}")
                won_uuid = igntouuid(won_opponent)
                print(f"\n [-] UUID: {won_uuid}")

                with open(record, 'a') as wrec:
                    wrec.write(f"Won against {won_uuid}\n")
            
            elif "[Client thread/INFO]: [CHAT]   " in line and "WINNER!\n" in line:
                start = line.index('  ')
                end = line.index('WINNER!',start+1)
                lost_opponent = line[start+2:end-1]
                lost_opponent = lost_opponent = lost_opponent.replace(samaeluser, '')
                for rnk in rnklist:
                    if rnk in lost_opponent:
                        lost_opponent = lost_opponent.replace(rnk, '')
                lost_opponent = lost_opponent.strip()

                print(f"\n [i] You lost to {lost_opponent}")
                lost_uuid = igntouuid(lost_opponent)
                print(f"\n [-] UUID: {lost_uuid}")

                with open(record, 'a') as wrec:
                    wrec.write(f"Lost to {lost_uuid}\n")
            

            # commands
            addcommands = ['b', 's', 'w']
            for addcommand in addcommands:
                if f"[Client thread/INFO]: [CHAT] -{addcommand}" in line:
                    start = line.index(f'-{addcommand}')
                    end = line.index('\n', start+1)
                    name = line[start+3:end]

                    print('> Fetching uuid for', name)
                    try:
                        uuid = igntouuid(name)

                        if addcommand == 'b':
                            print(f"> Blacklisting", uuid)
                            with open(f"{blacklist}", "a") as bl:
                                bl.write(f"\n{uuid}\n")
                            print(f"> Added {name} to blacklist\n")


                        elif addcommand == 's':
                            print(f"> Safelisting", uuid)
                            with open(f"{safelist}", "a") as sl:
                                sl.write(f"\n{uuid}\n")
                            print(f"> Added {name} to safelist\n")


                        elif addcommand == 'w':
                            print(f"> Weirdlisting", uuid)
                            with open(f"{weirdlist}", "a") as wl:
                                wl.write(f"\n{uuid}\n")
                            print(f"> Added {name} to weirdlist\n")


                    except KeyError:
                        print("Error: invalid ign")


            removecommands = ['rb', 'rs', 'rw']
            for removecommand in removecommands:
                if f"[Client thread/INFO]: [CHAT] -{removecommand}" in line:
                    start = line.index(f'-{removecommand}')
                    end = line.index('\n', start+1)
                    name = line[start+4:end]

                    print("> Fetching uuid for", name)
                    try:
                        uuid = igntouuid(name)

                        if removecommand == 'rb':
                            print(f"> Removing {uuid} from blacklist")
                            with open(f"{blacklist}", "r") as findbl:
                                data = findbl.read()
                                data = data.replace(uuid, '\n')
                            with open(f"{safelist}", "w") as findbl:
                                findbl.write(data)

                        elif removecommand == 'rs':
                            print(f"> Removing {uuid} from safelist")
                            with open(f"{safelist}", "r") as findsl:
                                data = findsl.read()
                                data = data.replace(uuid, '\n')
                            with open(f"{safelist}", "w") as findsl:
                                findsl.write(data)

                        elif removecommand == 'rw':
                            print(f"> Removing {uuid} from weirdlist")
                            with open(f"{weirdlist}", "r") as findwl:
                                data = findwl.read()
                                data = data.replace(uuid, '\n')
                            with open(f"{weirdlist}", "w") as findwl:
                                findwl.write(data)

                    except KeyError:
                        print("Error: invalid ign")

            if "[Client thread/INFO]: [CHAT] -api" in line:
                start = line.index('-api')
                end = line.index('\n', start+1)
                apikey = line[start+5:end]

                print(f"\n> Updating api key")

                config = configparser.ConfigParser()
                config.read(config_file)
                config.set('apikey', 'apikey', apikey)

                with open(config_file, 'w') as file_object:
                    config.write(file_object)
                print(f"> Successfully updated")
                readcfg()


            if "[Client thread/INFO]: [CHAT] -refresh" in line:
                readcfg()

            if "[Client thread/INFO]: [CHAT] -dd" in line:
                for samael_list in samael_lists:
                    dd(samael_list)
                print('Fixed list formatting!')

            if "[Client thread/INFO]: [CHAT] -filter" in line:
                with open(safelist, 'r') as sl:
                    slist = sl.readlines()
                with open(blacklist, 'r') as bl:
                    blist = bl.readlines()
                
                new_safelist, new_blacklist = filter_safelist_and_blacklist(slist, blist)
                
                write_list_to_txt(new_safelist, safelist)
                write_list_to_txt(new_blacklist, blacklist)
                print('Filtered lists')
                for samael_list in samael_lists:
                    dd(samael_list)
                print('Fixed list formatting!')

            if "[Client thread/INFO]: [CHAT] -clr" in line:
                with open(record, 'w') as clrrec:
                    clrrec.write('')
                print('Cleared record!')

            if "[Client thread/INFO]: [CHAT] -note" in line:
                print(line)
                namestart = line.index('-note')
                nameend = line.index(' "', namestart+1)
                name = line[namestart+6:nameend]
                print(f' [n] Target: {name}')
                notestart = line.index(' "')
                noteend = line.index('\n', notestart+1)
                note = line[notestart+2:noteend]
                print(f' [n] Note: {note}')
                print(f" [n] Grabbing {name}'s uuid")
                try:
                    note_uuid = igntouuid(name)

                    print(f" [n] UUID: {note_uuid}")
                    print(f" [n] Taking notes")
                    with open(notes, 'a') as nappend:
                        nappend.write(f'Target: {name} UUID: {note_uuid} Note: "{note}"\n')
                    print(f" [n] Noted {name}")
                except:
                    print(f" [n] Note error")


# antisniper
def antisniper(name, rank):
        print(f"\n\n{c.stBold}Checking: {rank} {name}{c.allDefault}")   

        uuid = igntouuid(name)
        
        url = f"https://api.hypixel.net/player?key={apikey}&uuid={uuid}"
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
        
        stat_bblr = round((stat_bedwars_beds_broken/max(stat_bedwars_beds_lost,1)),rounding_precision)
        stat_fkdr = round((stat_bedwars_final_kills/max(stat_bedwars_final_deaths,1)), rounding_precision)
        stat_bw_kdr = round(stat_bw_kills/max(stat_bw_deaths,1), rounding_precision)
        stat_bw_fksperstar = round(stat_bedwars_final_kills/max(stat_bedwars_star,1), rounding_precision)


        # SKYWARS
        try: stat_level_formatted = data["player"]["stats"]["SkyWars"]["levelFormatted"]
        except KeyError: stat_level_formatted = "xx0x"

        try: stat_skywars_kills = data["player"]["stats"]["SkyWars"]["kills"]
        except KeyError: stat_skywars_kills = 0

        try: stat_skywars_deaths = data["player"]["stats"]["SkyWars"]["deaths"]
        except KeyError: stat_skywars_deaths = 0

        stat_skywars_kdr = round((stat_skywars_kills/max(stat_skywars_deaths,1)), rounding_precision)
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

        sumowlr = round((stat_sumo_duel_wins/max(stat_sumo_duel_losses, 1)), rounding_precision)


        # UHC DUELS
        try: stat_uhc_duel_wins = data["player"]["stats"]["Duels"]["uhc_duel_wins"]
        except KeyError: stat_uhc_duel_wins = 0

        try: stat_uhc_duel_losses = data["player"]["stats"]["Duels"]["uhc_duel_losses"]
        except KeyError: stat_uhc_duel_losses = 0

        uhcwlr = round((stat_uhc_duel_wins/max(stat_uhc_duel_losses, 1)), rounding_precision)


        # REAL UHC
        try: stat_UHC_kills = data["player"]["stats"]["UHC"]["kills_solo"] + data["player"]["stats"]["UHC"]["kills"]
        except KeyError: stat_UHC_kills = 0

        try: stat_UHC_deaths = data["player"]["stats"]["UHC"]["deaths_solo"] + data["player"]["stats"]["UHC"]["deaths"]
        except KeyError: stat_UHC_deaths = 0

        uhckdr = round((stat_UHC_kills/max(stat_UHC_deaths, 1)), rounding_precision)


        # GENERAL DUELS
        try: stat_duels_wins = data["player"]["stats"]["Duels"]["wins"]
        except KeyError: stat_duels_wins = 0

        try: stat_duels_losses = data["player"]["stats"]["Duels"]["losses"]
        except KeyError: stat_duels_losses = 0

        try: stat_duels_bws = data["player"]["stats"]["Duels"]["best_overall_winstreak"]
        except KeyError: stat_duels_bws = 0

        try: stat_duels_cws = data["player"]["stats"]["Duels"]["current_winstreak"]
        except KeyError: stat_duels_cws = 0

        wlr = round((stat_duels_wins/max(stat_duels_losses, 1)), rounding_precision)

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
        stat_melee_accuracy = round((nocombomeleehits/max(nocombomeleeswings,1)*100), rounding_precision)
        stat_combo_melee_accuracy = round((stat_duels_combo_melee_hits/max(stat_duels_combo_melee_swings,1)*100), rounding_precision)

        # NWL
        try: hypixelxp = data["player"]["networkExp"]
        except KeyError: hypixelxp = 0

        nwl = round(((math.sqrt((2 * hypixelxp) + 30625) / 50) - 2.5), rounding_precision)


        # DISPLAY STATS
        print(f"{c.bgDefault}{c.DarkGray}UUID:", uuid)
        print(f"{c.bgDefault}{c.White}------------------------------------")
        if 15 < nwl < 100:
            print(f"{tSafe}    ||   NWL: {nwl}") 
        elif (100 < nwl < 200) or (5 < nwl < 15):
            print(f"{tRisky}   ||   NWL: {c.Yellow}{nwl}")
        elif nwl < 5:
            print(f"{tDanger}  ||   NWL: {c.Red}{nwl}")
        else:
            print(f"{tDanger}  ||   NWL: {c.Red}{nwl}")

        if 0 < intswstar < 10:
            print(f"{tSafe}    ||   SW star: {swstar}")
        elif intswstar < 15 or intswstar == 0:
            print(f"{tRisky}   ||   SW star: {c.Yellow}{swstar}")
        elif intswstar > 15:
            print(f"{tDanger}  ||   SW star: {c.Red}{swstar}")

        if stat_skywars_kdr < 1:
            print(f"{tSafe}    ||   SW kdr: {stat_skywars_kdr}")
        elif stat_skywars_kdr > 1 and stat_skywars_kdr < 2:
            print(f"{tRisky}   ||   SW kdr: {c.Yellow}{stat_skywars_kdr}")
        elif stat_skywars_kdr > 2:
            print(f"{tDanger}  ||   SW kdr: {c.Red}{stat_skywars_kdr}")

        if stat_bedwars_star < 200 and stat_bedwars_star != 0:
            print(f"{tSafe}    ||   BW star: {stat_bedwars_star} ☆")
        elif stat_bedwars_star > 200 and stat_bedwars_star < 350:
            print(f"{tRisky}   ||   BW star: {c.Yellow}{stat_bedwars_star} ☆")
        elif stat_bedwars_star > 350 or stat_bedwars_star == 0:
            print(f"{tDanger}  ||   BW star: {c.Red}{stat_bedwars_star} ☆")

        if stat_fkdr < 2 and stat_fkdr != 0:
            print(f"{tSafe}    ||   FKDR: {stat_fkdr}")
        elif stat_fkdr > 2 and stat_fkdr < 3.5:
            print(f"{tRisky}   ||   FKDR: {c.Yellow}{stat_fkdr}")
        elif stat_fkdr > 3.5:
            print(f"{tDanger}  ||   FKDR: {c.Red}{stat_fkdr}")
        else:
            print(f"{tRisky}   ||   FKDR: {c.Yellow}{stat_fkdr}")

        if stat_bblr < 1.4 and stat_bblr != 0:
            print(f"{tSafe}    ||   BBLR: {stat_bblr}")
        elif stat_bblr > 1.4 and stat_bblr < 2.8:
            print(f"{tRisky}   ||   BBLR: {c.Yellow}{stat_bblr}")
        elif stat_bblr > 2.8:
            print(f"{tDanger}  ||   BBLR: {c.Red}{stat_bblr}")
        else:
            print(f"{tRisky}   ||   BBLR: {c.Yellow}{stat_bblr}")    
        
        if stat_bw_kdr < 1.2:
            print(f"{tSafe}    ||   BW kdr: {stat_bw_kdr}")
        elif stat_bw_kdr > 1.2 and stat_bw_kdr < 2.4:
            print(f"{tRisky}   ||   BW kdr: {c.Yellow}{stat_bw_kdr}")
        elif stat_bw_kdr > 2.4:
            print(f"{tDanger}  ||   BW kdr: {c.Red}{stat_bw_kdr}")
        
        if stat_bw_fksperstar < 25:
            print(f"{tSafe}    ||   BW fks/star: {stat_bw_fksperstar}")
        elif stat_bw_fksperstar > 25 and stat_bw_fksperstar < 50:
            print(f"{tRisky}   ||   BW fks/star: {c.Yellow}{stat_bw_fksperstar}")
        elif stat_bw_fksperstar > 50:
            print(f"{tDanger}  ||   BW fks/star: {c.Red}{stat_bw_fksperstar}")
        
        if sumowlr < 1.1:
            print(f"{tSafe}    ||   Sumo wlr: {sumowlr}")
        elif sumowlr > 1.1 and sumowlr < 1.6:
            print(f"{tRisky}   ||   Sumo wlr: {c.Yellow}{sumowlr}")
        elif sumowlr > 1.6:
            print(f"{tDanger}  ||   Sumo wlr: {c.Red}{sumowlr}")   
        
        if stat_sumo_bws < 10 and stat_sumo_bws != 0:
            print(f"{tSafe}    ||   Sumo bws: {stat_sumo_bws}")
        elif stat_sumo_bws > 10 and stat_sumo_bws < 25:
            print(f"{tRisky}   ||   Sumo bws: {c.Yellow}{stat_sumo_bws}")
        elif stat_sumo_bws > 25 or (stat_sumo_bws == 0 and stat_sumo_duel_wins > 0):
            print(f"{tDanger}  ||   Sumo bws: {c.Red}{stat_sumo_bws}")
        else:
            print(f"{tRisky}   ||   Sumo bws: {c.Yellow}{stat_sumo_bws}")

        if stat_sumo_cws < 5:
            print(f"{tSafe}    ||   Sumo cws: {stat_sumo_cws}")
        elif stat_sumo_cws > 5 and stat_sumo_cws < 10:
            print(f"{tRisky}   ||   Sumo cws: {c.Yellow}{stat_sumo_cws}")
        elif stat_sumo_cws > 10:
            print(f"{tDanger}  ||   Sumo cws: {c.Red}{stat_sumo_cws}")
        else:
            print(f"{tSafe}    ||   Sumo cws: {stat_sumo_cws}")
        
        if uhcwlr < 1:
            print(f"{tSafe}    ||   UHCD wlr: {uhcwlr}")
        elif uhcwlr > 1 and uhcwlr < 2.5:
            print(f"{tRisky}   ||   UHCD wlr: {c.Yellow}{uhcwlr}")
        elif uhcwlr > 2.5:
            print(f"{tDanger}  ||   UHCD wlr: {c.Red}{uhcwlr}")
        
        if uhckdr < 0.5:
            print(f"{tSafe}    ||   UHC kdr: {uhckdr}")
        elif uhckdr > 0.5 and uhckdr < 1.5:
            print(f"{tRisky}   ||   UHC kdr: {c.Yellow}{uhckdr}")
        elif uhckdr > 1.5:
            print(f"{tDanger}  ||   UHC kdr: {c.Red}{uhckdr}")
  
        if wlr < 1.5 or (wlr == 0 and stat_duels_losses > 0):
            print(f"{tSafe}    ||   Wlr: {wlr}")
        elif wlr > 1.5 and wlr < 2.5:
            print(f"{tRisky}   ||   Wlr: {c.Yellow}{wlr}")
        elif wlr > 2.5 or (wlr == 0 and stat_duels_losses == 0):
            print(f"{tDanger}  ||   Wlr: {c.Red}{wlr}")      
        
        if stat_duels_wins > 10 and stat_duels_wins < 10000:
            print(f"{tSafe}    ||   Wins: {stat_duels_wins}")
        elif (stat_duels_wins > 3 and stat_duels_wins < 10) or (stat_duels_wins > 10000 and stat_duels_wins < 20000):
            print(f"{tRisky}   ||   Wins: {c.Yellow}{stat_duels_wins}")
        elif (stat_duels_wins < 3 and (stat_duels_losses < 4 * stat_duels_wins)) or (stat_duels_wins > 20000):
            print(f"{tDanger}  ||   Wins: {c.Red}{stat_duels_wins}")
        else:
            print(f"{tSafe}    ||   Wins: {stat_duels_wins}")       

        if stat_duels_losses > 10:
            print(f"{tSafe}    ||   Losses: {stat_duels_losses}")
        elif stat_duels_losses > 3 and stat_duels_losses < 10:
            print(f"{tRisky}   ||   Losses: {c.Yellow}{stat_duels_losses}")
        elif stat_duels_losses < 3:
            print(f"{tDanger}  ||   Losses: {c.Red}{stat_duels_losses}")
        else:
            print(f"{tSafe}    ||   Losses: {stat_duels_losses}")  
        
        if stat_duels_bws < 25 and stat_duels_bws != 0:
            print(f"{tSafe}    ||   Bws: {stat_duels_bws}")
        elif stat_duels_bws > 25 and stat_duels_bws < 50:
            print(f"{tRisky}   ||   Bws: {c.Yellow}{stat_duels_bws}")
        elif stat_duels_bws > 50 or stat_duels_bws == 0:
            print(f"{tDanger}  ||   Bws: {c.Red}{stat_duels_bws}")

        if stat_duels_cws < 5:
            print(f"{tSafe}    ||   Cws: {stat_duels_cws}")
        elif stat_duels_cws > 5 and stat_duels_cws < 15:
            print(f"{tRisky}   ||   Cws: {c.Yellow}{stat_duels_cws}")
        elif stat_duels_cws > 15:
            print(f"{tDanger}  ||   Cws: {c.Red}{stat_duels_cws}")
        else:
            print(f"{tSafe}    ||   Cws: {stat_duels_cws}")
        
        if stat_melee_accuracy < 50 and stat_melee_accuracy != 0:
            print(f"{tSafe}    ||   mAccuracy: {stat_melee_accuracy} %")
        elif stat_melee_accuracy > 50 and stat_melee_accuracy < 70:
            print(f"{tRisky}   ||   mAccuracy: {c.Yellow}{stat_melee_accuracy} %")
        elif stat_melee_accuracy > 70 or stat_melee_accuracy == 0:
            print(f"{tDanger}  ||   mAccuracy: {c.Red}{stat_melee_accuracy} %")
        
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
        with open(blacklist, 'r') as bl:
            for line in bl.readlines():
                line = line.strip()
                if line == uuid:
                    if api_on == False: print('')
                    print(f"{c.LightBlue} >> {c.bgBlue}{c.Black} BLACKLISTED! {c.bgDefault}{c.LightBlue} << {c.Default}")

        # Read safelist
        with open(safelist, 'r') as sl:
            for line in sl.readlines():
                line = line.strip()
                if line == uuid:
                    if api_on == False: print('')
                    print(f"{c.LightGreen} >> {c.bgGreen}{c.Black} SAFELISTED! {c.bgDefault}{c.LightGreen} << {c.Default}")

        # Read weirdlist
        with open(weirdlist, 'r') as wl:
            for line in wl.readlines():
                line = line.strip()
                if line == uuid:
                    if api_on == False: print('')
                    print(f"{c.LightYellow} >> {c.bgYellow}{c.Black} WEIRD! {c.bgDefault}{c.LightYellow} << {c.Default}")

        # Read notes
        with open(notes, 'r') as rnotes:
            for nline in rnotes.readlines():
                if uuid in nline:
                    if devmode == 'y': print(nline)
                    start = nline.index('Note: "')
                    end = nline.index('"\n', start+1)
                    note = nline[start+7:end]
                    print(f' {c.White}>>{c.allDefault} {c.bgLightBlue}{c.Black} Note: {note} {c.allDefault} {c.White}<<{c.allDefault} ')

        # Read record
        rec_lost_uuids = []
        rec_won_uuids = []
        autobl_list = []
        autosl_list = []
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
                if uuidcount > autoblacklist_loss_count-1:
                    autobl_list.append(uuid_)

            for uuid_ in rec_won_uuids:
                uuidcount = countOf(rec_won_uuids, uuid_)
                if uuidcount > autosafelist_win_count-1:
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
        if devmode == 'y':
            print(f'Auto blacklist list: {autobl_list}')
            print(f'Auto safelist list: {autosl_list}')

        # Autolist
        if autoblacklist_loss_count > 0:
            with open(blacklist, 'a') as abl:
                for autobl_uuid in autobl_list:
                    abl.write(f'{autobl_uuid}\n')
            dd(blacklist)

        if autosafelist_win_count > 0:
            with open(safelist, 'a') as asl:
                for autosl_uuid in autosl_list:
                    asl.write(f'{autosl_uuid}\n')
            dd(safelist)


readchat()
