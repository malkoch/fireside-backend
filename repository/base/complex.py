class ComplexRepository:
    def __init__(self, repositories):
        self._repositories = repositories

    def __getattr__(self, item):
        return self._repositories[item]
