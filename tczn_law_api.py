import json
from wsgiref.simple_server import make_server
import requests
# from numba.roc.decorators import autojit
from requests.auth import HTTPBasicAuth
# import numba
# from numba import jit

auth = HTTPBasicAuth('tczn', 'tczn123!@#')
url = "http://localhost:9200/wenshu/_search"


def application(environ, start_response):
    # global qar_file_path
    # global is_running
    start_response('200 OK', [('Content-Type', 'application/json'),
                              ('Access-Control-Allow-Origin', '*')])
    print(environ['PATH_INFO'])
    method = environ['PATH_INFO']
    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    request_body = environ['wsgi.input'].read(request_body_size)
    params = json.loads(request_body)

    if method == '/api/search':
        page_index = params['page_index']
        page_item_size = params['page_item_size']
        keyword = params['keyword']
        slop = params['slop']
        dataObject = {
          'from': page_index,
          'size': page_item_size,
          'highlight': {
            'fields': {
              'case_content': {}
            }
          },
          '_source': {
    'includes': [
      "case_name"
    ],
    'excludes': []
  },
          'query': {
            'bool': {
              'filter': [{
                'bool': {
                  'must': [{
                    'match_phrase': {
                      'case_content': {
                        'query': keyword,
                        'slop': slop,
                        'zero_terms_query': "NONE",
                        'boost': 1
                      }
                    }
                  }],
                  'adjust_pure_negative': True,
                  'boost': 1
                }
              }],
              'adjust_pure_negative': True,
              'boost': 1
            }
          }
        }

        res = requests.post(url=url, json=dataObject, auth=auth)
        
        return [res.text.encode()]

    if method == '/api/detail':
        id = params['id']
        dataObject = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'match': {
                                'id': id
                            }
                        }
                    ]
                }
            }
        }

        res = requests.post(url=url, json=dataObject, auth=auth)
        # res = requests.post(url=url, json=dataObject)
        return [res.text.encode()]

if __name__ == "__main__":
    port = 5088
    httpd = make_server("0.0.0.0", port, application)
    print('serving http on port {0}...'.format(str(port)))
    httpd.serve_forever()
