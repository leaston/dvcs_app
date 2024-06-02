"""
Summary of what this code does
1.	Initialization: Creates a directory to store repository objects.
2.	Data hash: Calculates a SHA-1 hash to uniquely identify the data.
3.	Write Data: Writes data to a file named after the hash.
4.	Commit: Encodes a commit message, writes the message to a file, and displays the commit hash.
This code represents a very simplified version of a version control system, mainly focused on commit management.

"""


""" This block imports two standard Python modules:
- os: This module lets you interact with the operating system, in particular to manage directories and files.
- hashlib : This module provides secure hash algorithms for creating cryptographic hashes (such as SHA-1). """
import os
import hashlib

""" This block defines a class called SimpleVCS, representing a simplified version control system.
__init__ method
- Parameter repo_dir: Repository directory where version data will be stored.
- Attribute self.repo_dir: Stores the path to the repository directory.
- Attribute self.objects_dir: Determines the path of the objects sub-directory where objects (commits) will be stored.
- Creation of objects directory : Uses os.makedirs to create the objects directory if it does not already exist. """

class SimpleVCS:
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.objects_dir = os.path.join(repo_dir, 'objects')
        os.makedirs(self.objects_dir, exist_ok=True)

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
    The following method writes data to a file after calculating its hash.
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
    
    """ The last method creates a commit by recording the commit message.
        1. Encodes the message: commit_data = message.encode('utf-8') converts the message into bytes.
        2. Writes the commit: commit_hash = self.write_object(commit_data) writes the commit data to a file and obtains the commit hash.
        3. Displays the commit hash: print(f'Committed with hash {commit_hash}') displays the hash of the newly created commit. """

    def commit(self, message):
        commit_data = message.encode('utf-8')
        commit_hash = self.write_object(commit_data)
        print(f'Committed with hash {commit_hash}')

""" This last block shows how to use the SimpleVCS class.
        1. Instantiate a SimpleVCS object: vcs = SimpleVCS('.my_vcs') creates a new SimpleVCS object with .my_vcs as the repository directory.
        2. Makes a commit: vcs.commit('Initial commit') creates a commit with the message 'Initial commit'. """

# Utilisation
vcs = SimpleVCS('.my_vcs')
vcs.commit('Initial commit')
