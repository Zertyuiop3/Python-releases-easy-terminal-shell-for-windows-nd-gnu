import json
import os
import time
import cmd
import getpass
import configparser
import hashlib
import logging # Ensure logging is imported at the top

# Clear screen at the start
os.system('cls' if os.name == 'nt' else 'clear')

def root_user_exists():
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
        return "root" in users
    except (FileNotFoundError, json.JSONDecodeError):
        return False

class CustomShell(cmd.Cmd):
    prompt = "root@azertyuiop [~]:~#  "
    intro = "Welcome to the taha's shell. Type 'help' or '?' to list commands."

    def __init__(self):
        super().__init__()
        self.logged_in = True  # Assuming auto-login as root for now
        self.username = "root"
        
        # Logger for shell operations
        self.logger = logging.getLogger(__name__) # Uses the module's logger
        self.logger.setLevel(logging.DEBUG)
        
        # Prepare handlers but add them in do_startlog
        self.file_handler = logging.FileHandler('log_file.log')
        self.file_handler.setLevel(logging.DEBUG)
        
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        self.console_handler.setFormatter(formatter)

    def do_settings(self, arg):
        """Opens the system settings application."""
        if os.name == 'nt':
            print("Starting your windows settings...")
            os.system("start ms-settings")
        else:
            print("Starting Linux desktop settings (requires xfce4-settings)...")
            # Note: xfce4-settings might not be available on all Linux systems.
            # Consider using a more universal command or making it configurable.
            os.system("xfce4-settings-manager") # Common command, or just xfce4-settings

    def do_whoami(self, arg):
        """Prints the current logged-in username."""
        if self.logged_in:
            print(self.username)
        else:
            print("You are not logged in.")

    def do_startlog(self, arg):
        """Starts logging shell activities to file and console."""
        # Avoid adding handlers multiple times if command is re-issued
        if self.file_handler not in self.logger.handlers:
            self.logger.addHandler(self.file_handler)
        if self.console_handler not in self.logger.handlers:
            self.logger.addHandler(self.console_handler)
        
        self.logger.debug('Shell log: This is a debug message (to file)')
        self.logger.info('Shell log: This is an info message (to file and console)')
        print("Logging started. Check log_file.log and console for messages.")

    def do_exit(self, arg):
        """Exits the shell."""
        print("Exiting shell...")
        os.system('cls' if os.name == 'nt' else 'clear')
        return True

    def do_clear(self, arg):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    if not root_user_exists():
        # This block runs for one-time setup if root user doesn't exist.

        # Configure logger for the setup process
        # This uses the same logger name as CustomShell, which is fine because
        # the script restarts, effectively resetting logger handlers.
        setup_logger = logging.getLogger(__name__)
        setup_logger.setLevel(logging.DEBUG)

        # File handler for setup logs
        setup_file_handler = logging.FileHandler('SETUP_LOG_FILE.log')
        setup_file_handler.setLevel(logging.DEBUG)

        # Console handler for setup logs
        setup_console_handler = logging.StreamHandler()
        setup_console_handler.setLevel(logging.INFO) # Only INFO and above to console

        setup_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        setup_file_handler.setFormatter(setup_formatter)
        setup_console_handler.setFormatter(setup_formatter)

        setup_logger.addHandler(setup_file_handler)
        setup_logger.addHandler(setup_console_handler)

        setup_logger.info("Setup process started because root user does not exist.")
        setup_logger.debug('SETUP-PLAN')
        setup_logger.debug('SETUP PROCESS START')
        setup_logger.debug('IMPORTING MODULES (Verification)')
        setup_logger.debug('++ ROOT-USER CREATION')
        setup_logger.debug('++ SETTINGS.CFG CREATION') # Corrected typo
        setup_logger.debug('PYTHON-RESTART WILL BE REQUIRED POST-SETUP')

        print("=========================SETUP============================")
        print("Welcome to tahabelfkira's shell (azertyuiop) - First Time Setup")
        print("Importing required configuration (verification step)...")
        
        # Modules are already imported at the top level.
        # This loop serves as a verbose check during setup.
        modules_to_check = [
            ('time', "Verified time module 1/6"),
            ('hashlib', "Verified hashlib for users 2/6"),
            ('cmd', "Verified cmd for prompt 3/6"),
            ('json', "Verified json for user save 4/6"),
            ('getpass', "Verified getpass for password 5/6"),
            ('configparser', "Verified configparser for settings save 6/6")
        ]
        all_modules_ok = True
        for module_name, message in modules_to_check:
            try:
                __import__(module_name) # Verifies it's available
                print(message)
                setup_logger.debug(f"Module '{module_name}' verified.")
            except ImportError:
                error_msg = f"Error: Required module '{module_name}' could not be imported."
                print(error_msg)
                setup_logger.error(error_msg)
                all_modules_ok = False
            time.sleep(0.2) # Shorter sleep

        if not all_modules_ok:
            print("Critical modules missing. Setup cannot continue. Please install missing modules.")
            setup_logger.critical("Critical modules missing. Setup aborted.")
            exit() # Or handle more gracefully

        print("Successfully verified configurations.")
        setup_logger.info("Required modules verified successfully.")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

        print("=========================SETUP: CONFIGURATION FILES============================")
        config = configparser.ConfigParser()
        if os.path.exists('settings.cfg'):
            # config.read('settings.cfg') # Reading is not strictly necessary if we overwrite/ensure values
            print("Settings file 'settings.cfg' already exists. Ensuring default sections...")
            setup_logger.info("'settings.cfg' exists. Will ensure default sections.")
        else:
            print("Settings file 'settings.cfg' does not exist. Creating a new one...")
            setup_logger.info("'settings.cfg' does not exist. Creating new one.")
        
        # Ensure default sections and values
        # Using a dictionary for easier management of defaults
        default_settings = {
            'os controlling': {'control the whole of your os': 'enable'},
            'subprocess controlling': {'control the whole of your os by subprocess.run ': 'disable'},
            'WSL (Windows subsystem for linux(WINDOWS ONLY))': {'Use it with python': 'enable'},
            'WSL version': {'choose the working version': '2'}
        }
        for section, options in default_settings.items():
            if not config.has_section(section):
                config.add_section(section)
            for key, value in options.items():
                if not config.has_option(section, key): # Add only if option doesn't exist
                    config.set(section, key, value)

        with open('settings.cfg', 'w') as f_config: # Use f_config to avoid conflict
            config.write(f_config)
        print("Settings file 'settings.cfg' configured.")
        setup_logger.info("'settings.cfg' configured/created.")

        # User file setup
        if not os.path.exists('users.json'):
            print("Creating users file 'users.json'...")
            setup_logger.info("Creating 'users.json'.")
            with open('users.json', 'w') as f_users: # Use f_users
                json.dump({}, f_users) # Create an empty JSON object
            print("Users file created.")
            setup_logger.info("'users.json' created.")
            time.sleep(0.5)
        else:
            print("Users file 'users.json' already exists.")
            setup_logger.info("'users.json' already exists.")


        # Root user creation logic (simplified as we are in setup block)
        print("Checking/Creating root user...")
        setup_logger.info("Checking/Creating root user.")
        time.sleep(0.5)
        try:
            with open('users.json', 'r+') as f_users: # Open for reading and writing
                try:
                    users = json.load(f_users)
                except json.JSONDecodeError:
                    users = {} # If file is empty or corrupt, start fresh
                    setup_logger.warning("'users.json' was empty or malformed. Initializing as empty.")
                
                if "root" not in users:
                    users["root"] = None  # No password for root by default in this setup
                    f_users.seek(0)  # Go to the beginning of the file
                    json.dump(users, f_users, indent=4) # Write back with indent
                    f_users.truncate() # Remove any trailing old data if new data is shorter
                    print("Root user created in 'users.json'.")
                    setup_logger.info("Root user created in 'users.json'.")
                else:
                    print("Root user already exists in 'users.json'.")
                    setup_logger.info("Root user already exists.")
        except FileNotFoundError: # Should have been created above, but as a fallback
            setup_logger.error("'users.json' not found during root user creation. This is unexpected.")
            print("Error: 'users.json' not found. Cannot create root user.")


        os.system('cls' if os.name == 'nt' else 'clear')
        print("=========================SETUP COMPLETE============================")
        print("Initial setup is complete.")
        print("Please restart the python file to use the shell.")
        setup_logger.info("Setup complete. User needs to restart the script.")
    else:
        print("Starting azertyuiop shell...")
        # Any non-setup specific logging for app start can go here if needed,
        # using a new logger instance or the same __name__ logger.
        # For now, CustomShell handles its own logging via do_startlog.
        shell = CustomShell()
        shell.cmdloop()