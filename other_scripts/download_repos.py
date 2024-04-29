#!/shared/apps/.gcc/11.2/python/3.9.5/bin/python3.9
import pandas as pd
import os
import subprocess
import shutil
import argparse
import numpy as np

from tqdm import tqdm

skip = False

tqdm.pandas()

# REPO_PATH = "/home/tim/repo_finder/openmp-usage-analysis-binaries/REPOS/"
REPO_PATH = "/home/ci24amun/projects/openmp-usage-analysis/openmp-usage-analysis-binaries/data/"
SCRIPT_PATH = "/home/ci24amun/projects/openmp-usage-analysis/openmp-usage-analysis-binaries/scripts/CI"
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
    if not (os.path.isfile('ci_result.partial.csv') or os.path.isfile('ci_result.csv')):
        print("Using default input")
        df_full = pd.read_csv('ci.csv', index_col=0)
        try:
            df_full.rename(columns={"usedHash": "usedHasOriginal"})
        except :
            print("S.th. whent wrong")
        # promote and expand coulmns
        print("Expanding table with 3 colums")
        df_full.insert(len(df_full.columns),"build_script",np.NaN)
        df_full.insert(len(df_full.columns),"expert","ci")
        df_full.insert(len(df_full.columns),"use_cmake",np.NaN)
        df_full.insert(len(df_full.columns),"use_configure",np.NaN)
        df_full.insert(len(df_full.columns),"usedHash",np.NaN)
        df_full.insert(len(df_full.columns),"note",np.NaN)
        print(" .. done")
    else:
        if os.path.isfile('ci_result.partial.csv'):
            print("Using partial result")
            if (os.path.isfile('ci_result.partial.csv_old')):
                print("Old ci_result.partial.csv_old present, aborting; please move or delete that file")
                return
            df_full = pd.read_csv('ci_result.partial.csv', index_col=0)
    
        
        else:
            if os.path.isfile('ci_result.csv'): 
                df_full = pd.read_csv('ci_result.csv', index_col=0)
            else:
                print("Should not be here")
    
    # df = df_full.iloc[0:2]
    df = df_full
    try:
        #df = df.progress_apply(one_repo_at_a_time, axis=1)
        df = df.progress_apply(intercept_exceptions, axis=1)
        #df = df.apply(intercept_exceptions, axis=1)
    except Exception as e:
        print("Failed with ",e)
        os.rename('ci_result.partial.csv','ci_result.partial.csv_old')
        df.to_csv('ci_result.partial.csv')
        return

    if skip:
        print("*+*+* SKIP Called *+*+*")
        os.rename('ci_result.partial.csv','ci_result.partial.csv_old')
        df.to_csv('ci_result.partial.csv')
        print("Updated ci_result.partial.csv") 
    # df['expert'] = "tj"

    df.to_csv('ci_result.csv')

def intercept_exceptions(row):
    global skip
    if skip:
        return skip_repos(row)
    else:
        try:
            if not skip:
                return one_repo_at_a_time(row)
        except KeyboardInterrupt:
            skip=True
            return skip_repos(row)

def skip_repos(row):
    return row

def one_repo_at_a_time(row):
    path = REPO_PATH + row["Code"].replace('/', '--')
    print("### Processing ",row["Code"].replace('/', '--')," ###")
    try:
        if not (pd.isna(row['build_script']) and pd.isna(row['note'])):
            if row['build_script'] == "autofail.sh":
                customScriptFile= SCRIPT_PATH+"/"+row["Code"].replace('/', '--')+".sh"
#                print("Checking file "+customScriptFile)
                if os.path.isfile(customScriptFile):
                    print(" -> Build script replaced with detected script file:"+"CI/"+row["Code"].replace('/', '--')+".sh")
                    row['build_script']="CI/"+row["Code"].replace('/', '--')+".sh"
                    row['note'] = "TODO:TestScript"
                else:
                    if os.path.isfile(SCRIPT_PATH+"/"+row["Code"].replace('/', '--')+".fail.sh"):
                        row['build_script']="CI/"+row["Code"].replace('/', '--')+".fail.sh"
                        row['note'] = "Confirmed Fail"
                    else:
                        print(" -> Build script automatically derived from previous fail")
            else:
                print (" -> Build script already discovered for "+row["Code"].replace('/', '--'),": ",row['build_script'])
            # already found out the build script
            return row
    except KeyError:
        print ("KeyError: build_script or note unknown")
        

    print ("\t* Dowloading ",row["Code"].replace('/', '--'))
    row['usedHash'] = apply_dowload_repo(row)
 #   print("Downloaded repo with hash",row['usedHash'])
#    print ("##### Attempting compile for ",row["Code"].replace('/', '--'),"###########")
    if "Makefile" in os.listdir(path) or "makefile" in os.listdir(path):
        #print("Makfile in ",path)
        if try_build_script(path, "/home/ci24amun/projects/openmp-usage-analysis/openmp-usage-analysis-binaries/scripts/default_make.sh"):
            row['build_script'] = "default_make.sh"
            row['use_configure'] = False
            row['note']="Autobuild Success"
            print (" -> Makefile successfull for ",row["Code"].replace('/', '--'))
            
            shutil.rmtree(path)
            return row
        else:
            print("\t* Makefile failed") 
    else:
        print("\t* Makefile not available")
    if "CMakeLists.txt" in os.listdir(path):
        #print("cmake in ",path)
        if try_build_script(path, "/home/ci24amun/projects/openmp-usage-analysis/openmp-usage-analysis-binaries/scripts/default_cmake.sh"):
            row['build_script'] = "default_cmake.sh"
            row['use_configure'] = False
            row['note']="Autobuild Success"
            print (" -> cmake successfull for ",row["Code"].replace('/', '--'))
            shutil.rmtree(path)
            return row       
        else:
            print("\t* CMake failed") 
    else:
        print("\t* Cmake not available")
    if "configure" in os.listdir(path):
        #print("Configure in ",path)
        if try_build_script(path, "/home/ci24amun/projects/openmp-usage-analysis/openmp-usage-analysis-binaries/scripts/default_configure.sh"):
            row['build_script'] = "default_configure.sh"
            row['use_configure'] = False
            row['note']="Autobuild Success"
            print (" -> configure & makefile successfull for ",row["Code"].replace('/'))
            shutil.rmtree(path)
            return row
        else:
            print("\t* configure failed") 
    else:
        print("\t* configure not available")
    # save storage space
    print (" -> TODO: autobuild failed for ",row["Code"].replace('/', '--'),"; provide scriptfile \".sh\"")
    row['note']="Autobuild Fail"
    row['build_script']="autofail.sh"
    # Keep the repo for a manual build attempt
    return row
    pass
#    return row


def try_build_script(path, script):
    assert os.path.isfile(script)
    try:
        output = subprocess.check_output("%s %s -O0"%(script,path), cwd=path,
                                         stderr=subprocess.STDOUT,
                                         shell=True, encoding='UTF-8')
        #print(output)
        if "BUILD SUCCESSFUL" in output:
            return True
        else:
            return False

    except subprocess.CalledProcessError as e:
        print("ERROR: building Repo:")
        print(e.output)
    return False


if __name__ == '__main__':
#    parser = argparse.ArgumentParser(
#        prog='downloader',
#        description='Required parameters: --parameters-file, --rules-file, --clusters-file and some job definition.',
#        argument_default=argparse.SUPPRESS
#   )
#    parser.add_argument('--args', help=argparse.SUPPRESS, action='store_true')
#
#
    main()
