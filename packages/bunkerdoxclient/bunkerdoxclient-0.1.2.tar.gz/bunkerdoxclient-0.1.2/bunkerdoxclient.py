import os
import json
import requests
from uuid import UUID
import pydantic
from typing import List


BUNKERDOX_DOMAIN = 'https://bunkerdox.com'
KNOWLEDGEBASES_ENDPOINT = '/'.join([BUNKERDOX_DOMAIN, 'api/knowledgebases'])
SEARCH_ENDPOINT = '/'.join([BUNKERDOX_DOMAIN, 'api/search/'])


class AuthenticationError(Exception):
    pass


class Knowledgebase(pydantic.BaseModel):
    id: UUID
    name: str


class KnowledgebaseResponse(pydantic.BaseModel):
    count: pydantic.conint(ge=0)
    knowledgebases: List[Knowledgebase]


class SearchResult(pydantic.BaseModel):
    id: UUID
    display: str
    score: float
    document: UUID
    page: int
    link: str
    content: str


class SearchResponse(pydantic.BaseModel):
    count: pydantic.conint(ge=0)
    results: List[SearchResult]


def raise_exception_if_response_error(response: requests.Response):
    if response.status_code in {401, 403}:
        raise AuthenticationError(response.text)
    
    if response.status_code != 200:
        raise Exception('Error occurred performing this query')


def get_knowledgebases(starts_with: str = '', api_key: str=None) -> KnowledgebaseResponse:
    """
    Retreives the knowledgebases accessible via this API key.

    Parameters
    ----------
    starts_with: str
        Returns only knowledgebases where the display name starts with specified string sequence if specified.
    api_key: str
        The API key to use, overrides the BUNKERDOX_API_KEY environment variable.

    Returns
    -------
    KnowledgebaseResponse
        Knowledgebases accessible via this API key and associated metadata.
    """
    
    params = {}
    if starts_with:
        params['startsWith'] = starts_with

    if api_key is None:
        api_key = os.getenv('BUNKERDOX_API_KEY')

    headers = {
        'Content-Type': 'application/json'
    }

    if api_key is not None:
        headers['x-api-key'] = api_key

    response = requests.get(KNOWLEDGEBASES_ENDPOINT, params=params, headers=headers)
    raise_exception_if_response_error(response)
    
    resp_js = response.json()
    return KnowledgebaseResponse.parse_obj(resp_js)


def search(strQuery: str, knowledgebases: list[UUID]=None, topk: int=4, api_key: str=None) -> SearchResponse:
    """
    Use vector search to find fragments that are closest to the specified search string in the specified knowledgebases.

    Parameters
    ----------
    strQuery: str
        The string query to perform search with.

    knowledgebases: list[UUID]
        The knowledgebases to search through specified as list of their UUIDs.

    topk: int
        The maximum number of results to return.

    api_key: str
        The API key to use, overrides the BUNKERDOX_API_KEY environment variable.

    Returns
    -------
    SearchResponse
        Search results ordered from closest to farthest match and associated metadata.
    """
    
    data = {
        'topk': topk,
        'strQuery': strQuery
    }

    if knowledgebases:
        data['knowledgebases'] = list(map(str, knowledgebases))

    json_data = json.dumps(data)

    if api_key is None:
        api_key = os.getenv('BUNKERDOX_API_KEY')

    headers = {
        'Content-Type': 'application/json'
    }

    if api_key is not None:
        headers['x-api-key'] = api_key

    response = requests.post(SEARCH_ENDPOINT, data=json_data, headers=headers)
    raise_exception_if_response_error(response)
    
    resp_js = response.json()

    return SearchResponse.parse_obj(resp_js)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Performs a search on your BunkerDox knowledgebases.')
    parser.add_argument('strQuery', type=str, help='The search query')
    parser.add_argument('--topk', type=int, default=4, help='Number of documents to retrieve as sources.')
    parser.add_argument('--knowledgebase-ids',  nargs='+', help='Specify which knowledgebases to search by ID')
    parser.add_argument('--api-key', type=str, help='Explicitly specify API key overriding the value set by BUNKERDOX_API_KEY environment variable.')

    args = parser.parse_args()

    response = search(args.strQuery, args.knowledgebase_ids, args.topk, args.api_key)
    print('Result count:', response.count)
    
    for result in response.results:
        print('==============================\n')
        print('Document: ', result.display, '\tPage:', result.page, '\tID:', result.id)
        print('Score:', result.score)
        print('Content:')
        print(result.content)
