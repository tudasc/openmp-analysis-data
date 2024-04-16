#!/bin/env/python

import pandas as pd


def main():
    df = pd.read_csv('found_repos.csv', index_col=0)
    df = df.sort_values('Stars', ascending=False)

    df_tj = df.iloc[0::4]
    df_ci = df.iloc[1::4]
    df_rs = df.iloc[2::4]
    df_mg = df.iloc[3::4]

    df_tj.to_csv('tj.csv')
    df_ci.to_csv('ci.csv')
    df_rs.to_csv('rs.csv')
    df_mg.to_csv('mg.csv')



if __name__ == '__main__':
    main()
