

from typing import Dict


class Features(dict):
    def __init__(*args, **kwargs):
        # self not in the signature to allow passing self as a kwarg
        if not args:
            raise TypeError("descriptor '__init__' of 'Features' object needs an argument")
        self, *args = args
        super(Features, self).__init__(*args, **kwargs)
