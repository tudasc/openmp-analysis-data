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
    df_full = pd.read_csv('tj.csv', index_col=0)

    # df = df_full.iloc[0:2]
    df = df_full

    df = df.progress_apply(one_repo_at_a_time, axis=1)

    # df['usedHash'] = df.progress_apply(apply_dowload_repo, axis=1)
    # df['expert'] = "tj"

    # df.to_csv('tj_result.csv')

    # df['use_cmake'] = df.progress_apply(has_cmake_list, axis=1)

    # print(df['use_cmake'].value_counts())

    # df['DEFAULT_CMAKE_BUILDABLE'] = df.progress_apply(can_build_default_cmake, axis=1)
    # print(df['DEFAULT_CMAKE_BUILDABLE'].value_counts())

    df.to_csv('tj_result.csv')


def one_repo_at_a_time(row):
    path = REPO_PATH + row["Code"].replace('/', '--')
    row['usedHash'] = apply_dowload_repo(row)
    if "CMakeLists.txt" in os.listdir(path):
        row['use_cmake'] = True
        if can_build_default_cmake(row):
            row['DEFAULT_CMAKE_BUILDABLE'] = True
        else:
            row['DEFAULT_CMAKE_BUILDABLE'] = False
    else:
        row['use_cmake'] = False
        row['DEFAULT_CMAKE_BUILDABLE'] = False
    # save storage space
    shutil.rmtree(path)
    return row


def has_cmake_list(row):
    path = REPO_PATH + row["Code"].replace('/', '--')
    if "CMakeLists.txt" in os.listdir(path):
        return True
    return False


def can_build_default_cmake(row):
    path = REPO_PATH + row["Code"].replace('/', '--')
    if "CMakeLists.txt" in os.listdir(path):
        if try_default_cmake_build(path):
            return True
    return False


def try_default_cmake_build(path):
    build_dir = path + "/build"
    try:
        # remove
        if os.path.isdir(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir, exist_ok=True)
        # configure
        subprocess.check_output(f'cmake .. -DCMAKE_C_FLAGS="-O0" -DCMAKE_CXX_FLAGS="-O0"', cwd=build_dir,
                                stderr=subprocess.STDOUT,
                                shell=True, encoding='UTF-8')
        # building
        subprocess.check_output(f'cmake --build .', cwd=build_dir,
                                stderr=subprocess.STDOUT,
                                shell=True, encoding='UTF-8')
        return True

    except subprocess.CalledProcessError as e:
        print("ERROR: building Repo:")
        print(e.output)
    return False


if __name__ == '__main__':
    main()
