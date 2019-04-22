import os
import yaml

from st2tests.base import BaseActionTestCase


class BaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(BaseActionTestCase, self).setUp()

        self.full_config = self._load_yaml('full.yaml')
        self.blank_config = self._load_yaml('blank.yaml')

        # touch cacert file that is referred in test-case
        open(self.full_config['cacert'], 'a').close()

    def tearDown(self):
        # delete temporary files which are created for this test
        os.remove(self.full_config['cacert'])

    def _load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))
