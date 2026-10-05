from backend.domain.repositories.unit_of_work import UnitOfWork


class LocalUnitOfWork(UnitOfWork):
    def commit(self) -> None:
        print("Commit")

    def rollback(self) -> None:
        print("Rollback")

    def __enter__(self) -> UnitOfWork:
        print('start of unit wor')
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None: # type: ignore
        print('exit of unit of work')
