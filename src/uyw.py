import os
import json

class UploadYourWorld:
    """
    the main class of the application
    """
    def __init__(self, root_folder=".UploadYourWorld"):
        os.makedirs(root_folder, exist_ok=True)
        self.root_folder = root_folder
        self.fs_json = 'fs.json'
        self.file_system = self.load_file_system()
        self.cur_location = '/'

    def list_dir(self, dir_path: str=None):
        """
        list all files and dirs in a path
        Args:
            dir_path: the path to the dir
        """
        if dir_path:
            cur_node = self.get_path_node(dir_path)
        else:
            cur_node = self.get_path_node(self.cur_location)

        if cur_node.get('type') == 'dir':
            # this is a dir, list it
            sub_items = cur_node.get('sub')
            for key in sub_items:
                print(key)

    def change_directory(self, target_path: str=None):
        """
        cd to another dir, currently only support relative path
        """
        self.cur_location = os.path.join(self.cur_location, target_path)
        self.cur_location = os.path.abspath(self.cur_location)

    def is_dir(self, node):
        return node.get('type') == 'dir'

    def get_path_node(self, path: str):
        """
        get the node(dict) of a path
        """
        dir_list = self.path_to_list(path)
        cur_dict = self.file_system
        #print(dir_list, cur_dict, self.cur_location)
        for d in dir_list:
            if self.is_dir(cur_dict):
                if d == "":
                    # current dir
                    continue
                else:
                    cur_dict = cur_dict.get('sub').get(d)
            else:
                raise ValueError("Path not valiad")
        #    print(cur_dict)
        return cur_dict

    def path_to_list(self, path: str):
        """
        convert a path string to a list of keys
        """
        return path.split('/')[1:]

    def add_file(self, file_path: str):
        """
        add file from the outside fs to uyw fs
        Args:
            file_path: the path to the outside fs file
        """
        file_name = os.path.basename(file_path)
        uyw_file_path = os.path.join(self.cur_location, file_name)

    def save_file_system(self, file_path=None):
        """
        save the file system to the json file
        Args:
            file_path: the path to the target json file
        Return:
            boolean: success?
        """
        if not file_path:
            file_path = os.path.join(self.root_folder, self.fs_json)
        try:
            with open(file_path, 'w') as fp:
                json.dump(self.file_system, fp)
        except Exception as exc:
            return False

        return True

    def load_file_system(self, file_path=None) -> dict:
        """
        load a json based file system
        Args:
            file_path: the path to the json file
        Return:
            dict: the loaded file system 
        """
        if not file_path:
            file_path = os.path.join(self.root_folder, self.fs_json)

        if not os.path.exists(file_path):
            # json file does not exist
            return {}
        else:
            with open(file_path, 'r') as fp:
                fs = json.load(fp)

        return fs

