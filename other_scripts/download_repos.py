#!/bin/env/python

import pandas as pd
import os
import subprocess
from tqdm import tqdm

REPO_PATH = "./REPOS/"


def cloneRepo(repoUrl, path, commit_hash=None):
    try:
        # remove any old repo
        if not os.path.isdir(path):
            # not already present:
            # download
            subprocess.check_output(f'git clone --depth 1 {repoUrl} {path}', stderr=subprocess.STDOUT, shell=True)

        # get current hash, remove trailing \n
        current_hash = subprocess.check_output(f'git rev-parse --verify HEAD', cwd=path, stderr=subprocess.STDOUT,
                                               shell=True, encoding='UTF-8').strip()
        if commit_hash is None or current_hash == commit_hash:
            return current_hash
        else:
            # fetch different revision
            # TODO one could check that origin-url is set up correctly
            subprocess.check_output(f'git fetch --depth 1 origin {commit_hash}', cwd=path, stderr=subprocess.STDOUT,
                                    shell=True)
            subprocess.check_output(f'git checkout {commit_hash}', cwd=path, stderr=subprocess.STDOUT,
                                    shell=True, )
            return commit_hash

    except subprocess.CalledProcessError as e:
        print("ERROR: downloading Repo:")
        print(e.output)


def apply_dowload_repo(row):
    print(row)
    h = None
    if pd.notna(row['usedHash']):
        h = row['usedHash']
    return cloneRepo(row["URL"], REPO_PATH + row["Code"].replace('/', '--'), h)


def main():
    df_full = pd.read_csv('tj.csv', index_col=0)

    df = df_full.iloc[0:3]
    df['usedHash'] = df.apply(apply_dowload_repo, axis=1)
    df['expert'] = "tj"

    df.to_csv('tj_result.csv')


if __name__ == '__main__':
    main()
