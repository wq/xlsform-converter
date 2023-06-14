# xlsform-converter (xlsconv)

xlsform-converter converts surveys defined via the [XLSForm standard] into [Django models] and configuration.  This makes it possible to re-use the powerful form building tools provided by the [Open Data Kit ecosystem][ecosystem], while leveraging Django's robust support for relational databases like [PostgreSQL].

xlsform-converter is designed to facilitate the rapid development of offline-capable data collection apps via the [wq framework].  The ultimate goal is to provide full compatibility with the form authoring tools provided by [ODK][ecosystem] and [KoboToolbox] (etc.).  Note that this is not the same as full XForm compatibility: the client and server components of wq ([wq.app] and [wq.db]) use a JSON-based [REST API] to exchange data and are not directly compatible with their ODK Analogues (ODK Collect and ODK Aggregate, respectively).

For the database itself, the key distinction from other XLSForm tools (including those powered by Django, like KoboToolbox) is that xlsform-converter converts the xlsform fields directly into a Django model definition, rather than representing the entire XForm standard within Django.  This means that each row in an XLSForm "survey" tab is mapped to (usually) a single column in a simple relational database table.  Repeat questions are handled by creating a second model with a `ForeignKey` to the parent survey model.

> For a more thorough comparison of XLSForm tools, see <https://wq.io/overview/survey123-vs-kobotoolbox-vs-wq>.

xlsform-converter also supports a couple of additional "constraints" that are not part of the XLSForm standard:

 * `wq:ForeignKey('app.ModelName')`: Create a foreign key to an existing Django model (presumably not defined in the spreadsheet).  This is effectively a more relational version of `select_one_external`.
 * `wq:initial(3)`: Very similar to `repeat_count`, but only set for new records.
 * `wq:length(5)`: Text field maximum length (similar to a `string-length` constraint)

[![Latest PyPI Release](https://img.shields.io/pypi/v/xlsconv.svg)](https://pypi.org/project/xlsconv)
[![Release Notes](https://img.shields.io/github/release/wq/xlsform-converter.svg)](https://github.com/wq/xlsform-converter/releases)
[![License](https://img.shields.io/pypi/l/xlsconv.svg)](https://github.com/wq/xlsform-converter/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/wq/xlsform-converter.svg)](https://github.com/wq/xlsform-converter/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/wq/xlsform-converter.svg)](https://github.com/wq/xlsform-converter/network)
[![GitHub Issues](https://img.shields.io/github/issues/wq/xlsform-converter.svg)](https://github.com/wq/xlsform-converter/issues)

[![Tests](https://github.com/wq/xlsform-converter/actions/workflows/test.yml/badge.svg)](https://github.com/wq/xlsform-converter/actions/workflows/test.yml)
[![Python Support](https://img.shields.io/pypi/pyversions/xlsconv.svg)](https://pypi.python.org/pypi/xlsconv)

### Included Templates

xlsform-converter uses ASTs and templates to generate the following Django/wq project files from a given XLSForm (for example, [this file](https://github.com/wq/xlsform-converter/raw/main/tests/files/input_types.xls)).

#### Django Apps
   - [`models.py`](https://github.com/wq/xlsform-converter/blob/main/tests/files/input_types/models.py)
   - [`admin.py`](https://github.com/wq/xlsform-converter/blob/main/tests/files/input_types/admin.py) (for use with [`django.contrib.admin`](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/))
   - [`wizard.py`](https://github.com/wq/xlsform-converter/blob/main/tests/files/input_types/wizard.py) (for use with [Django Data Wizard](https://github.com/wq/django-data-wizard))
   - [`rest.py`](https://github.com/wq/xlsform-converter/blob/main/tests/files/input_types/rest.py) (for use with [`wq.db.rest`](https://wq.io/wq.db/rest))
   - [`serializers.py`](https://github.com/wq/xlsform-converter/blob/main/files/input_types/serializers.py) (for use with `wq.db.rest`)

### Usage

If you are using wq, you may be interested in [wq.create], which uses xlsconv internally for the `wq addform` command.  Otherwise, you can use xlsconv directly with the following command-line API:

```bash
# Recommended: create virtual environment
# python3 -m venv venv
# . venv/bin/activate

# Install xlsconv
pip install xlsconv

# Use the default models.py template
xls2django my-odk-survey.xls > myapp/models.py

# Use the rest.py template (or admin.py, or serializers.py)
xls2django my-odk-survey.xls rest > myapp/models.py
```

[XLSForm standard]: https://xlsform.org/
[Django models]: https://docs.djangoproject.com/en/1.9/topics/db/models/
[Mustache templates]: https://wq.io/docs/templates
[ecosystem]: https://getodk.org/about/ecosystem.html
[KoboToolbox]: https://www.kobotoolbox.org/
[PostgreSQL]: http://www.postgresql.org/
[wq framework]: https://wq.io/
[wq.app]: https://wq.io/wq.app/
[wq.db]: https://wq.io/wq.db/
[REST API]: https://wq.io/wq.db/url-structure
[wq.create]: https://wq.io/wq.create/
