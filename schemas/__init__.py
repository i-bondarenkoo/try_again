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
)

ResponseUserWithRelationship.model_rebuild()
ResponseTaskWithUser.model_rebuild()
