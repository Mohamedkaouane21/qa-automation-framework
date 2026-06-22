# Convenience targets. Run `make help` for the list.
.DEFAULT_GOAL := help
PYTEST := python -m pytest

# Retries absorb transient flakiness from the public demo targets (Heroku
# cold starts, network blips) without hiding real failures.
RERUN := --reruns 2 --reruns-delay 3

.PHONY: help install browsers lint format unit api ui bdd smoke test trace report docker clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install package + dev dependencies
	pip install -e ".[dev]"

browsers: ## Install Playwright browsers
	python -m playwright install --with-deps

lint: ## Ruff + black checks
	ruff check .
	black --check .

format: ## Auto-format with black + ruff --fix
	ruff check --fix .
	black .

unit: ## Unit tests with coverage gate
	$(PYTEST) -m unit --cov=src --cov-report=term-missing --cov-report=xml

api: ## API tests
	$(PYTEST) -m api $(RERUN)

ui: ## UI tests (headless, all artifacts on failure)
	$(PYTEST) -m ui $(RERUN) --screenshot=only-on-failure \
		--video=retain-on-failure --tracing=retain-on-failure \
		--output=reports/ui-artifacts

bdd: ## BDD scenarios
	$(PYTEST) -m bdd $(RERUN) --screenshot=only-on-failure --output=reports/ui-artifacts

smoke: ## Fast smoke subset across all layers
	$(PYTEST) -m smoke $(RERUN)

test: ## Full suite (unit + api + ui + bdd)
	$(PYTEST) $(RERUN) --screenshot=only-on-failure \
		--video=retain-on-failure --tracing=retain-on-failure \
		--output=reports/ui-artifacts

trace: ## Regenerate the requirements traceability matrix
	python scripts/gen_traceability.py

report: ## Generate the Allure HTML report from results
	allure generate reports/allure-results --clean -o reports/allure-report

docker: ## Build the container image
	docker build -t qa-framework .

clean: ## Remove generated artifacts
	rm -rf reports .coverage coverage.xml .pytest_cache
