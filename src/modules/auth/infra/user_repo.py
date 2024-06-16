from src.core.infra.tortoiserepo import TortoiseRepo
from src.modules.auth.domain import user
from src.modules.auth.infra import model


class UserTortoiseRepo(TortoiseRepo[model.User, user.User]):
    model = model.User
    entity = user.User
