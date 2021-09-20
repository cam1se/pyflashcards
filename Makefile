


# This must be run from the directory it exists in.

PACKAGE_DIR			:= pyflashcards
DOCS_DIR			:= docs
REPORTS_DIR			:= reports
COVERAGE_BADGE		:= ${DOCS_DIR}/_static/coverage.svg

######################################### General ############################################################

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: clean format lint tests docs build ## Clean everything, then format code, lint, run tests, build docs, and build package

.PHONY: clean_artifacts
clean_artifacts:
	@echo "Cleaning artifacts..."
	@$$(find . -type f -name '*.py[co]' -delete -o -type d -name '__pycache__' -delete)
	@$$(find . -type f -name '*.log' -delete)
	@$$(find . -type f -name '*.jpg' -delete)
	@$$(find . -type f -name '*.mp4' -delete)
	@$$(find . -type f -name '*.JPG' -delete)
	@$$(find . -type f -name '*.MP4' -delete)
	@$$(find . -type f -name '*.csv' -delete)
	@rm -rf .mypy_cache

.PHONY: clean
clean: clean_artifacts clean_tests clean_docs clean_build  ## Clean tests, docs, and build

.PHONY: reports
reports: ## Make the reports dir if it doesn't exist
	@mkdir -p ${REPORTS_DIR}


########################################## Testing ###########################################################

.PHONY: clean_tests
clean_tests: ## Clean raw coverage and html results
	@echo "Cleaning tests..."
	@rm -rf ${REPORTS_DIR}
	@rm -rf .pytest_cache

.PHONY: tests
unit_tests: # Run unit tests.
	@echo "Running unit tests..."
	@pytest tests

.PHONY: coverage
coverage: ## Build the coverage badge from the test results
	@echo "Building coverage badge..."
	@rm -f ${COVERAGE_BADGE}
	@coverage-badge -o ${COVERAGE_BADGE}

###################################### Static Code Analyis ###################################################

.PHONY: format
format: ## Run Black to format code
	@echo "Running black to format all python code..."
	@black . --line-length 111 --exclude venv

.PHONY: lint
lint: reports ## Run mypy for static typing analysis and pylint for linting
	@echo "Performing static typing analysis..."
	@mypy pyflashcards | tee ${REPORTS_DIR}/linting
	@echo "Linting..."
	@pylint pyflashcards | tee -a ${REPORTS_DIR}/linting

######################################### Documentation ######################################################

.PHONY: clean_docs
clean_docs:  ## Remove generated docs
	@echo "Cleaning docs..."
	@rm -f ${DOCS_DIR}/modules.rst
	@rm -rf ${DOCS_DIR}/build

.PHONY: docs-api-check
docs-api-check: clean_artifacts ## Static analysis of docstrings for missing / errors
	@echo "Validating docstrings..."
	@pydocstyle -ve ${PACKAGE_DIR}/** | tee ${REPORTS_DIR}/docstrings

.PHONY: sphinx
sphinx: clean_docs reports ## Generate Sphinx documentation
	@echo "Building html documentation..."
	@cd ${DOCS_DIR} && sphinx-build -W -b html . build
	@rm -rf ${DOCS_DIR}/build/.doctrees ${DOCS_DIR}/build/_sources ${DOCS_DIR}/build/_static/fonts

.PHONY: docs
docs: docs-api-check sphinx ## Generate all documentation with prerequisite checks.

############################################## Publishing ####################################################

.PHONY: clean_build
clean_build: ## Clean build artifacts
	@rm -rf build dist

.PHONY: build
build: clean_build ## Build dist but do not publish
	@python setup.py sdist

.PHONY: publish
publish: build  ## Build and publish to PyPi
	@twine upload dist/*
