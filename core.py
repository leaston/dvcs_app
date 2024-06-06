from storage import Storage
import os

class SimpleVCS:
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.storage = Storage(repo_dir)
        self.current_branch_file = os.path.join(repo_dir, 'HEAD')
        self.init_repo()

    def init_repo(self):
        if not os.path.exists(self.current_branch_file):
            with open(self.current_branch_file, 'w') as f:
                f.write('main')
        self.create_branch('main')
        print(f"Repository initialized in {self.repo_dir}")

    def create_branch(self, branch_name):
        if not self.branch_exists(branch_name):
            self.storage.save_branch(branch_name, self.get_latest_commit())
            print(f"Branch '{branch_name}' created.")
        else:
            print(f"Branch '{branch_name}' already exists.")

    def branch_exists(self, branch_name):
        branch_path = os.path.join(self.storage.branches_dir, branch_name)
        return os.path.exists(branch_path)

    def checkout(self, branch_name):
        if self.branch_exists(branch_name):
            self.set_current_branch(branch_name)
            print(f"Switched to branch '{branch_name}'")
        else:
            print(f"Branch '{branch_name}' does not exist.")

    def set_current_branch(self, branch_name):
        with open(self.current_branch_file, 'w') as f:
            f.write(branch_name)

    def get_current_branch(self):
        with open(self.current_branch_file, 'r') as f:
            return f.read().strip()

    def get_latest_commit(self):
        current_branch = self.get_current_branch()
        return self.storage.load_branch(current_branch)

    def merge(self, source_branch):
        target_branch = self.get_current_branch()
        if not self.branch_exists(source_branch):
            print(f"Source branch '{source_branch}' does not exist.")
            return

        source_commit = self.storage.load_branch(source_branch)
        target_commit = self.storage.load_branch(target_branch)

        source_tree = self.storage.load_commit(source_commit)
        target_tree = self.storage.load_commit(target_commit)

        merged_tree, conflicts = self.merge_trees(source_tree, target_tree)

        if conflicts:
            print("Merge conflicts detected!")
            for conflict in conflicts:
                print(conflict)
            return

        merged_commit_hash = self.storage.save_commit(merged_tree)
        self.storage.save_branch(target_branch, merged_commit_hash)
        print(f"Branch '{source_branch}' merged into '{target_branch}' successfully.")

    def merge_trees(self, source_tree, target_tree):
        merged_tree = {}
        conflicts = []

        for path in set(source_tree.keys()).union(target_tree.keys()):
            if path in source_tree and path in target_tree:
                if source_tree[path] == target_tree[path]:
                    merged_tree[path] = source_tree[path]
                else:
                    conflicts.append(f"Conflict at {path}")
            elif path in source_tree:
                merged_tree[path] = source_tree[path]
            else:
                merged_tree[path] = target_tree[path]

        return merged_tree, conflicts

    def add(self, files):
        self.storage.add_to_staging(files)
        print(f"Added files to staging: {files}")

    def commit(self, message):
        staged_files = self.storage.get_staging_files()
        commit_data = {
            'message': message,
            'parent': self.get_latest_commit(),
            'files': staged_files
        }
        commit_hash = self.storage.save_commit(commit_data)
        current_branch = self.get_current_branch()
        self.storage.save_branch(current_branch, commit_hash)
        self.storage.clear_staging()
        print(f'Committed with hash {commit_hash}')

    def list_commits(self):
        current_commit = self.get_latest_commit()
        while current_commit:
            commit = self.storage.load_commit(current_commit)
            print(f"{current_commit} - {commit['message']}")
            current_commit = commit.get('parent')

    def reset_to_commit(self, commit_hash):
        current_branch = self.get_current_branch()
        self.storage.save_branch(current_branch, commit_hash)
        print(f"Branch '{current_branch}' reset to commit '{commit_hash}'")
