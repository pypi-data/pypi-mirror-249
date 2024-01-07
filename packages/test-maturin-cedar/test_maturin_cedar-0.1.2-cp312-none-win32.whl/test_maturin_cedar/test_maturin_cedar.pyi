from typing import Optional


def sum_as_string(a: int, b: int) -> str: ...

class Authorizer:
    def is_authorized(
        self,
        request: tuple[Optional[str], Optional[str], Optional[str]],  # principal, action, resource
        policy_set: str
    ) -> bool: ...
