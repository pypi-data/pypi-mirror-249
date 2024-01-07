from urllib.parse import urlparse

from ..common.logger import logger
from ..common.types import DatapoolRuleMatch, DatapoolRules


class DatapoolRulesChecker:
    def __init__(self):
        pass

    def match(self, rule_data: DatapoolRules, against: DatapoolRuleMatch):
        # match by content type
        logger.info(f"DatapoolRulesChecker.match {rule_data=} {against=}")
        content_type = DatapoolRulesChecker._into_list(rule_data.content_type)
        if against.content_type not in content_type:
            logger.info(
                f'Content type does not match: {content_type=} vs "{against.content_type=}"'
            )
            return False

        # match by OPTIONAL domain
        if rule_data.domain is not None:
            domain = DatapoolRulesChecker._into_list(rule_data.domain)
            if against.url.host not in domain:
                logger.info(
                    f'Domain does not match: {domain=} vs "{against.url.host=}"'
                )
                return False

        return True

    @staticmethod
    def _into_list(v):
        if type(v) is not list:
            return [v]
        return v
