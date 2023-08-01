import requests
import json
import math, time, os, subprocess
from pathlib import Path

# for api calls
def getInfo(call):
    r = requests.get(call)
    return r.json()

# colors class
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
    bgDarkGray     = "\033[100m"
    bgLightRed     = "\033[101m"
    bgLightGreen   = "\033[102m"
    bgLightYellow  = "\033[103m"
    bgLightBlue    = "\033[104m"
    bgLightMagenta = "\033[105m"
    bgLightCyan    = "\033[106m"
    bgWhite        = "\033[107m"


# chill variables (very chill)
rounding_precision = 3
version = "4.2.3"
discord = "https://discord.gg/N3rVjjVEsv"

# directories for shit
home = str(Path.home())
samaeldir = (home+r"\Samael "+version)

blacklist = (samaeldir+r"\blacklist.txt")
safelist = (samaeldir+r"\safelist.txt")
apikeydir = (samaeldir+r"\apikey.txt")
weirdlist = (samaeldir+r"\weirdlist.txt")
safenick1 = "AbigailCruz1998"



apikeyfile = open(apikeydir, "r")
apikey = apikeyfile.read()






# splash screen
print("\n")
print(f"{c.Red}███████╗ █████╗ ███╗   ███╗ █████╗ ███████╗██╗     ")
print(f"{c.Red}██╔════╝██╔══██╗████╗ ████║██╔══██╗██╔════╝██║     ")
print(f"{c.Red}███████╗███████║██╔████╔██║███████║█████╗  ██║     ")
print(f"{c.Red}╚════██║██╔══██║██║╚██╔╝██║██╔══██║██╔══╝  ██║     ")
print(f"{c.Red}███████║██║  ██║██║ ╚═╝ ██║██║  ██║███████╗███████╗")
print(f"{c.Red}╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝")
                                                                                                         

print(f"{c.bgDefault}{c.White}\n >>> Version {version}")
print(f"{c.bgDefault}{c.White} > Use alongside Lilith")
print(f"{c.bgDefault}{c.White} > Made by Toxikuu, DuelsHollow, & Scycle")
print(f"{c.bgDefault}{c.White} > This project is free and open source. Feel free to change whatever you like, make improvements, make forks, add new features, and do whatever you want with this <3")
print(f"{c.bgDefault}{c.White} > Special thanks to:")
print(f"{c.bgDefault}{c.White}     > Nolqk, Zani, Sedged, DuelsHollow, Yhuvko, Praxzz, Virse, Plonk, Scycle, i5tar, Nea, Nuclear")
print(f"{c.bgDefault}{c.White} > Join the Discord! {discord}")

print("\n\n")


# checks if a process exists (this is to figure out what client youre using and from that the path of the latest.log)
def process_exists(process_name):
    progs = str(subprocess.check_output('tasklist'))
    if process_name in progs:
        # print("process name is in programs") [DEBUGGING]
        return True
    else:
        # print("process name is NOT in programs") [DEBUGGING]
        return False


