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
                st = os.stat(commit_file) # Récupération des informations de fichier pour chaque commit.
                mode = stat.filemode(st.st_mode) # Convertion du mode de fichier en une chaîne de caractères similaire à ce que produit ls -l.
                size = st.st_size # Taille du fichier.
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry['timestamp'])) # Formatage du timestamp en une chaîne lisible.
                print(f"{mode} {size} {mtime} {entry['hash']} - {entry['message']}") # Affichage des droits, de la taille, de la date de modification, de hash et du message du commit.



def main():
    parser = argparse.ArgumentParser(description="Simple VCS")

    parser.add_argument('command', choices=['init', 'commit', 'log', 'ls'], help="Command to execute")

    parser.add_argument('repo_dir', help="Repository directory")
    parser.add_argument('-m', '--message', help="Commit message")

    args = parser.parse_args()

    if args.command == 'init':
        vcs = SimpleVCS(args.repo_dir)
        print(f"Repository '{args.repo_dir}' initialized.") # Displays a message confirming the creation of the repository with the directory name.

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

if __name__ == "__main__":
    main()