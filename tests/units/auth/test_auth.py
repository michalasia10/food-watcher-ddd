from src.modules.auth_new.domain.user import User, TypeEnum, StatusEnum


def test_create_user_hash_pswd():
    # given
    password = "test_password"
    user = User.create(
        email="test@emai.com",
        password=password,
        username="test",
        first_name="test",
        last_name="test",
        status=StatusEnum.ACTIVE.value,
        type=TypeEnum.USER.value,
    )
    # then
    assert user.password != password


def test_create_token():
    # given
    secret = "test"
    algorithm = "HS256"
    user = User.create(
        email="test",
        password="test",
        username="test",
        first_name="test",
        last_name="test",
        status=StatusEnum.ACTIVE.value,
        type=TypeEnum.USER.value,
    )

    # when
    token = user.create_token(secret_key=secret, algorithm=algorithm)

    # then
    assert token is not None
    assert isinstance(token, (str, bytes))


def test_correct_password():
    # given
    password = "test_password"
    user = User.create(
        email="test@email.com",
        password=password,
        username="test",
        first_name="test",
        last_name="test",
        status=StatusEnum.ACTIVE.value,
        type=TypeEnum.USER.value,
    )
    # when / then
    assert user.correct_password(password)
    assert not user.correct_password("wrong_password")