# does the funny antisniping thing
def antisniper():
    print(f"{c.bgDefault}{c.White}---------")

    blacklist = (samaeldir+r"\blacklist.txt")
    safelist = (samaeldir+r"\safelist.txt")
    weirdlist = (samaeldir+r"\weirdlist.txt")

    try:
        resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
        uuid = resp.json()["id"]

    except KeyError:
        print("\n-MOJANG API ERROR-\n")

    

    url = f"https://api.hypixel.net/player?key={apikey}&uuid={uuid}"
    
    data = getInfo(url)


    try:
        stat_bedwars_star = data["player"]["achievements"]["bedwars_level"]
    except KeyError:
        stat_bedwars_star = 0
    try:
        stat_bedwars_final_kills = data["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
    except KeyError:
        stat_bedwars_final_kills = 0
    try:
        stat_bedwars_final_deaths = data["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
    except KeyError:
        stat_bedwars_final_deaths = 0

    try:
        stat_level_formatted = data["player"]["stats"]["SkyWars"]["levelFormatted"]
    except KeyError:
        stat_level_formatted = "xx0x"
    try:
        stat_skywars_kills = data["player"]["stats"]["SkyWars"]["kills"]
    except KeyError:
        stat_skywars_kills = 0
    try:
        stat_skywars_deaths = data["player"]["stats"]["SkyWars"]["deaths"]
    except KeyError:
        stat_skywars_deaths = 0


    stat_fkdr = round((stat_bedwars_final_kills/max(stat_bedwars_final_deaths,1)), rounding_precision)
    stat_skywars_kdr = round((stat_skywars_kills/max(stat_skywars_deaths,1)), rounding_precision)

    try:
        stat_sumo_duel_wins = data["player"]["stats"]["Duels"]["sumo_duel_wins"]
    except KeyError:
        stat_sumo_duel_wins = 0
    try:
        stat_sumo_duel_losses = data["player"]["stats"]["Duels"]["sumo_duel_losses"]
    except KeyError:
        stat_sumo_duel_losses = 0
        
    sumowlr = round((stat_sumo_duel_wins/max(stat_sumo_duel_losses, 1)), rounding_precision)

    try:
        stat_sumo_bws = data["player"]["stats"]["Duels"]["best_sumo_winstreak"]
    except KeyError:
        stat_sumo_bws = 0

    try:
        stat_uhc_duel_wins = data["player"]["stats"]["Duels"]["uhc_duel_wins"]
    except KeyError:
        stat_uhc_duel_wins = 0

    try:
        stat_uhc_duel_losses = data["player"]["stats"]["Duels"]["uhc_duel_losses"]
    except KeyError:
        stat_uhc_duel_losses = 0

    uhcwlr = round((stat_uhc_duel_wins/max(stat_uhc_duel_losses, 1)), rounding_precision)
    
    # REAL UHC
    try:
        stat_UHC_kills = data["player"]["stats"]["UHC"]["kills_solo"] + data["player"]["stats"]["UHC"]["kills"]
    except KeyError:
        stat_UHC_kills = 0

    try:
        stat_UHC_deaths = data["player"]["stats"]["UHC"]["deaths_solo"] + data["player"]["stats"]["UHC"]["deaths"]
    except KeyError:
        stat_UHC_deaths = 0

    uhckdr = round((stat_UHC_kills/max(stat_UHC_deaths, 1)), rounding_precision)

    # All Duels
    try:
        stat_duels_wins = data["player"]["stats"]["Duels"]["wins"]
    except KeyError:
        stat_duels_wins = 0

    try:
        stat_duels_losses = data["player"]["stats"]["Duels"]["losses"]
    except KeyError:
        stat_duels_losses = 0

    try:
        stat_duels_bws = data["player"]["stats"]["Duels"]["best_overall_winstreak"]
    except KeyError:
        stat_duels_bws = 0

    # Bedwars
    try:
        stat_bw_kills = data["player"]["stats"]["Bedwars"]["kills_bedwars"]
    except KeyError:
        stat_bw_kills = 0

    try:
        stat_bw_deaths = data["player"]["stats"]["Bedwars"]["deaths_bedwars"]
    except KeyError:
        stat_bw_deaths = 0
    
    # Melee
    try:
        stat_duels_melee_hits = data["player"]["stats"]["Duels"]["melee_hits"]
    except KeyError:
        stat_duels_melee_hits = 0

    try:
        stat_duels_melee_swings = data["player"]["stats"]["Duels"]["melee_swings"]
    except KeyError:
        stat_duels_melee_swings = 0

    try:
        stat_duels_combo_melee_hits = data["player"]["stats"]["Duels"]["combo_duel_melee_hits"]
    except KeyError:
        stat_duels_combo_melee_hits = 0

    try:
        stat_duels_combo_melee_swings = data["player"]["stats"]["Duels"]["combo_duel_melee_swings"]
    except KeyError:
        stat_duels_combo_melee_swings = 0

    try:
        hypixelxp = data["player"]["networkExp"]
    except KeyError:
        hypixelxp = 0

    nwl = round(((math.sqrt((2 * hypixelxp) + 30625) / 50) - 2.5), rounding_precision)
    

    nocombomeleehits = stat_duels_melee_hits-stat_duels_combo_melee_hits
    nocombomeleeswings = stat_duels_melee_swings-stat_duels_combo_melee_swings

    stat_melee_accuracy = round((nocombomeleehits/max(nocombomeleeswings,1)*100), rounding_precision)


    stat_bw_kdr = round(stat_bw_kills/max(stat_bw_deaths,1), rounding_precision)
    stat_bw_fksperstar = round(stat_bedwars_final_kills/max(stat_bedwars_star,1), rounding_precision)

    tDanger = f'{c.White}{c.bgRed}DANGER{c.bgDefault}'
    tRisky = f'{c.Yellow}Risky{c.White}'
    tSafe = f'{c.White}Safe'


    wlr = round((stat_duels_wins/max(stat_duels_losses, 1)), rounding_precision)

    swstar = stat_level_formatted[2:-1]+" ☆"
    intswstar = int(stat_level_formatted[2:-1])

    bwstar = str(stat_bedwars_star)+" ☆"

    stat_combo_melee_accuracy = round((stat_duels_combo_melee_hits/max(stat_duels_combo_melee_swings,1)*100), rounding_precision)


    if nwl < 100 or nwl > 15:
        print(f"{tSafe}    ||   NWL: {nwl}") 
    elif (nwl > 100 and nwl < 200) or 5 < nwl < 15:
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

    # time.sleep(0.005)
    
    if stat_skywars_kdr < 1:
        print(f"{tSafe}    ||   SW kdr: {stat_skywars_kdr}")
    elif stat_skywars_kdr > 1 and stat_skywars_kdr < 2:
        print(f"{tRisky}   ||   SW kdr: {c.Yellow}{stat_skywars_kdr}")
    elif stat_skywars_kdr > 2:
        print(f"{tDanger}  ||   SW kdr: {c.Red}{stat_skywars_kdr}")
    
    # time.sleep(0.005)
    
    if stat_bedwars_star < 200 and stat_bedwars_star != 0:
        print(f"{tSafe}    ||   BW star: {stat_bedwars_star} ☆")
    elif stat_bedwars_star > 200 and stat_bedwars_star < 350:
        print(f"{tRisky}   ||   BW star: {c.Yellow}{stat_bedwars_star} ☆")
    elif stat_bedwars_star > 350 or stat_bedwars_star == 0:
        print(f"{tDanger}  ||   BW star: {c.Red}{stat_bedwars_star} ☆")

    # time.sleep(0.005)
    
    if stat_fkdr < 2:
        print(f"{tSafe}    ||   FKDR: {stat_fkdr}")
    elif stat_fkdr > 2 and stat_fkdr < 3.5:
        print(f"{tRisky}   ||   FKDR: {c.Yellow}{stat_fkdr}")
    elif stat_fkdr > 3.5:
        print(f"{tDanger}  ||   FKDR: {c.Red}{stat_fkdr}")

    # time.sleep(0.005)
    
    if stat_bw_kdr < .8:
        print(f"{tSafe}    ||   BW kdr: {stat_bw_kdr}")
    elif stat_bw_kdr > .8 and stat_bw_kdr < 1.6:
        print(f"{tRisky}   ||   BW kdr: {c.Yellow}{stat_bw_kdr}")
    elif stat_bw_kdr > 1.6:
        print(f"{tDanger}  ||   BW kdr: {c.Red}{stat_bw_kdr}")

    # time.sleep(0.005)
    
    if stat_bw_fksperstar < 25:
        print(f"{tSafe}    ||   BW fks/star: {stat_bw_fksperstar}")
    elif stat_bw_fksperstar > 25 and stat_bw_fksperstar < 50:
        print(f"{tRisky}   ||   BW fks/star: {c.Yellow}{stat_bw_fksperstar}")
    elif stat_bw_fksperstar > 50:
        print(f"{tDanger}  ||   BW fks/star: {c.Red}{stat_bw_fksperstar}")

    # time.sleep(0.005)
    
    if sumowlr < 1.5:
        print(f"{tSafe}    ||   Sumo wlr: {sumowlr}")
    elif sumowlr > 1.5 and sumowlr < 2.25:
        print(f"{tRisky}   ||   Sumo wlr: {c.Yellow}{sumowlr}")
    elif sumowlr > 2.25:
        print(f"{tDanger}  ||   Sumo wlr: {c.Red}{sumowlr}")

    # time.sleep(0.005)
    
    if stat_sumo_bws < 10 and stat_sumo_bws != 0:
        print(f"{tSafe}    ||   Sumo bws: {stat_sumo_bws}")
    elif stat_sumo_bws > 10 and stat_sumo_bws < 25:
        print(f"{tRisky}   ||   Sumo bws: {c.Yellow}{stat_sumo_bws}")
    elif stat_sumo_bws > 25 or (stat_sumo_bws == 0 and stat_sumo_duel_wins > 0):
        print(f"{tDanger}  ||   Sumo bws: {c.Red}{stat_sumo_bws}")

    # time.sleep(0.005)
    
    if uhcwlr < 1:
        print(f"{tSafe}    ||   UHCD wlr: {uhcwlr}")
    elif uhcwlr > 1 and uhcwlr < 2.5:
        print(f"{tRisky}   ||   UHCD wlr: {c.Yellow}{uhcwlr}")
    elif uhcwlr > 2.5:
        print(f"{tDanger}  ||   UHCD wlr: {c.Red}{uhcwlr}")

    # time.sleep(0.005)
    
    if uhckdr < 0.5:
        print(f"{tSafe}    ||   UHC kdr: {uhckdr}")
    elif uhckdr > 0.5 and uhckdr < 1.5:
        print(f"{tRisky}   ||   UHC kdr: {c.Yellow}{uhckdr}")
    elif uhckdr > 1.5:
        print(f"{tDanger}  ||   UHC kdr: {c.Red}{uhckdr}")

    # time.sleep(0.005)
    
    if wlr < 1.5 or (wlr == 0 and stat_duels_losses > 0):
        print(f"{tSafe}    ||   Wlr: {wlr}")
    elif wlr > 1.5 and wlr < 2.5:
        print(f"{tRisky}   ||   Wlr: {c.Yellow}{wlr}")
    elif wlr > 2.5 or (wlr == 0 and stat_duels_losses == 0):
        print(f"{tDanger}  ||   Wlr: {c.Red}{wlr}")

    # time.sleep(0.005)
    
    if stat_duels_wins > 10 and stat_duels_wins < 10000:
        print(f"{tSafe}    ||   Wins: {stat_duels_wins}")
    elif (stat_duels_wins > 3 and stat_duels_wins < 10) or (stat_duels_wins > 10000 and stat_duels_wins < 20000):
        print(f"{tRisky}   ||   Wins: {c.Yellow}{stat_duels_wins}")
    elif (stat_duels_wins < 3 and (stat_duels_losses < 4 * stat_duels_wins)) or (stat_duels_wins > 20000):
        print(f"{tDanger}  ||   Wins: {c.Red}{stat_duels_wins}")
    else:
        print(f"{tSafe}    ||   Wins: {stat_duels_wins}")

    # time.sleep(0.005)

    if stat_duels_losses > 10:
        print(f"{tSafe}    ||   Losses: {stat_duels_losses}")
    elif stat_duels_losses > 3 and stat_duels_losses < 10:
        print(f"{tRisky}   ||   Losses: {c.Yellow}{stat_duels_losses}")
    elif stat_duels_losses < 3:
        print(f"{tDanger}  ||   Losses: {c.Red}{stat_duels_losses}")
    else:
        print(f"{tSafe}    ||   Losses: {stat_duels_losses}")

    # time.sleep(0.01)
    
    if stat_duels_bws < 25 and stat_duels_bws != 0:
        print(f"{tSafe}    ||   Bws: {stat_duels_bws}")
    elif stat_duels_bws > 25 and stat_duels_bws < 50:
        print(f"{tRisky}   ||   Bws: {c.Yellow}{stat_duels_bws}")
    elif stat_duels_bws > 50 or stat_duels_bws == 0:
        print(f"{tDanger}  ||   Bws: {c.Red}{stat_duels_bws}")

    # time.sleep(0.01)
    
    if stat_melee_accuracy < 50 and stat_melee_accuracy != 0:
        print(f"{tSafe}    ||   mAccuracy: {stat_melee_accuracy} %")
    elif stat_melee_accuracy > 50 and stat_melee_accuracy < 70:
        print(f"{tRisky}   ||   mAccuracy: {c.Yellow}{stat_melee_accuracy} %")
    elif stat_melee_accuracy > 70 or stat_melee_accuracy == 0:
        print(f"{tDanger}  ||   mAccuracy: {c.Red}{stat_melee_accuracy} %")

    # time.sleep(0.01)
    
    if stat_combo_melee_accuracy < 75:
        print(f"{tSafe}    ||   Combo mAcc: {stat_combo_melee_accuracy} %")
    elif stat_combo_melee_accuracy > 75 and stat_combo_melee_accuracy < 100:
        print(f"{tRisky}   ||   Combo mAcc: {c.Yellow}{stat_combo_melee_accuracy} %")
    elif stat_combo_melee_accuracy > 100:
        print(f"{tDanger}  ||   Combo mAcc: {c.Red}{stat_combo_melee_accuracy} %")
    else:
        print(f"{tSafe}    ||   Combo mAcc: {stat_combo_melee_accuracy} %")




    blacklist = open(blacklist, "r")
    read = blacklist.readlines()
    modified = []

    for line in read:
            modified.append(line.strip())

    for line in modified:
        if line == uuid or line == name:
            print(f"{c.bgDefault}{c.White}---------")
            print(f"{c.bgBlue}{c.White}BLACKLISTED!{c.bgDefault}")
    blacklist.close()  



    safelist = open(safelist, "r")
    read = safelist.readlines()
    modified = []

    for line in read:
            modified.append(line.strip())

    for line in modified:
        if line == uuid or line == name:
            print(f"{c.bgDefault}{c.White}---------")
            print(f"{c.bgGreen}{c.White}SAFELISTED!{c.bgDefault}")
    safelist.close()  






    weirdlist = open(weirdlist, "r")
    read = weirdlist.readlines()
    modified = []

    for line in read:
            modified.append(line.strip())

    for line in modified:
        if line == uuid or line == name:
            print(f"{c.bgDefault}{c.White}---------")
            print(f"{c.bgYellow}{c.White}Weird Stats{c.bgDefault}")
    weirdlist.close() 



    print(f"{c.bgDefault}{c.White}---------")
    print(f"{c.bgDefault}{c.DarkGray}UUID:", uuid)
    print(f"{c.bgDefault}{c.White}---------")


# follow(thefile) follows the latest.log file and reads for new chat messages
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.04)
            continue
        yield line


# do the thing prints "checking <ign>" and then runs the antisniper function
def dothething():
    print("Checking:", name)   
    antisniper()


# tox: i fixed lunar and cheatbreaker not working
# i also deleted if __name__ == __main__
# you have to relaunch samael if you switch clients

while True:
    if process_exists('Lunar Client.exe'):
        logfile = open(home+"/.lunarclient/offline/multiver/logs/latest.log", "r")
    elif process_exists('Badlion Client.exe'):
        logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/blclient/minecraft/latest.log", "r")
    elif process_exists('CheatBreaker.exe'):
        logfile = open(os.getenv("APPDATA")+"/CheatBreaker/logs/1.8.9/latest.log", "r")
    else:
        logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r")

    try:
                            # [OBSOLETE] if you dont want to have the launcher open you can manually set the path of the exe
                            # tox: you only have to have the launcher open when you launch samael i think




        # the below code parses the ign from the raw chat message in the latest.log file
        loglines = follow(logfile)
        for line in loglines:
            if "[Client thread/INFO]: [CHAT] ? [MVP++]" in line:
                start = line.index('[MVP++]')
                end = line.index('Lvl:',start+1)
                name = line[start+8:end-1]
                dothething()






            elif "[Client thread/INFO]: [CHAT] ? [MVP+]" in line:
                start = line.index('[MVP+]')
                end = line.index('Lvl:',start+1)

                name = line[start+7:end-1]
                dothething()




            elif "[Client thread/INFO]: [CHAT] ? §0[UHC]" in line:
                start = line.index('[UHC]')
                end = line.index('Lvl:',start+1)

                name = line[start+6:end-1]
                dothething()





            elif "[Client thread/INFO]: [CHAT] ? [MVP]" in line:
                start = line.index('[MVP]')
                end = line.index('Lvl:',start+1)

                name = line[start+6:end-1]
                dothething()






            elif "[Client thread/INFO]: [CHAT] ? [VIP+]" in line:
                start = line.index('[VIP+]')
                end = line.index('Lvl:',start+1)

                name = line[start+7:end-1]
                dothething()







            elif "[Client thread/INFO]: [CHAT] ? [VIP]" in line:
                start = line.index('[VIP]')
                end = line.index('Lvl:',start+1)

                name = line[start+6:end-1]
                dothething()
            

        

            elif "[Client thread/INFO]: [CHAT] ? " in line and "[Client thread/INFO]: [CHAT] ? W/L:" not in line:
                start = line.index('? ')
                end = line.index('Lvl:',start+1)

                name = line[start+2:end-1]
                dothething()


            


            # commands to add players to list
            # the format for this is "/fakechat -<b, s, or w> <ign>"
            # example: /fakechat -b toxikuu
            elif "[Client thread/INFO]: [CHAT] -b" in line:
                start = line.index('-b')
                end = line.index('\n', start+1)

                substring = line[start+3:end]
            
                print("> Fetching uuid for", substring)
                

                try:
                    resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{substring}")
                    uuid = resp.json()["id"]
                    print("> Blacklisting", uuid)


                    with open(f"{blacklist}", "a") as testbl:
                        testbl.write(f"\n{uuid}")

                    print(f"> Added {substring} to blacklist\n")

                except KeyError:
                    print("Error: invalid ign")    


            elif "[Client thread/INFO]: [CHAT] -s" in line:
                start = line.index('-s')
                end = line.index('\n', start+1)

                substring = line[start+3:end]
            
                print("> Fetching uuid for", substring)
                

                try:
                    resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{substring}")
                    uuid = resp.json()["id"]
                    print("> Safelisting", uuid)


                    with open(f"{safelist}", "a") as testsl:
                        testsl.write(f"\n{uuid}")

                    print(f"> Added {substring} to safelist\n")

                except KeyError:
                    print("Error: invalid ign")


            elif "[Client thread/INFO]: [CHAT] -w" in line:
                start = line.index('-w')
                end = line.index('\n', start+1)

                substring = line[start+3:end]
            
                print("> Fetching uuid for", substring)
                

                try:
                    resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{substring}")
                    uuid = resp.json()["id"]
                    print("> Weirdlisting", uuid)


                    with open(f"{weirdlist}", "a") as testwl:
                        testwl.write(f"\n{uuid}")

                    print(f"> Added {substring} to weirdlist\n")

                except KeyError:
                    print("Error: invalid ign")



            # this code checks for nicks

            if "[Client thread/INFO]: [CHAT] Lilith > Found 1 likely nicked players: Possibly \n" in line:
                pass
            elif f"[Client thread/INFO]: [CHAT] Lilith > Found 1 likely nicked players: Possibly Toxikuu" in line:
                pass
            elif f"[Client thread/INFO]: [CHAT] Lilith > Found {1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10 or 11 or 12 or 13 or 14 or 15 or 16} likely nicked players: Possibly " in line:
                print(f"{c.bgDefault}{c.LightMagenta}---------")
                print(f"{c.bgMagenta}{c.White}NICK OMG WTF DODGE NICK DODGE!!{c.bgDefault}")
                print(f"{c.bgDefault}{c.LightMagenta}---------\n{c.White}")

    except:
        continue
