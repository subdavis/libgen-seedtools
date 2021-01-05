#!/bin/bash

black .
isort .
mypy . --ignore-missing-imports