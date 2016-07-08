if [ "$LINT" ]; then
    flake8 xlsconv tests
else
    python setup.py test
fi
