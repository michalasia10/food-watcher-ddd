from src.core.infra.repo.tortoiserepo import TortoiseRepo
from src.modules.auth.domain.entity import user as entity
from src.modules.auth.infra.model import user as model


class UserTortoiseRepo(TortoiseRepo[model.User, entity.User]):
    model = model.User
    entity = entity.User
