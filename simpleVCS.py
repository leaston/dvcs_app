import os
import hashlib


class SimpleVCS:
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.objects_dir = os.path.join(repo_dir, 'objects')
        os.makedirs(self.objects_dir, exist_ok=True)


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
        print(f'Committed with hash {commit_hash}')


# Utilisation
vcs = SimpleVCS('.my_vcs')
vcs.commit('Initial commit')
