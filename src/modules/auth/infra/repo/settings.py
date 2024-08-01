from src.core.infra.repo.tortoiserepo import TortoiseRepo
from src.modules.auth.domain.entity import settings as entity
from src.modules.auth.infra.model import settings as model


class MacroTortoiseRepo(TortoiseRepo[model.Macro, entity.Macro]):
    model = model.Macro
    entity = entity.Macro


class UserSettingsTortoiseRepo(TortoiseRepo[model.UserSettings, entity.UserSettings]):
    model = model.UserSettings
    entity = entity.UserSettings
