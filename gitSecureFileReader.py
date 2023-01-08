import re


secret_key_regex = "(?:[0–9a-z\-_\t .]{0,20})(?:[\s|']|[\s|\"]){0,3}(?:=|>|:=|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9_-]{32})(?:['|\"|\n|\r|\s|\x60]|$)"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class GitSecureFileReader:
    def __init__(self, file_dir):
        self.dir = file_dir
    
    def file_opener(self):
        try:
            file1 = open(self.dir, 'r')
            return file1
        except Exception as e:
            print(f"Error opening file {e}")
            return None

    def file_reader(self):
        return self.file_opener().readlines()

    def detect_secret_keys(self):
        lines = self.file_reader()
        count = 0
        has_key = False

        for line in lines:
            count += 1
            z = re.match(secret_key_regex, line)

            if z:
                has_key = True
                print(bcolors.WARNING +"Warning: File directory "+ f"{self.dir}" +bcolors.ENDC)
                print(bcolors.WARNING  + f"Warning: Line {count} has a secret key " + bcolors.BOLD + 
                        bcolors.FAIL + f'{z.groups()[0]}', bcolors.ENDC + bcolors.WARNING +
                        "please have a look." + bcolors.ENDC)
        
        if has_key is False:
            print(bcolors.OKGREEN+f"YAY!!!!!! No secret key found in {self.dir.split('/')[-1]}"+bcolors.ENDC)
