import argparse
from core import SimpleVCS
import os

def main():
    parser = argparse.ArgumentParser(description="Simple VCS")
    parser.add_argument('command', choices=[
        'init', 'add', 'commit', 'log', 'branch', 'checkout', 'merge', 'reset', 'help', 'h', 
        'mkdir', 'create_file', 'rm', 'cd', 'ls'], help="Command to execute")
    parser.add_argument('repo_dir', help="Repository directory")
    parser.add_argument('name', nargs='?', help="Branch name, commit message, or file/directory name")
    parser.add_argument('source', nargs='?', help="Source branch for merge command")
    parser.add_argument('-m', '--message', help="Commit message")
    args = parser.parse_args()

    vcs = SimpleVCS(args.repo_dir)

    if args.command == 'init':
        vcs.init_repo()

    elif args.command == 'add':
        if args.name:
            vcs.add(args.name.split())
        else:
            vcs.add('.')

    elif args.command == 'commit':
        if args.message:
            vcs.commit(args.message)
        else:
            print("Commit message is required.")

    elif args.command == 'log':
        vcs.list_commits()

    elif args.command == 'branch':
        if args.name:
            vcs.create_branch(args.name)
        else:
            print("Branch name is required.")

    elif args.command == 'checkout':
        if args.name:
            vcs.checkout(args.name)
        else:
            print("Branch name is required.")

    elif args.command == 'merge':
        if args.source:
            vcs.merge(args.source)
        else:
            print("Source branch name is required.")

    elif args.command == 'reset':
        if args.name:
            vcs.reset_to_commit(args.name)
        else:
            print("Commit hash is required.")

    elif args.command in ['help', 'h']:
        parser.print_help()

    elif args.command == 'mkdir':
        if args.name:
            os.makedirs(os.path.join(args.repo_dir, args.name), exist_ok=True)
            print(f"Directory '{args.name}' created.")
        else:
            print("Directory name is required.")
            
    elif args.command == 'create_file':
        if args.name:
            file_path = os.path.join(args.repo_dir, args.name)
            with open(file_path, 'w') as f:
                pass
            print(f"File '{args.name}' created.")
        else:
            print("File name is required.")
            
    elif args.command == 'rm':
        if args.name:
            target_path = os.path.join(args.repo_dir, args.name)
            if os.path.isdir(target_path):
                os.rmdir(target_path)
                print(f"Directory '{args.name}' removed.")
            elif os.path.isfile(target_path):
                os.remove(target_path)
                print(f"File '{args.name}' removed.")
            else:
                print(f"'{args.name}' does not exist.")
        else:
            print("Target name is required.")
            
    elif args.command == 'cd':
        if args.name:
            os.chdir(os.path.join(args.repo_dir, args.name))
            print(f"Changed directory to '{args.name}'.")
        else:
            print("Directory name is required.")
            
    elif args.command == 'ls':
        for entry in os.listdir(args.repo_dir):
            print(entry)

if __name__ == "__main__":
    main()
