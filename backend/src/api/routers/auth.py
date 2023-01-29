from dependency_injector.wiring import inject
from fastapi import APIRouter, Response, HTTPException, status, Depends
from fastapi.security import HTTPBearer

from api.shared import dependency, bearer_auth
from config.container_ioc import Container
from modules.auth.app.usecases.dtos import UserAuthInputDto, TokenOutputDto, UserCreateInputDto
from src.modules.auth.app.services.authentication import AuthService
from src.modules.auth.app.usecases.command import UserCommand
from src.modules.auth.domain.exceptions import BadCredentials, UserNotFound, UserAlreadyExists

router = APIRouter(tags=['auth'])


@router.post('/login')
@inject
def login(credentials: UserAuthInputDto,
          auth_service: AuthService = dependency(Container.auth_service)
          ) -> TokenOutputDto | HTTPException:
    try:
        return auth_service.authenticate(credentials)
    except (UserNotFound, BadCredentials) as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/create_account')
@inject
def create_account(user: UserCreateInputDto,
                   command: UserCommand = dependency(Container.user_command)
                   ) -> HTTPException | Response:
    try:
        command.create(user)
        return Response(status_code=status.HTTP_201_CREATED)
    except UserAlreadyExists as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/test')
def test_get_user(user: HTTPBearer = Depends(bearer_auth)):
    print(user)
    return 'sth'
