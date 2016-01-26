if [ "$LINT" ]; then
    flake8 xlsconv tests --exclude models.py
else
    python setup.py test
fi
