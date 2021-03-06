import os

import pytest

from ..helpers import create_flow, assert_request, get_results

cur_dir = os.path.dirname(os.path.abspath(__file__))
compose_yml = os.path.join(cur_dir, 'docker-compose.yml')
flow_yml = os.path.join(cur_dir, 'flow.yml')
pod_dir = os.path.join(cur_dir, 'pods')


@pytest.mark.skip(reason='using daemon for container runtime is untest and unimplemented')
@pytest.mark.parametrize('docker_compose', [compose_yml], indirect=['docker_compose'])
def test_simple_hub_pods(docker_compose):
    flow_id = create_flow(flow_yml)
    print(f'Flow created with id {flow_id}')

    expected_text = 'text:hey, dude'
    response = assert_request(method='post',
                              url='http://0.0.0.0:45678/api/search',
                              payload={'top_k': 10, 'data': [expected_text]})
    print(f'Response is: {response}')

    text_matched = get_results(query=expected_text)['search']['docs'][0]['text']
    print(f'Returned document has the text: {text_matched}')

    assert_request(method='get',
                   url=f'http://0.0.0.0:8000/flow/{flow_id}')

    assert_request(method='delete',
                   url=f'http://0.0.0.0:8000/flow?flow_id={flow_id}')

    assert expected_text == text_matched
