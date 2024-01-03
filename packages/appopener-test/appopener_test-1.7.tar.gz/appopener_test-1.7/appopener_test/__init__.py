__version__ = "1.8"
from . import check, update_list, commands, features
from difflib import SequenceMatcher
import os, re

check.check_os()
# Checking if required files exists or not
if os.name == "nt":
    check.check_json()
    check.app_names()

    # Get the path of working directory
    main_path = os.path.join((check.get_path()), "Data")

    # REDIRECTED FUNCTION FOR SIMPLIFICATION
    def give_appnames(upper=False):
        '''
        #### `give_appname` is a callable function which gives Appnames as Dictionary in upper or lower case.
        Examples:
        1: app_names = give_appnames(upper=True)
        2: app_names = give_appnames(upper=False)
        #### `upper=True` gives appnames in upper case.
        #### `upper=False` gives appnames in lower case.
        '''
        if upper:
            upper = True
        keys = features.give_appnames(upper=upper)
        return keys

    # For making list
    def mklist(name="", path="", output=True):
        '''
        #### `mklist` is the function which gives Appnames along with their Appids in the specified output file.
        Examples:
        1: mklist(name="json_format.json", path="path_to_folder", output=True)
        2: mklist(name="txt_format.txt", path="path_to_folder", output=True)
        #### `path=` is the path where the file must be stored (to save in working dir dont include it)
        #### `output=True` prints the context of funtion.
        '''
        name = name
        path = path
        output = output
        features.mklist(name=name, path=path, output=output)

    # Run application (Regex implemented)
    def run(self, output=True):
        print()
        print("'RUN' FUNCTION IS REPLACED BY 'OPEN' FUNCTION")
        print("TRY USING 'OPEN(app_name)'")
        print()

    # Open application (Regex implemented)
    def open(self, output=True, match_closest=False, throw_error=False):
        '''
        #### `open` is the function which is used to open applications.
        Examples:
        1: open("whatsapp")
        2: open("whatsapp, telegram")
        3: open("calcu", match_closest=True)
        4: open("whatsapp, telegram", output=False)
        #### `match_closest=True` matches the closest match in given appname.
        #### `output=False` don't print the context of function.
        '''
        if not output:
            output = False
        if match_closest:
            match_closest = True
        inp = (self).lower()
        val=(re.compile(r'[^a-zA-Z-^0-9?,>&]').sub(" ",inp)).strip()
        if val == (""):
            pass
        elif val == ("cls"):
            os.system("cls")
        elif val == ("version"):
            print("AppOpener version "+__version__)
        elif inp == ("?"):
            invsys = '"'
            os.system(f"explorer {invsys}https://appopener.readthedocs.io/en/latest/{invsys}")
        elif val == ("help"):
            print()
            commands.commands()
            print()
        elif val == ("ls"):
            features.list_apps()
        elif val == ("rename -m"):
            os.startfile(os.path.join(main_path,"app_names.json"))
            print("RELOAD PROGRAM TO APPEND CHANGES")
        elif val == ("update"):
            update_list.update(output=output)
        elif " > " in val:
            update_list.do_changes_cli(val)
            update_list.check_new_name()
            update_list.pre_change()
            update_list.modify()
        elif val == ("default"):
            update_list.default(output=output)
            update_list.check_new_name()
            update_list.pre_change()
            update_list.modify()
        elif val == "mklist":
            mklist(output=output)
        elif "find " in val:
            print()
            val2 = val.replace("find ","")
            empty_list = []
            if "," in val2:
                splited = val2.split(",")
                empty_list.extend(splited)
            else:
                empty_list.append(val2)
            features.find_apps(app_names=empty_list)
            print()
        elif val == "log -c" or val == "log":
            print()
            val2 = val.replace("log -","")
            features.change_log(val)
            print()
        else:
            if "," in val:
                splited = val.split(",")
                for i in splited:
                    j = i.strip()
                    if j != "":
                        features.open_things(j, output=output, match_closest=match_closest, throw_error=throw_error)
            else:
                features.open_things(val, output=output, match_closest=match_closest, throw_error=throw_error)

    # Close any application by just its name :)
    def close(self, output=True, match_closest=False, throw_error=False):
        '''
        #### `close` is the function which is used to close applications.
        Examples:
        1: close("whatsapp")
        2: close("whatsapp, telegram")
        3: close("calcu", match_closest=True)
        4: close("whatsapp, telegram", output=False)
        #### `match_closest=True` matches the closest match in given appname.
        #### `output=False` don't print the context of function.
        '''
        if not output:
            output = False
        if match_closest:
            match_closest = True
        inp = (self).lower()
        val=(re.compile(r'[^a-zA-Z-^0-9?,>&+.]').sub(" ",inp)).strip()
        if "," in val:
            splited = val.split(",")
            for i in splited:
                j = i.strip()
                if j != "":
                    features.close_things(j, output=output, match_closest=match_closest, throw_error=throw_error)
        else:
            features.close_things(val, output=output, match_closest=match_closest, throw_error=throw_error)

else:
    def open(self):

        app = self.lower()
        
        native_list = ['app store', 'mail', 'contacts', 'calender', 'reminders', 'notes', 'face time', 'messages',
                    'maps', 'find my', 'photos', 'photo booth', 'preview', 'music', 'tv', 'podcasts', 'voice memos', 'garageband']
        # highest_similarity = 0.0
        # most_similar_string = None
        # for string in native_list:
        #     similarity_ratio = SequenceMatcher(None, app, string).ratio()
        #     if similarity_ratio > highest_similarity:
        #         highest_similarity = similarity_ratio
        #         most_similar_string = string
        #     print(most_similar_string)
        if app in native_list:
            subprocess.run(["open", "-a", app])

        else:

            item_list = []
            for item in os.listdir("/Applications/"):
                item_path = os.path.join("/Applications/", item)
                item_list.append(item_path)
                print(item_path)

            highest_similarity = 0.0
            most_similar_string = None

            for string in item_list:
                similarity_ratio = SequenceMatcher(None, app, string).ratio()
                if similarity_ratio > highest_similarity:
                    highest_similarity = similarity_ratio
                    most_similar_string = string
            formatted_file_path = f'"{most_similar_string}"'
            os.system(f'open {formatted_file_path}')


    def close(self):

        app = self.lower()

        native_list = ['app store', 'mail', 'contacts', 'calender', 'reminders', 'notes', 'face time', 'messages',
                    'maps', 'find my', 'photos', 'photo booth', 'preview', 'music', 'tv', 'podcasts', 'voice memos', 'garageband']
        # highest_similarity = 0.0
        # most_similar_string = None
        # for string in native_list:
        #     similarity_ratio = SequenceMatcher(None, app, string).ratio()
        #     if similarity_ratio > highest_similarity:
        #         highest_similarity = similarity_ratio
        #         most_similar_string = string
        #     print(most_similar_string)
        if app in native_list:
            subprocess.run(
                ["osascript", "-e", f'tell application "{app}" to quit'])

        else:

            item_list = []
            for item in os.listdir("/Applications/"):
                item_path = os.path.join("/Applications/", item)
                item_list.append(item_path)
                print(item_path)

            highest_similarity = 0.0
            most_similar_string = None

            for string in item_list:
                similarity_ratio = SequenceMatcher(None, app, string).ratio()
                if similarity_ratio > highest_similarity:
                    highest_similarity = similarity_ratio
                    most_similar_string = string
            os.system(
                f'osascript -e \'tell application "{most_similar_string}" to quit\'')

