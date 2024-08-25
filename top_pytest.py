import json
import httpx

def get_pytest_rows(json_data):
    for row in json_data['rows']:
        project = row['project']
        if 'pytest' in project and 'pytest' != project:
            yield row

def main():
    data_source = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json'
    r = httpx.get(data_source)
    assert r.status_code == 200

    data = json.loads(r.text)
    print(f"Data last updated: {data['last_update']} ")
    print('| | Package | Downloads | Description |')
    print('| -- | -- | -- | --- |')
    for i, row in enumerate(get_pytest_rows(data), start=1):
        url = f"https://pypi.org/project/{row['project']}"
        print(f"| {i} | [{row['project']}]({url}) | {row['download_count']:,} |")

if __name__ == '__main__':
    main()
