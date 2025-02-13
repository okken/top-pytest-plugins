import json
import httpx

max_count = 200

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
    ]

def get_pytest_rows(json_data):
    for row in json_data['rows']:
        project = row['project']
        if ('pytest' in project and 
            'pytest' != project and 
            project not in deprecated_packages):
            yield row

def get_summary(project):
    try:
        r = httpx.get(f'https://pypi.org/pypi/{project}/json')
        assert r.status_code == 200
        data = r.json()
        return data['info'].get('summary', '')
    except AssertionError:
        return r.status_code


if __name__ == '__main__':
    main()
