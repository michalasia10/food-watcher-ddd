from fastapi import APIRouter
from api.shared import dependency

router = APIRouter(tags=['auth'])


@router.post('/login')
def login():
    pass


@router.post('/logout')
def logout():
    pass

@router.get('/dummy')
def dummy():
    return 'dummy'