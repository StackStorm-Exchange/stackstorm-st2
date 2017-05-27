import os

from st2client.models import LiveAction
from st2client.client import Client
from st2reactor.sensor.base import Sensor

EXECUTION_EVENT_TRIGGER = 'st2.ExecutionEvent'


class ExecutionStatusSensor(Sensor):

    def __init__(self, sensor_service, config=None):

        super(ExecutionStatusSensor, self).__init__(sensor_service=sensor_service,
                                                    config=config)
        self.logger = self.sensor_service.get_logger(
            name=self.__class__.__name__
        )

        self._client = Client
        self.client = self._get_client()

    def setup(self):
        self.config = self._config

    def run(self):

        stream_mgr = self.client.managers['Stream']

        execution = None

        detect_creations = self.config['sensor']['detect_creations']
        action_refs = self.config['sensor']['action_refs']
        statuses_trigger = self.config['sensor']['statuses_trigger']

        if detect_creations:
            events = ['st2.execution__create', 'st2.execution__update']
        else:
            events = ['st2.execution__update']

        for event in stream_mgr.listen(events):
            execution = LiveAction(**event)

            execution_id = execution.action["id"]
            execution_action_ref = execution.action["ref"]
            execution_status = execution.status

            self.logger.info(
                "Execution for action %s just went to %s status" % (
                    execution_action_ref, execution_status
                )
            )

            if execution_action_ref in action_refs and execution_status in statuses_trigger:

                payload = {
                    'execution_id': execution_id,
                    'execution_action_ref': execution_action_ref,
                    'execution_status': execution_status
                }
                self.logger.info(
                    "Matched incoming execution event - triggering %s: %s" % (
                        EXECUTION_EVENT_TRIGGER,
                        payload
                    )
                )
                self._sensor_service.dispatch(trigger=EXECUTION_EVENT_TRIGGER, payload=payload)

    def _get_client(self):
        base_url, api_url, auth_url = self._get_st2_urls()
        cacert = self._get_cacert()

        client_kwargs = {
            'base_url': base_url,
            'api_url': api_url,
            'auth_url': auth_url,
        }

        if cacert:
            client_kwargs['cacert'] = cacert

        api_key = self._get_api_key()
        token = self._get_auth_token()

        # API key has precendece over auth token generated for each action
        # invocation
        if api_key:
            client_kwargs['api_key'] = api_key
        else:
            client_kwargs['token'] = token

        return self._client(**client_kwargs)

    def _get_st2_urls(self):
        # First try to use base_url from config.
        base_url = self.config.get('base_url', None)
        api_url = self.config.get('api_url', None)
        auth_url = self.config.get('auth_url', None)

        # not found look up from env vars. Assuming the pack is
        # configuered to work with current StackStorm instance.
        if not base_url:
            api_url = os.environ.get('ST2_ACTION_API_URL', None)
            auth_url = os.environ.get('ST2_ACTION_AUTH_URL', None)

        return base_url, api_url, auth_url

    def _get_api_key(self):
        api_key = self.config.get('api_key', None)
        return api_key

    def _get_auth_token(self):
        # First try to use auth_token from config.
        token = self.config.get('auth_token', None)

        # not found look up from env vars. Assuming the pack is
        # configuered to work with current StackStorm instance.
        if not token:
            token = os.environ.get('ST2_ACTION_AUTH_TOKEN', None)

        return token

    def _get_cacert(self):
        cacert = self.config.get('cacert', None)
        return cacert

    def cleanup(self):
        # This is called when the st2 system goes down. You can perform
        # cleanup operations like closing the connections to external
        # system here.
        pass

    def add_trigger(self, trigger):
        # This method is called when trigger is created
        pass

    def update_trigger(self, trigger):
        # This method is called when trigger is updated
        pass

    def remove_trigger(self, trigger):
        # This method is called when trigger is deleted
        pass
