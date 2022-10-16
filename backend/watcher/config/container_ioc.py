from dependency_injector import containers, providers

from watcher.dummy.infra.adapters.dummy_adapters import ListDummyUsers


class Container(containers.DeclarativeContainer):
    # config = providers.Configuration()
    # config = providers.Configuration(yaml_files=['config.yml'])

    # db = providers.Singleton('db', db_url=config.db.url)
    wiring_config = containers.WiringConfiguration(modules=["watcher.api.api"])
    config = providers.Configuration()
    dummy_users = providers.Factory(
        ListDummyUsers,
        sth='STH@',
    )
