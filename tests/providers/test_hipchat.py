import pytest

from notifiers import get_notifier
from notifiers.exceptions import BadArguments, NotificationError


class TestHipchat:
    # No online tess for hipchat since they're deprecated and denies new signups
    notifier_name = 'hipchat'

    def test_metadata(self):
        p = get_notifier(self.notifier_name)
        assert p.metadata == {
            'base_url': 'https://{group}.hipchat.com',
            'provider_name': 'hipchat',
            'room_url': '/v2/room/{room}/notification',
            'site_url': 'https://www.hipchat.com/docs/apiv2',
            'user_url': '/v2/user/{user}/message'
        }

    @pytest.mark.parametrize('data, message', [
        ({'id': 'foo', 'token': 'bar', 'message': 'boo', 'room': 'bla', 'user': 'gg'}, 'is valid under each of'),
        ({'id': 'foo', 'token': 'bar', 'message': 'boo', 'room': 'bla', 'team_server': 'gg', 'group': 'gg'},
         'is valid under each of'),
    ])
    def test_missing_required(self, data, message):
        p = get_notifier(self.notifier_name)
        data['env_prefix'] = 'test'
        with pytest.raises(BadArguments) as e:
            p.notify(**data)
        assert f'{message}' in e.value.message

    def test_bad_request(self):
        p = get_notifier(self.notifier_name)
        data = {
            'token': 'foo',
            'room': 'baz',
            'message': 'bar',
            'id': 'bla',
            'group': 'nada'
        }
        with pytest.raises(NotificationError) as e:
            rsp = p.notify(**data)
            rsp.raise_on_errors()
        assert 'Invalid OAuth session' in e.value.message
