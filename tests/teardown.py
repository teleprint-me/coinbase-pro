import time


class Teardown(object):
    @staticmethod
    def teardown_method():
        # Avoid rate limit
        time.sleep(.25)
