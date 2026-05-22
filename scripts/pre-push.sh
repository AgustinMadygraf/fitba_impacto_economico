#!/bin/bash

# Pre-push hook: Check syntax and run tests

echo "Running pre-push checks..."

# 1. Run tests with coverage
.venv/bin/python -m pytest --cov=src --cov-fail-under=80 tests/
if [ $? -ne 0 ]; then
    echo "Tests failed or coverage below 80%."
    exit 1
fi

echo "Pre-push checks passed!"
exit 0
