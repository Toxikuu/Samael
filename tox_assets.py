# Functions to be used as assets in scripts
import os, sys, requests, time

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def getInfo(call):
    r = requests.get(call)
    return r.json()

def igntouuid(ign):
    try:
        pdb = getInfo(f"https://playerdb.co/api/player/minecraft/{ign}")
        uuid = pdb["data"]["player"]["raw_id"]
    except:
        print(f"Failed to access uuid for {ign}")
    return uuid

def uuidtoign(uuid):
    try:
        pdb = getInfo(f"https://playerdb.co/api/player/minecraft/{uuid}")
        ignfromuuid = pdb["data"]["player"]["username"]
    except:
        print(f"Failed to access ign for {uuid}")
    return ignfromuuid

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def get_line_count(file):
    with open(file) as f:
        linecount = len(f.readlines())
    return linecount

def clear_file(file):
    with open(file, 'w') as f:
        f.write('')

def create_files_if_nonexistent(*files, v=False):
    for file in files:
        try:
            with open(file, 'r'): pass
        except FileNotFoundError:
            with open(file, 'x'): pass
            if v: print(f'Creating files: {file}')

def get_hypixel_stats(apikey, uuid):
    if uuid != None:
        url = f"https://api.hypixel.net/player?key={apikey}&uuid={uuid}"
        data = getInfo(url)
        return data

def read_ids_from_file(filename):
    ids = set()
    with open(filename, 'r') as file:
        for line in file:
            ids.add(line.strip())
    return ids

def remove_blacklisted_ids(safelist, blacklist, weirdlist):
    safelist_ids = read_ids_from_file(safelist)
    blacklist_ids = read_ids_from_file(blacklist)
    weirdlist_ids = read_ids_from_file(weirdlist)
    blacklist_ids.update(weirdlist_ids)
    
    removed_ids = safelist_ids.intersection(blacklist_ids)
    
    num_removed = 0
    if removed_ids:
        for id_ in removed_ids:
            num_removed += 1
        safelist_ids -= removed_ids
    
        with open(safelist, 'w') as file:
            for id_ in safelist_ids:
                file.write(id_ + '\n')
        print(f'> Removed {num_removed} blacklisted/weirdlisted UUIDs from safelist.')

    else:
        print("> No UUIDs to remove from the safelist.")

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

def count_specific_strings_in_file(file_path, target_string):
    with open(file_path, 'r') as file:
        content = file.read()
        # Split the content into words based on whitespace
        words = content.split()
        # Count the number of occurrences of the target string
        num_occurrences = words.count(target_string)
        return num_occurrences

def Samael_text(color):
    print("\n")
    print(f"{color}███████╗ █████╗ ███╗   ███╗ █████╗ ███████╗██╗     ")
    print(f"{color}██╔════╝██╔══██╗████╗ ████║██╔══██╗██╔════╝██║     ")
    print(f"{color}███████╗███████║██╔████╔██║███████║█████╗  ██║     ")
    print(f"{color}╚════██║██╔══██║██║╚██╔╝██║██╔══██║██╔══╝  ██║     ")
    print(f"{color}███████║██║  ██║██║ ╚═╝ ██║██║  ██║███████╗███████╗")
    print(f"{color}╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝")