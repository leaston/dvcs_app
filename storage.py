import os
import hashlib
import json
import zlib

class Storage:
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.objects_dir = os.path.join(repo_dir, 'objects')
        self.branches_dir = os.path.join(repo_dir, 'branches')
        self.staging_area = os.path.join(repo_dir, 'staging')
        os.makedirs(self.objects_dir, exist_ok=True)
        os.makedirs(self.branches_dir, exist_ok=True)
        os.makedirs(self.staging_area, exist_ok=True)

    def save_object(self, data):
        compressed_data = self.compress_data(data)
        obj_hash = self.hash_data(compressed_data)
        obj_path = os.path.join(self.objects_dir, obj_hash)
        with open(obj_path, 'wb') as f:
            f.write(compressed_data)
        return obj_hash

    def load_object(self, obj_hash):
        obj_path = os.path.join(self.objects_dir, obj_hash)
        with open(obj_path, 'rb') as f:
            compressed_data = f.read()
        return self.decompress_data(compressed_data)

    def hash_data(self, data):
        return hashlib.sha1(data).hexdigest()

    def compress_data(self, data):
        return zlib.compress(data.encode())

    def decompress_data(self, data):
        return zlib.decompress(data).decode()

    def save_commit(self, commit):
        commit_data = json.dumps(commit)
        return self.save_object(commit_data)

    def load_commit(self, commit_hash):
        commit_data = self.load_object(commit_hash)
        return json.loads(commit_data)

    def save_branch(self, branch_name, commit_hash):
        branch_path = os.path.join(self.branches_dir, branch_name)
        with open(branch_path, 'w') as f:
            f.write(commit_hash)

    def load_branch(self, branch_name):
        branch_path = os.path.join(self.branches_dir, branch_name)
        with open(branch_path, 'r') as f:
            return f.read().strip()

    def add_to_staging(self, files):
        if files == '.':
            files = os.listdir(self.repo_dir)
        for file in files:
            file_path = os.path.join(self.repo_dir, file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    file_data = f.read()
                file_hash = self.save_object(file_data)
                staging_file_path = os.path.join(self.staging_area, file)
                with open(staging_file_path, 'w') as f:
                    f.write(file_hash)

    def get_staging_files(self):
        staging_files = {}
        for file in os.listdir(self.staging_area):
            staging_file_path = os.path.join(self.staging_area, file)
            with open(staging_file_path, 'r') as f:
                file_hash = f.read().strip()
            staging_files[file] = file_hash
        return staging_files

    def clear_staging(self):
        for file in os.listdir(self.staging_area):
            os.remove(os.path.join(self.staging_area, file))
