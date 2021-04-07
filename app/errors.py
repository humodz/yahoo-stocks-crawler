class InvalidRegion(Exception):
    def __init__(self, region):
        super().__init__(f'Invalid region: {region}')
        self.region = region


class MaximumResultsExceeded(Exception):
    def __init__(self, max_results):
        super().__init__(f'Yahoo Finance can only display up to {max_results} results')
