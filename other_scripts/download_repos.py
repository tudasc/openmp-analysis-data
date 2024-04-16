#!/bin/env/python

import pandas as pd
import os
import subprocess
from tqdm import tqdm

REPO_PATH = "./REPOS/"


def cloneRepo(repoUrl, path, re_download=False):
    try:
        # remove any old repo
        if os.path.isdir(path):
            if re_download:
                subprocess.check_output(f'rm -rf {path}', stderr=subprocess.STDOUT, shell=True)
            else:
                # already present
                return

        # download
        subprocess.check_output(f'git clone --depth 1 {repoUrl} {path}', stderr=subprocess.STDOUT, shell=True)


    except subprocess.CalledProcessError as e:
        print("ERROR: downloading Repo:")
        print(e.output)


def main():
    df = pd.read_csv('tj.csv', index_col=0)

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        cloneRepo(row["URL"], REPO_PATH + row["Code"].replace('/', '--'))


if __name__ == '__main__':
    main()
