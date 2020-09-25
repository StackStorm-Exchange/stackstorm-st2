from lib.action import St2BaseAction
from lib.formatters import format_rule_update_result

__all__ = [
    'St2RulesDisableAction'
]


class St2RulesDisableAction(St2BaseAction):
    def run(self, pack=None, name=None, exclude=None):

        rule = self._manipulate_rule(pack=pack, name=name, enabled=False)
        if rule is None or isinstance(rule, str):
            # error happened
            return False, rule
        else:
            # all good here
            return True, format_rule_update_result(rule, exclude)
