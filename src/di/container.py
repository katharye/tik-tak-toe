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

            for param_name, param in sig.parameters.items():
                if param_name not in bound_args.arguments:
                    if param.annotation is not inspect.Parameter.empty:
                        bound_args.arguments[param_name] = self.resolve(param.annotation)

            return func(**bound_args.arguments)
        return wrap


def configure_container(container: Container) -> None:
    from datasource import GameRepository, PlayerRepository
    from domain import IGameRepository, IPlayerRepository
    from domain import AuthService, GameService, BotStrategy_MinMax, JWTProvider
    from domain import IAuthService, IGameService, IBotStrategy, IJWTProvider


    container.register(IGameRepository, GameRepository, scope=Scope.SINGLETON)
    container.register(IBotStrategy, BotStrategy_MinMax, scope=Scope.SINGLETON)
    container.register(IGameService, GameService, scope=Scope.SINGLETON)
    container.register(IAuthService, AuthService, scope=Scope.SINGLETON)
    container.register(IPlayerRepository, PlayerRepository, scope=Scope.SINGLETON)
    container.register(IJWTProvider, JWTProvider, scope=Scope.SINGLETON)
    