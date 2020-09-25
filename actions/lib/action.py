import os

from st2common.runners.base_action import Action
from st2client.client import Client
from st2client.models.keyvalue import KeyValuePair  # pylint: disable=no-name-in-module

from lib.utils import filter_none_values

__all__ = [
    'St2BaseAction'
]


class St2BaseAction(Action):
    def run(self, **kwargs):
        pass

    def __init__(self, config):
        super(St2BaseAction, self).__init__(config)
        self._client = Client
        self._kvp = KeyValuePair
        self.client = self._get_client()

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

        # not found look up from env vars. Assuming the pack is
        # configuered to work with current StackStorm instance.
        if not api_key:
            api_key = os.environ.get('ST2_ACTION_AUTH_API_KEY', None)

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
        if cacert and cacert == 'True':
            cacert = True
        return cacert

    def _run_client_method(self, method, method_kwargs, format_func, format_kwargs=None):
        """
        Run the provided client method and format the result.

        :param method: Client method to run.
        :type method: ``func``

        :param method_kwargs: Keyword arguments passed to the client method.
        :type method_kwargs: ``dict``

        :param format_func: Function for formatting the result.
        :type format_func: ``func``

        :rtype: ``list`` of ``dict``
        """
        # Filter out parameters with string value of "None"
        # This is a work around since the default values can only be strings
        method_kwargs = filter_none_values(method_kwargs)
        method_name = method.__name__
        self.logger.debug('Calling client method "%s" with kwargs "%s"' % (method_name,
                                                                           method_kwargs))

        result = method(**method_kwargs)
        result = format_func(result, **format_kwargs or {})
        return result

    def _manipulate_rule(self, name, pack, enabled):
        """
        Enable or disable rule.

        :param name: Name of the rule
        :type name: ``str``

        :param pack: Pack where the rule is
        :type pack: ``str``

        :param enabled:
        :type enabled: ``bool``

        :return: Updated rule or string in case of an error
        :rtype: ``dict`` or ``str``
        """

        rule_name = '{}.{}'.format(pack, name)
        failure_reason = None
        rule = None
        try:
            rule = self.client.rules.get_by_name(name=name, pack=pack)
            if not rule:
                failure_reason = 'rule not found'
        except Exception as exc:
            failure_reason = exc

        if failure_reason:
            return 'Could not get rule {}: {}'.format(rule_name, failure_reason)

        try:
            rule_enabled = rule.enabled
        except AttributeError:
            # this should not happen, but better be safe than sorry
            self.logger.debug("Hmm, rule {}.{} doesn't have attribute 'enabled', "
                              "assuming it's off then.".format(name, pack))
            rule_enabled = False

        if rule_enabled == enabled:
            # already enabled/disabled, so just return true and formatted results
            return rule

        try:
            rule.enabled = enabled

            self.client.rules.update(rule)
        except Exception as exc:
            return 'Could not update rule {}: {}'.format(rule_name, exc)

        return rule
