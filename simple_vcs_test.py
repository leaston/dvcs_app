import os
import hashlib
import argparse
import json
import stat
import time

class SimpleVCS:
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.objects_dir = os.path.join(repo_dir, 'objects')
        self.log_file = os.path.join(repo_dir, 'log.json')
        os.makedirs(self.objects_dir, exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def hash_object(self, data):
        sha1 = hashlib.sha1()
        sha1.update(data)
        return sha1.hexdigest()

    def write_object(self, data):
        obj_hash = self.hash_object(data)
        obj_path = os.path.join(self.objects_dir, obj_hash)
        with open(obj_path, 'wb') as f:
            f.write(data)
        return obj_hash

    def commit(self, message):
        commit_data = message.encode('utf-8')
        commit_hash = self.write_object(commit_data)
        self.log_commit(commit_hash, message)
        print(f'Committed with hash {commit_hash}')

    def log_commit(self, commit_hash, message):
        timestamp = time.time()
        with open(self.log_file, 'r+') as f:
            log = json.load(f)
            log.append({'hash': commit_hash, 'message': message, 'timestamp': timestamp})
            f.seek(0)
            json.dump(log, f)

    def list_commits(self):
        with open(self.log_file, 'r') as f:
            log = json.load(f)
            for entry in log:
                print(f"{entry['hash']} - {entry['message']}")

    def list_commits_detailed(self):
        with open(self.log_file, 'r') as f:
            log = json.load(f)
            for entry in log:
                commit_file = os.path.join(self.objects_dir, entry['hash'])
                st = os.stat(commit_file)
                mode = stat.filemode(st.st_mode)
                size = st.st_size
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry['timestamp']))
                print(f"{mode} {size} {mtime} {entry['hash']} - {entry['message']}")

    def add_file(self, file_path):
        if not os.path.isfile(file_path):
            print(f"File '{file_path}' does not exist.")
            return
        with open(file_path, 'rb') as f:
            data = f.read()
        obj_hash = self.write_object(data)
        print(f"File '{file_path}' added with hash {obj_hash}")

    def create_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write("")
        print(f"File '{file_path}' created.")

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' deleted.")
        else:
            print(f"File '{file_path}' does not exist.")

    def create_dir(self, dir_path):
        os.makedirs(dir_path, exist_ok=True)
        print(f"Directory '{dir_path}' created.")

    def delete_dir(self, dir_path):
        if os.path.exists(dir_path):
            os.rmdir(dir_path)
            print(f"Directory '{dir_path}' deleted.")
        else:
            print(f"Directory '{dir_path}' does not exist.")

    def list_files(self, path):
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f'{subindent}{f}')

def main():
    parser = argparse.ArgumentParser(description="Simple VCS")
    parser.add_argument('command', choices=['init', 'commit', 'log', 'ls', 'add', 'touch', 'rmfile', 'mkdir', 'rmdir', 'list-files', 'help', 'h'], help="Command to execute")
    parser.add_argument('repo_dir', help="Repository directory")
    parser.add_argument('-m', '--message', help="Commit message")
    parser.add_argument('-f', '--file', help="File path")
    parser.add_argument('-d', '--dir', help="Directory path")

    args = parser.parse_args()

    if args.command == 'init':
        vcs = SimpleVCS(args.repo_dir)
        print(f"Repository '{args.repo_dir}' initialized.")

    elif args.command == 'commit':
        if args.message:
            vcs = SimpleVCS(args.repo_dir)
            vcs.commit(args.message)
        else:
            print("Commit message is required.")

    elif args.command == 'log':
        vcs = SimpleVCS(args.repo_dir)
        vcs.list_commits()

    elif args.command == 'ls':
        vcs = SimpleVCS(args.repo_dir)
        vcs.list_commits_detailed()

    elif args.command == 'add':
        if args.file:
            vcs = SimpleVCS(args.repo_dir)
            vcs.add_file(args.file)
        else:
            print("File path is required for add command.")

    elif args.command == 'touch':
        if args.file:
            vcs = SimpleVCS(args.repo_dir)
            vcs.create_file(args.file)
        else:
            print("File path is required for create-file command.")

    elif args.command == 'rmfile':
        if args.file:
            vcs = SimpleVCS(args.repo_dir)
            vcs.delete_file(args.file)
        else:
            print("File path is required for delete-file command.")

    elif args.command == 'mkdir':
        if args.dir:
            vcs = SimpleVCS(args.repo_dir)
            vcs.create_dir(args.dir)
        else:
            print("Directory path is required for create-dir command.")

    elif args.command == 'rmdir':
        if args.dir:
            vcs = SimpleVCS(args.repo_dir)
            vcs.delete_dir(args.dir)
        else:
            print("Directory path is required for delete-dir command.")

    elif args.command == 'list-files':
        vcs = SimpleVCS(args.repo_dir)
        vcs.list_files(args.repo_dir)

    elif args.command in ['help', 'h']:
        parser.print_help()

if __name__ == "__main__":
    main()



