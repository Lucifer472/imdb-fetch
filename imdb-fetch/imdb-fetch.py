import requests
import json

url = "https://caching.graphql.imdb.com/"
headers = {"Content-Type": "application/json"}

after = "eyJlc1Rva2VuIjpbIjMxNTUzMjgwMDAwMCIsIjEzNyIsInR0MDA4MDI3NCJdLCJmaWx0ZXIiOiJ7XCJjb25zdHJhaW50c1wiOntcIm9yaWdpbkNvdW50cnlDb25zdHJhaW50XCI6e1wiYW55UHJpbWFyeUNvdW50cmllc1wiOltcIklOXCIsXCJHQlwiLFwiVVNcIixcIlhLT1wiLFwiSlBcIl19LFwicmVsZWFzZURhdGVDb25zdHJhaW50XCI6e1wicmVsZWFzZURhdGVSYW5nZVwiOntcImVuZFwiOlwiMjAyNC0wMy0zMVwiLFwic3RhcnRcIjpcIjE5ODAtMDEtMDFcIn19fSxcImxhbmd1YWdlXCI6XCJlbi1VU1wiLFwic29ydFwiOntcInNvcnRCeVwiOlwiWUVBUlwiLFwic29ydE9yZGVyXCI6XCJBU0NcIn0sXCJyZXN1bHRJbmRleFwiOjB9In0"

file_path = "id.txt"

while after:
    payload = {
        "operationName": "AdvancedTitleSearch",
        "variables": {"after":after,"first":1,"locale":"en-US","originCountryConstraint":{"anyPrimaryCountries":["IN","GB","US","XKO","JP"]},"releaseDateConstraint":{"releaseDateRange":{"end":"2024-03-31","start":"1980-01-01"}},"sortBy":"YEAR","sortOrder":"ASC"},
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "65dd1bac6fea9c75c87e2c0435402c1296b5cc5dd908eb897269aaa31fff44b1",
                "version": 1
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        data = response.json()
        if data['data']['advancedTitleSearch']['pageInfo']['hasNextPage']:
            after = data['data']['advancedTitleSearch']['pageInfo']['endCursor']
        else:
            after = None  # No more pages
        title_id = data['data']['advancedTitleSearch']['edges'][0]['node']['title']['id']
        with open(file_path, "a") as file:
            file.write( "\n" + title_id)
        print("Retrieved ID:", title_id)
    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)
        break
    except requests.exceptions.RequestException as err:
        print("Request Error:", err)
        break
    except json.decoder.JSONDecodeError:
        print("Failed to decode response as JSON. Response content:")
        print(response.content.decode())
        break

