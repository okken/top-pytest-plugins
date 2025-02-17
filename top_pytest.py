import json
import httpx

max_count = 201

def main():
    data_source = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json'
    r = httpx.get(data_source)
    assert r.status_code == 200

    data = json.loads(r.text)
    print(f"Data last updated: {data['last_update']} ")
    print('| # | Package | Downloads | Summary |')
    print('| -- | -- | -- | --- |')
    for i, row in enumerate(get_pytest_rows(data), start=1):
        if i > max_count:
            break
        url = f"https://pypi.org/project/{row['project']}"
        project = row['project']
        count = row['download_count']
        description = get_summary(project)
        print(f"| {i} | [{project}]({url}) | {count:,} | {description} |")

# These packages are deprecated and should not be used
# We'll need to update this list as we review the package list
deprecated_packages = [
    'pytest-runner', # deprecated, recommend use tox
    'pytest-coverage', # not supported, same uthor as pytest-cov, recommend use pytest-cov
    'pytest-cover', # not supported, same uthor as pytest-cov, recommend use pytest-cov
    'pytest-pythonpath', # This plugin is obsolete as of pytest 7.0.0.
    'pytest-parallel', # deprecated, recommend use pytest-xdist
    'pytest-forked', # minimal maintenance. looking for a maintainer
    'pytest-messenger', # no activity sincd 2022, looks abandoned
    'ipytest', # Not a plugin
    ]

extra_named_packages = [
    # Stuff that doesn't have pytest in the name but are plugins, or have 
    # plugin components as part of their package, and are worth considering for the list
    # Note: these all have Framework :: Pytest trove classifiers, so we could search on that

    'hypothesis', # property-based testing, has a built in pytest plugin
    # see https://hypothesis.readthedocs.io/en/latest/details.html#the-hypothesis-pytest-plugin
    'syrupy', # snapshot testing
]

notes = {
    'hypothesis': "Includes a small pytest plugin.",
    'pytest-cov': "Test & Code episode [pytest-cov : The pytest plugin for measuring coverage](https://testandcode.com/episodes/pytest-cov)",
    'pytest-mock': "Test & Code episode [pytest-mock : Mocking in pytest](https://testandcode.com/episodes/pytest-mock)"
}

def get_pytest_rows(json_data):
    for row in json_data['rows']:
        project = row['project']
        if ('pytest' in project and 
            'pytest' != project and 
            project not in deprecated_packages
            ) or (project in extra_named_packages):
            yield row

def get_summary(project):
    try:
        r = httpx.get(f'https://pypi.org/pypi/{project}/json')
        assert r.status_code == 200
        data = r.json()
        summary = data['info'].get('summary', '')
        # Pytest -> pytest
        if summary is None:
            summary = ""
        summary = summary.replace("Pytest", "pytest")
        if project in notes:
            summary += f" ({notes[project]})"
        return summary
    except AssertionError:
        return r.status_code


if __name__ == '__main__':
    main()
