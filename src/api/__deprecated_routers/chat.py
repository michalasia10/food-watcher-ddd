# from asyncio import AbstractEventLoop
#
# from dependency_injector.wiring import inject
# from fastapi import APIRouter, Depends, HTTPException
# from starlette.websockets import WebSocket
#
# from api.routers.base import BaseModelView
# from api.shared import bearer_auth
# from api.shared import dependency
# from config.di import Container
# from modules.chat.domain.value_objects import ChanelId
# from src.api.shared.loop import get_event_loop
# from src.modules.chat.app.dtos import ChannelInputDto, ChannelOutputDto, WebSockMessage
# from src.modules.chat.app.repository.messages import MessageCompositeRepository
# from src.modules.chat.facade import WebSocketFacade, NotificationPublisherFacade
# from src.modules.chat.infra.services.websockets import ConnectionManager
#
# router = APIRouter(prefix="/chat", tags=["chat"])
#
# conn_manager = ConnectionManager()
#
#
# class ChannelsViewSet(BaseModelView[ChannelInputDto, ChannelOutputDto]):
#     prefix = "/chanel"
#     tag = "chanel"
#     crud_methods = ("create", "list", "read")
#
#     @inject
#     def __init__(
#         self,
#         query_service=dependency(Container.chanel_query),
#         command_service=dependency(Container.chanel_command),
#     ):
#         super(ChannelsViewSet, self).__init__(
#             query_service=query_service,
#             command_service=command_service,
#             basic_create_dto=ChannelInputDto,
#             basic_output_dto=ChannelOutputDto,
#         )
#
#
# @router.post("/send_message/{channel_id}/")
# @inject
# async def send_message(
#     channel_id: ChanelId,
#     message: WebSockMessage,
#     user=Depends(bearer_auth),
#     loop: AbstractEventLoop = Depends(get_event_loop),
#     rabitmq_url: str = dependency(Container.rabitmq_url),
#     message_repository: MessageCompositeRepository = dependency(
#         Container.composite_message_repository
#     ),
# ):
#     publisher = NotificationPublisherFacade(
#         channel_id, message, rabitmq_url, message_repository, loop, user
#     )
#     try:
#         await publisher.publish()
#         return "Message published"
#     except Exception as e:
#         raise HTTPException(
#             status_code=400, detail=f"Error while publishing message: {e}"
#         )
#
#
# @router.websocket("/ws/{channel_id}/")
# @inject
# async def chat(
#     websocket: WebSocket,
#     channel_id: ChanelId,
#     loop: AbstractEventLoop = Depends(get_event_loop),
#     rabitmq_url=dependency(Container.rabitmq_url),
#     composite_message_repository: MessageCompositeRepository = dependency(
#         Container.composite_message_repository
#     ),
# ):
#     facade = WebSocketFacade(
#         websocket,
#         channel_id,
#         conn_manager,
#         loop,
#         rabitmq_url,
#         composite_message_repository,
#     )
#     await facade.run()
