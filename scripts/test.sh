#!/bin/bash -e

rm -f htmlcov/*
rm -f .coverage

coverage run --source='.' ./manage.py test

PARMS=--omit='*migrations*'
echo "Coverage results:"
coverage report $PARMS
coverage html $PARMS
coverage xml -o htmlcov/coverage.xml $PARMS
echo "HTML report generated in htmlcov/index.html"
