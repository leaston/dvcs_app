import os
import hashlib
import argparse
import json

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
        with open(self.log_file, 'r+') as f:
            log = json.load(f)
            log.append({'hash': commit_hash, 'message': message})
            f.seek(0)
            json.dump(log, f)

    def list_commits(self):
        with open(self.log_file, 'r') as f:
            log = json.load(f)
            for entry in log:
                print(f"{entry['hash']} - {entry['message']}")

def main():
    parser = argparse.ArgumentParser(description="Simple VCS")
    parser.add_argument('command', choices=['init', 'commit', 'log'], help="Command to execute")
    parser.add_argument('repo_dir', help="Repository directory")
    parser.add_argument('-m', '--message', help="Commit message")

    args = parser.parse_args()

    if args.command == 'init':
        vcs = SimpleVCS(args.repo_dir)
        print("Repository initialized.")

    elif args.command == 'commit':
        if args.message:
            vcs = SimpleVCS(args.repo_dir)
            vcs.commit(args.message)
        else:
            print("Commit message is required.")

    elif args.command == 'log':
        vcs = SimpleVCS(args.repo_dir)
        vcs.list_commits()

if __name__ == "__main__":
    main()
