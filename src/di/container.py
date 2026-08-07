# di/container.py

from sqlalchemy.orm import Session 

from typing import Callable, TypeVar
import inspect 
T = TypeVar("T")

from functools import wraps


from enum import Enum

class Scope(Enum):
    TRANSIENT = "transient"
    SINGLETON = "singleton"


class Container:
    def __init__(self):
        self.repository = {}
        self.cache = {}
    def register(self, service_type: T, factory: Callable[[], T] | None = None, scope: Scope = Scope.TRANSIENT):
        if factory is None:
            factory = service_type
        self.repository[service_type] = {
            "scope": scope,
            "factory": factory,
        }

    def resolve(self, service_type:T) -> T:
        func_info = self.repository.get(service_type, None)
        if func_info is None:
            raise ValueError(f"Сервис {service_type} не зарегистрирован в контейнере.")

        if func_info["scope"] is Scope.SINGLETON and service_type in self.cache:
            return self.cache.get(service_type, None)

        func = func_info["factory"]
        args = inspect.signature(func)

        kwargs = {}
        for arg in args.parameters.values():
            if arg.annotation is not inspect.Parameter.empty and arg.name != 'self':
                kwargs[arg.name] = self.resolve(arg.annotation)

        result = func(**kwargs)

        if func_info["scope"] is Scope.SINGLETON:
            self.cache[service_type] = result

        return result

    def inject(self, func: Callable):
        @wraps(func)
        def wrap(*args, **kwargs):
            sig = inspect.signature(func)

            bound_args = sig.bind_partial(*args, **kwargs)

            created_sessions = []

            for param_name, param in sig.parameters.items():
                if param_name not in bound_args.arguments:
                    if param.annotation is not inspect.Parameter.empty:
                        resolved_obj = self.resolve(param.annotation)
                        bound_args.arguments[param_name] = resolved_obj

                        if isinstance(resolved_obj, Session):
                            created_sessions.append(resolved_obj)

            try:
                result = func(**bound_args.arguments)
                for s in created_sessions:
                    s.commit()
                return result
            except Exception:
                for s in created_sessions:
                    s.rollback()
                raise
            finally:
                for s in created_sessions:
                    s.close()
                return func(**bound_args.arguments)
        return wrap


def configure_container(container: Container) -> None:
    from datasource import InMemoryStorage
    from datasource import InMemoryGameRepository
    from domain import GameService
    from domain import BotStrategy_MinMax
    from domain import IGameRepository, IBotStrategy
    from domain import GameServiceABC

    container.register(InMemoryStorage, scope=Scope.SINGLETON)
    container.register(IGameRepository, InMemoryGameRepository, scope=Scope.SINGLETON)
    container.register(IBotStrategy, BotStrategy_MinMax, scope=Scope.SINGLETON)
    container.register(GameServiceABC, GameService, scope=Scope.SINGLETON)