'''

"""
Summary of what this code does :
1.	Initialization: Creates a directory to store repository objects.
2.	Data hash: Calculates a SHA-1 hash to uniquely identify the data.
3.	Write Data: Writes data to a file named after the hash.
4.	Commit: Encodes a commit message, writes the message to a file, and displays the commit hash.
This code represents a very simplified version of a version control system, mainly focused on commit management.

"""


""" This block imports two standard Python modules:
- os: This module lets you interact with the operating system, in particular to manage directories and files.
- hashlib : This module provides secure hash algorithms for creating cryptographic hashes (such as SHA-1). 
- argparse : adds a CLI to the “simple_vcs.py” file.
- json : To write a Python object to a JSON format file and work with data in JSON (JavaScript Object Notation) format."""
import os
import hashlib
import argparse
import json
import stat
import time

""" This block defines a class called SimpleVCS, representing a simplified version control system.
__init__ method
- Parameter repo_dir: Repository directory where version data will be stored.
- Attribute self.repo_dir: Stores the path to the repository directory.
- Attribute self.objects_dir: Determines the path of the objects sub-directory where objects (commits) will be stored.
- Creation of objects directory : Uses os.makedirs to create the objects directory if it does not already exist. """

# Modifying the SimpleVCS class to take into account the repository directory name
class SimpleVCS:
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.objects_dir = os.path.join(repo_dir, 'objects')
        # Log file for recording commits
        self.log_file = os.path.join(repo_dir, 'log.json')
        os.makedirs(self.objects_dir, exist_ok=True)
        # Log file initialization: If the log file does not exist, it is created and initialized with an empty list.
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    """ 
    The following method calculates the SHA-1 hash of the supplied data.
        1. Parameter data : The data to be hashed.
        2. SHA-1 object creation: hashlib.sha1() creates a new SHA-1 object.
        3. Update with data: sha1.update(data) updates the SHA-1 object with the data.
        4. Return hash: sha1.hexdigest() returns the hash as a hexadecimal string. """

    def hash_object(self, data):
        sha1 = hashlib.sha1()
        sha1.update(data)
        return sha1.hexdigest()
    
    """ 
    The following method writes data to a file after calculating its hash:
        1. Calculates the hash: obj_hash = self.hash_object(data) calculates the data hash.
        2. Determines file path: obj_path = os.path.join(self.objects_dir, obj_hash) creates the full path to the file based on the hash.
        3. Writes data to file: with open(obj_path, 'wb') as f: f.write(data) opens file in binary write mode and writes data to it.
        4. Returns the hash: return obj_hash returns the data hash. """

    def write_object(self, data):
        obj_hash = self.hash_object(data)
        obj_path = os.path.join(self.objects_dir, obj_hash)
        with open(obj_path, 'wb') as f:
            f.write(data)
        return obj_hash
    
    """ This method creates a commit by recording the commit message:
        1. Encodes the message: commit_data = message.encode('utf-8') converts the message into bytes.
        2. Writes the commit: commit_hash = self.write_object(commit_data) writes the commit data to a file and obtains the commit hash.
        3. Displays the commit hash: print(f'Committed with hash {commit_hash}') displays the hash of the newly created commit. """

    def commit(self, message):
        commit_data = message.encode('utf-8')
        commit_hash = self.write_object(commit_data)
        self.log_commit(commit_hash, message)
        print(f'Committed with hash {commit_hash}')

    """
    2. log_commit method:
        * log_commit: logs each commit with its hash and message in the log.json log file."""

    def log_commit(self, commit_hash, message):
        with open(self.log_file, 'r+') as f:
            log = json.load(f)
            log.append({'hash': commit_hash, 'message': message})
            f.seek(0)
            json.dump(log, f)

    """
    3. list_commits method:
        * list_commits: Reads the log file and displays all recorded commits."""

    def list_commits(self):
        with open(self.log_file, 'r') as f:
            log = json.load(f)
            for entry in log:
                print(f"{entry['hash']} - {entry['message']}")

    # To display commit details with the 'ls' command
    def list_commits_detailed(self):
        with open(self.log_file, 'r') as f:
            log = json.load(f)
            for entry in log:
                commit_file = os.path.join(self.objects_dir, entry['hash'])
                # Collect (retrieval , recover) file information for each commit.
                st = os.stat(commit_file) 
                # Converts the file mode into a string similar to ls -l.
                mode = stat.filemode(st.st_mode) 
                # File size.
                size = st.st_size 
                # Formatting the timestamp into a readable string.
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry['timestamp'])) 
                # display rights, size, modification date, hash and commit message.
                print(f"{mode} {size} {mtime} {entry['hash']} - {entry['message']}") 


""" This last block shows how to use the SimpleVCS class:
        1. Instantiate a SimpleVCS object: vcs = SimpleVCS('.my_vcs') creates a new SimpleVCS object with .my_vcs as the repository directory.
        2. Makes a commit: vcs.commit('Initial commit') creates a commit with the message 'Initial commit'. """

# Utilisation
"""vcs = SimpleVCS('.my_vcs')
vcs.commit('Initial commit')
"""

# Adding a simple CLI
def main():
    parser = argparse.ArgumentParser(description="Simple VCS")
    # Log command: Added to the CLI for the listing of commits. Ajout de la nouvelle commande ls à la CLI.
    parser.add_argument('command', choices=['init', 'commit', 'log', 'ls'], help="Command to execute")
    # Adding a mandatory positional argument to specify the repository directory.
    parser.add_argument('repo_dir', help="Repository directory")
    parser.add_argument('-m', '--message', help="Commit message")

    args = parser.parse_args()

    if args.command == 'init':
        vcs = SimpleVCS(args.repo_dir)
        print(f"Repository '{args.repo_dir}' initialized.")

    elif args.command == 'commit':
        if args.message:
            vcs = SimpleVCS('.my_vcs')
            vcs.commit(args.message)
        else:
            print("Commit message is required.")
        
    elif args.command == 'log':
        vcs = SimpleVCS('.my_vcs')
        vcs.list_commits()

    # ls command management 
    elif args.command == 'ls':
        vcs = SimpleVCS(args.repo_dir)
        vcs.list_commits_detailed()
            

if __name__ == "__main__":
    main()


'''