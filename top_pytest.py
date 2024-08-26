import json
import httpx

def get_pytest_rows(json_data):
    for row in json_data['rows']:
        project = row['project']
        if 'pytest' in project and 'pytest' != project:
            yield row

from pprint import pprint

def get_summary(project):
    try:
        r = httpx.get(f'https://pypi.org/pypi/{project}/json')
        assert r.status_code == 200
        data = r.json()
        return data['info']['summary']

    except AssertionError:
        return r.status_code

def main():
    data_source = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json'
    r = httpx.get(data_source)
    assert r.status_code == 200

    data = json.loads(r.text)
    print(f"Data last updated: {data['last_update']} ")
    print('| # | Package | Downloads | Summary |')
    print('| -- | -- | -- | --- |')
    for i, row in enumerate(get_pytest_rows(data), start=1):
        url = f"https://pypi.org/project/{row['project']}"
        project = row['project']
        count = row['download_count']
        description = get_summary(project)
        print(f"| {i} | [{project}]({url}) | {count:,} | {description} |")

if __name__ == '__main__':
    main()
