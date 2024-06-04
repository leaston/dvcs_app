import os
import hashlib
import argparse
import json
import stat
import time

# class SimpleVCS
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