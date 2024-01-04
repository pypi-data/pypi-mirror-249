'''
See top level package docstring for documentation
'''

import argparse
import logging
import pathlib

########################################################################

myself = pathlib.Path(__file__).stem
logger = logging.getLogger(__name__)

WARN = True

########################################################################


class DelegatumError(Exception):
    pass


class DelegatumMissError(DelegatumError):
    pass


########################################################################


class Delegatum():
    '''See top level package docstring for documentation'''
    def __init__(self, hierarchy=None, labels=None, default=None):
        self._hierarchy = hierarchy if hierarchy is not None else []

        # _labels should always be the same length as _hierarchy
        if labels is not None:
            self._labels = labels
        else:
            self._labels = [None] * len(self._hierarchy)
        self.default = default

    def __call__(self, key):
        return self[key]

    def __getitem__(self, key):
        # Walk self._hierarchy
        for i, scope in enumerate(self._hierarchy):
            try:
                scope_type = type(scope).__name__
                logger.debug(f"Searching for {key} in {scope_type} [{i}]...")
                return self._lookup(key=key, scope=scope, priority=i)
            except Exception:
                logger.debug(f"Miss for {key} in {scope_type} [{i}]")
        logger.debug("Returning default: {self.default}")
        return self.default

    def __setitem__(self, key, value):
        if WARN:
            logger.warning("Setting values not supported")
            logger.warning("Please set up scope lookups using constructor")
        pass

    def __len__(self):
        return len(self._hierarchy)

    def __str__(self):
        result = ''
        for i, scope in enumerate(self._hierarchy):
            if self._labels[i] is not None:
                label = self._labels[i]
            else:
                label = 'unlabeled scope'
            scope_type = type(scope).__name__
            result += f"Priority {i + 1} {label}, type: {scope_type}\n"
        result += f"Default: {self.default}"
        return result

    def _lookup(self, key, scope, priority=None):
        scope_type = type(scope).__name__
        if False:
            pass  # Kluge for ease of re-ordering
        elif hasattr(scope, '__getitem__') and callable(scope.__getitem__):
            # Scope entry works like a dict
            # This covers configparser.ConfigParser
            if key in scope:
                value = scope[key]
                logger.debug(f"Hit: {value} (from: {scope_type} [{priority}])")
                return value
            raise DelegatumMissError
        elif isinstance(scope, argparse.Namespace):
            if hasattr(scope, key):
                value = getattr(scope, key)
                logger.debug(f"Hit: {value} (from: {scope_type} [{priority}])")
                return value
            raise DelegatumMissError
        elif callable(scope):
            try:
                value = scope(key)
                logger.debug(f"Hit: {value} (from: {scope_type} [{priority}])")
                return value
            except Exception as e:
                logger.debug(f"Callable scope raised exception: {e}")
                pass
        else:
            message = f"Unknown scope type: {scope_type} [{priority}]"
            raise DelegatumError(message)


def main():
    pass


if __name__ == '__main__':
    main()
