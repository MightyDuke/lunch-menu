from typing import Annotated, AsyncIterable
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.sse import EventSourceResponse
from lunch_menu.models.voting import VoteRequest, VoteResponse
from lunch_menu.services.user import UserService
from lunch_menu.services.voting import VotingService

security = HTTPBearer()
router = APIRouter(tags = ["Voting"])

@router.put("/vote", name = "Vote", description = "Cast a vote", status_code = status.HTTP_204_NO_CONTENT)
async def vote(
    body: VoteRequest,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    voting_service: Annotated[VotingService, Depends()],
    session_service: Annotated[UserService, Depends()]
):
    user_id = await session_service.get_session(authorization.credentials)
    await voting_service.vote(user_id, body.date, body.establishment, body.item)


@router.get("/vote/stream", name = "Vote Stream", description = "SSE stream of votes", response_class = EventSourceResponse)
async def vote_stream(
    voting_service: Annotated[VotingService, Depends()]
) -> AsyncIterable[VoteResponse]:
    async for votes in voting_service.listen():
        yield VoteResponse(votes)