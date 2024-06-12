#!/bin/env/python

import pandas as pd


def main():

    df_tj = pd.read_csv('tj_result.csv', index_col=0)
    df_ci = pd.read_csv('ci_result.csv', index_col=0)
    df_rs = pd.read_csv('rs_result.csv', index_col=0)
#    df_mg = pd.read_csv('results.csv', index_col=0)

    df = pd.concat([df_tj, df_ci, df_rs])

    df.to_csv('result.csv')



if __name__ == '__main__':
    main()
