RESULT_FILE=ci_result.mk2.csv
all: 
	./other_scripts/download_repos.py ci_result.csv --csvOutput=ci_result.mk2.csv --expert=CI --intermediateResultsFile ci_result.intermediate.csv

start:
	./other_scripts/download_repos.py ci.csv --csvOutput=${RESULT_FILE} --expert=CI --intermediateResultsFile ci_result.intermediate.csv --resume=false

continue:
	if [[ -e ci_result.intermediate.csv ]];then\
		./other_scripts/download_repos.py ci_result.intermediate.csv --csvOutput=ci_result.mk2.csv --expert=CI --intermediateResultsFile ci_result.intermediate.csv \
	else \
		./other_scripts/download_repos.py ${RESULT_FILE} -csvOutput=${RESULT_FILE} --expert=CI --intermediateResultsFile ci_result.intermediate.csv\
	fi	

next:
	./other_scripts/download_repos.py ci_result.intermediate.csv --csvOutput=ci_result.mk2.csv --expert=CI --intermediateResultsFile ci_result.intermediate.csv -n
