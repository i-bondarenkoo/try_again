from schemas.task import (
    CreateTask,
    ResponseTask,
    PathUpdateTask,
    ShortResponseTask,
    ResponseTaskWithUser,
)
from schemas.user import (
    CreateUser,
    ResponseUser,
    UpdateUser,
    ResponseUserWithRelationship,
    ResponseShortUser,
    LoginUser,
    RegisterUser,
)
from schemas.token import TokenResponse

ResponseUserWithRelationship.model_rebuild()
ResponseTaskWithUser.model_rebuild()
