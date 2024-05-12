from src.core_new.infra.tortoiserepo import TortoiseRepo
from src.modules.auth_new.domain import user
from src.modules.auth_new.infra import model


class UserTortoiseRepo(TortoiseRepo[model.User, user.User]):
    model = model.User
    entity = user.User
