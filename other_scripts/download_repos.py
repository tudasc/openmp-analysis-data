#!/bin/env/python

import pandas as pd
import os
import subprocess
import shutil
from tqdm import tqdm

tqdm.pandas()

REPO_PATH = "./REPOS/"


def cloneRepo(repoUrl, path, commit_hash=None):
    try:
        # remove any old repo
        if not os.path.isdir(path):
            # not already present:
            # download
            subprocess.check_output(f'git clone --depth 1 {repoUrl} {path}', stderr=subprocess.STDOUT, shell=True,
                                    encoding='UTF-8')

        # get current hash, remove trailing \n
        current_hash = subprocess.check_output(f'git rev-parse --verify HEAD', cwd=path, stderr=subprocess.STDOUT,
                                               shell=True, encoding='UTF-8').strip()
        if commit_hash is None or current_hash == commit_hash:
            return current_hash
        else:
            # fetch different revision
            # TODO one could check that origin-url is set up correctly
            subprocess.check_output(f'git fetch --depth 1 origin {commit_hash}', cwd=path, stderr=subprocess.STDOUT,
                                    shell=True, encoding='UTF-8')
            subprocess.check_output(f'git checkout {commit_hash}', cwd=path, stderr=subprocess.STDOUT,
                                    shell=True, encoding='UTF-8')
            return commit_hash

    except subprocess.CalledProcessError as e:
        print("ERROR: downloading Repo:")
        print(e.output)


def apply_dowload_repo(row):
    h = None
    if pd.notna(row['usedHash']):
        h = row['usedHash']
    return cloneRepo(row["URL"], REPO_PATH + row["Code"].replace('/', '--'), h)


def main():
    df_full = pd.read_csv('tj_result.csv', index_col=0)

    # df = df_full.iloc[0:2]
    df = df_full

    df = df.progress_apply(one_repo_at_a_time, axis=1)

    # df['expert'] = "tj"

    print(df['use_configure'].value_counts())

    # print(df['DEFAULT_CMAKE_BUILDABLE'].value_counts())

    df.to_csv('tj_result.csv')


def one_repo_at_a_time(row):
    path = REPO_PATH + row["Code"].replace('/', '--')
    if row['use_cmake']:
        return row

    row['usedHash'] = apply_dowload_repo(row)
    if "configure" in os.listdir(path):
        row['use_configure'] = True
        if try_build_script(path, "./scripts/default_configure.sh"):
            row['build_script'] = "default_configure.sh"
        else:
            pass
            # not buildable
    else:
        row['use_configure'] = False
    # save storage space
    shutil.rmtree(path)
    return row


def try_build_script(path, script):
    assert os.path.isfile(script)
    try:
        output = subprocess.check_output(script, cwd=path,
                                         stderr=subprocess.STDOUT,
                                         shell=True, encoding='UTF-8')
        if "BUILD SUCCESSFUL" in output:
            return True
        else:
            return False

    except subprocess.CalledProcessError as e:
        print("ERROR: building Repo:")
        print(e.output)
    return False


if __name__ == '__main__':
    main()
