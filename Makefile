RESULT_FILE=ci_result.mk2.csv
INTERMEDIATE_RESULTS=ci_result.intermediate.csv
all:
	./other_scripts/download_repos.py ci_result.csv --basePath='.' --repoPath='./data'  --csvOutput=ci_result.mk2.csv --expert=CI --intermediateResultsFile $(INTERMEDIATE_RESULTS)

start:
	./other_scripts/download_repos.py ci.csv --basePath='.' --repoPath='./data'  --csvOutput=$(RESULT_FILE) --expert=CI --intermediateResultsFile $(INTERMEDIATE_RESULTS) --resume=false

continue:
	@if [[ -e $(INTERMEDIATE_RESULTS) ]] ; then \
	@echo Continuing;\
	./other_scripts/download_repos.py $(INTERMEDIATE_RESULTS) --basePath='.' --repoPath='./data' --csvOutput=ci_result.mk2.csv --expert=CI --intermediateResultsFile $(INTERMEDIATE_RESULTS) ;\
	else \
	./other_scripts/download_repos.py $(RESULT_FILE) --basePath='.' --repoPath='./data' --csvOutput=$(RESULT_FILE) --expert=CI --intermediateResultsFile $(INTERMEDIATE_RESULTS) ;\
	fi

next:
	@if [[ -e $(INTERMEDIATE_RESULTS) ]] ; then \
	./other_scripts/download_repos.py $(INTERMEDIATE_RESULTS) --basePath='.' --repoPath='./data'  --csvOutput=ci_result.mk2.csv --expert=CI --intermediateResultsFile $(INTERMEDIATE_RESULTS) -n ;\
	else \
	./other_scripts/download_repos.py $(RESULT_FILE) --basePath='.' --repoPath='./data'  --csvOutput=$(RESULT_FILE) --expert=CI --intermediateResultsFile $(INTERMEDIATE_RESULTS) -n ; \
	fi

test:
	./other_scripts/download_repos.py ci.csv --basePath='.' --repoPath='./data' --csvOutput=test_csv.csv --expert=CI --intermediateResultsFile ci_test.intermee.csv --resume=false --verbose
	#/home/ci24amun/projects/openmp-usage-analysis/openmp-usage-analysis-binaries
