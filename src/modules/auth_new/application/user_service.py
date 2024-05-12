from modules.auth_new.domain.user_repo import IUserRepo
from src.modules.auth_new.application.dto import UserInputDto, UserOutputDto, UserAuthInputDto, TokenOutputDto
from src.modules.auth_new.domain.errors import BadCredentials, UserNotFound
from src.modules.auth_new.domain.user import User


class AuthenticationService:
    def __init__(
            self,
            user_repository: IUserRepo,
            secret_key: str,
            algorithm: str,
    ):
        self._user_repository = user_repository
        self._secret_key = secret_key
        self._algorithm = algorithm

    async def create(self, input_dto: UserInputDto) -> UserOutputDto:
        user = User.create(
            username=input_dto.username,
            password=input_dto.password,
            email=input_dto.email,
            first_name=input_dto.first_name,
            last_name=input_dto.last_name
        )
        await self._user_repository.asave(user)

        return UserOutputDto(**user.snapshot)

    async def authenticate(
            self,
            credentials: UserAuthInputDto
    ) -> TokenOutputDto | BadCredentials | UserNotFound:

        user: User = await self._user_repository.aget_first_from_filter(
            username=credentials.username
        )
        if not user:
            raise UserNotFound("User not found.")

        if user.correct_password(credentials.password):
            return TokenOutputDto(
                api_token=user.create_token(
                    secret_key=self._secret_key,
                    algorithm=self._algorithm
                ),
                user_id=user.id
            )

        raise BadCredentials("Incorrect password.")
