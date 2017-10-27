import sys

from st2common.runners.base_action import Action


class CheckPermission(Action):
    def run(self, collect_anonymous_data):
        if collect_anonymous_data.lower() == "true":
            return True
        # No permission therefore exit 1
        sys.exit(1)
