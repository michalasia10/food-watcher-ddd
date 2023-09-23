from .base import BaseModelView
from .chat import router as ChatRouter, ChannelsViewSet
from .consumption import router as ConsumptionRouter
from .products import ProductViewSet
from .recipe import RecipeViewSet, RecipeProductViewSet
from .users import UserViewSet
