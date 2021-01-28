from lib.action import St2BaseAction
from lib.formatters import format_rule_result

__all__ = [
    'St2RulesEnableAction'
]


class St2RulesEnableAction(St2BaseAction):
    def run(self, pack=None, name=None, exclude=None):

        rule = self._manipulate_rule(pack=pack, name=name, enabled=True)
        return format_rule_result(rule, exclude)
