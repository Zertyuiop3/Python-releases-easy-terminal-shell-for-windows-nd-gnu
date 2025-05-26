import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('SETUP_LOG_FILE.log')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.debug('SETUP-PLAN') 
logger.debug('SETUP PROCESS START')
logger.debug('IMPORTING MODULES')  
logger.debug('++ ROOT-USER') 
logger.debug('++ SETIINGS.CFG') 
logger.debug('PYTHON-RESTART') 
  # Only in file
logger.info('This is an info message')   # In both file and console
import json
import os
import time
import cmd
import getpass
import configparser
import hashlib
import logging
os.system('cls' if os.name == 'nt' else 'clear')

def root_user_exists():
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
        return "root" in users
    except (FileNotFoundError, json.JSONDecodeError):
        return False

class CustomShell(cmd.Cmd):
    prompt = "root@azertyuiop [~] "
    intro = "Welcome to the taha's shell. Type 'help' or '?' to list commands."

    def __init__(self):
        super().__init__()
        self.logged_in = True
        self.username = "root"
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler('log_file.log')
        self.file_handler.setLevel(logging.DEBUG)
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        self.console_handler.setFormatter(formatter)

    def do_settings(self, arg):
        if os.name == 'nt':
            print("Starting your windows settings")
            os.system("start ms-settings")
        else:
            print("Starting Linux desktop settings")
            os.system("xfce4-settings")

    def do_whoami(self, arg):
        if self.logged_in:
            print(self.username)
        else:
            print("You are not logged in.")

    def do_startlog(self, arg):
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        self.logger.debug('This is a debug message')  # Only in file
        self.logger.info('This is an info message')  # In both file and console

    def do_exit(self, arg):
        print("Exiting shell...")
        os.system('cls' if os.name == 'nt' else 'clear')
        return True

    def do_clear(self, arg):
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    if not root_user_exists():
        print("=========================SETUP============================")
        print("Welcome to tahabelfkira's shell (azertyuiop)")
        print("Importing required configuration...")
        modules = [
            ('time', "imported time 1/6"),
            ('hashlib', "imported hashlib for users 2/6"),
            ('cmd', "imported cmd for prompt 3/6"),
            ('json', "imported json for user save 4/6"),
            ('getpass', "imported getpass for password 5/6"),
            ('configparser', "imported configparser for settings save 6/6")
        ]
        for module_name, message in modules:
            try:
                __import__(module_name)
            except ImportError:
                print(f"Error importing {module_name}")
            time.sleep(1)
            print(message)
        print("Successfully imported configurations")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=========================SETUP============================")
        config = configparser.ConfigParser()
        if os.path.exists('settings.cfg'):
            config.read('settings.cfg')
            print("Settings file exists.")
        else:
            print("Settings file does not exist. Creating a new one...")
            config.add_section('os controlling')
            config.set('os controlling', 'control the whole of your os', 'enable')
            config.add_section('subprocess controlling')
            config.set('subprocess controlling', 'control the whole of your os by subprocess.run ', 'disable')
            config.add_section('WSL (Windows subsystem for linux(WINDOWS ONLY))')
            config.set('WSL (Windows subsystem for linux(WINDOWS ONLY))', 'Use it with python', 'enable')
            config.add_section('WSL version')
            config.set('WSL version', 'choose the working version', '2')
            with open('settings.cfg', 'w') as f:
                config.write(f)
            print("Settings file created.")
        if os.path.exists('users.json'):
            print("Using existing users file")
            time.sleep(1)
        else:
            print("Creating users file")
            with open('users.json', 'w') as f:
                json.dump({}, f)
            time.sleep(1)
        if root_user_exists():
            print("Using cached root user")
            time.sleep(1)
        else:
            print("Creating root user")
            time.sleep(1)
            try:
 
                with open('users.json', 'r') as f:
                    users = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                users = {}
            users["root"] = None
            with open('users.json', 'w') as f:
                json.dump(users, f)
            print("Root user added.")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Now restart your python file")
    else:
        print("Starting azertyuiop shell ")
        shell = CustomShell()
        shell.cmdloop()