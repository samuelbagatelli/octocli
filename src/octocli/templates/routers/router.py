from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..schemas.current_user import CurrentUserSchema
from ..schemas.{{ tablename }} import {{ classname }}CreateSchema, {{ classname }}UpdateSchema, {{ classname }}ViewSchema
from ..services import {{ classname }}Service
from ..settings import get_session
from ..utils import ExceptionHandler, PermissionChecker

MODEL = "{{ tablename }}"

router = APIRouter(prefix=f"/{MODEL}", tags=[MODEL.title()])


# ——————————————————————————————————CREATE—————————————————————————————————————
create_checker = PermissionChecker(["{{ tablename }}_create"])
@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary=f"Create a new {{ classname }}",
)
def {{ tablename }}_create(
    payload: {{ classname }}CreateSchema,
    current_user: Annotated[CurrentUserSchema, Depends(create_checker)],
    session: Annotated[Session, Depends(get_session)],
):
    try:
        service = {{ classname }}Service(session, current_user)
        response = service.create(payload.model_dump())

        return response
    except Exception as e:
        session.rollback()
        raise ExceptionHandler(e)


# ———————————————————————————————————READ——————————————————————————————————————
view_checker = PermissionChecker(["{{ tablename }}_view"])
@router.get(
    "/view/{{{ tablename }}_id}",
    response_model={{ classname }}ViewSchema,
    summary="Information about specific {{ classname }}",
)
def {{ tablename }}_view(
    {{ tablename }}_id: int,
    current_user: Annotated[CurrentUserSchema, Depends(view_checker)],
    session: Annotated[Session, Depends(get_session)],
):
    try:
        service = {{ classname }}Service(session, current_user)
        reponse = service.view({{ tablename }}_id)

        return response
    except Exception as e:
        raise ExceptionHandler(e)


# ——————————————————————————————————UPDATE—————————————————————————————————————
update_checker = PermissionChecker(["{{ tablename }}_update"])
@router.patch(
    "/update/{{{ tablename }}_id}",
    summary="Update info about specific {{ classname }}",
)
def {{ tablename }}_update(
    {{ tablename }}_id: int,
    payload: {{ classname }}UpdateSchema,
    current_user: Annotated[CurrentUserSchema, Depends(update_checker)],
    session: Annotated[Session, Depends(get_session)],
):
    try:
        service = {{ classname }}Service(session, current_user)
        response = service.update(
            {{ tablename }}_id, 
            payload.model_dump(exclude_none=True),
        )

        return response
    except Exception as e:
        session.rollback()
        raise ExceptionHandler(e)


# ——————————————————————————————————DELETE—————————————————————————————————————
delete_checker = PermissionChecker(["{{ tablename }}_delete"])
@router.delete(
    "/delete/{{{ tablename }}_id}",
    summary="Soft delete a {{ classname }}",
)
def {{ tablename }}_delete(
    {{ tablename }}_id: int,
    current_user: Annotated[CurrentUserSchema, Depends(delete_checker)],
    session: Annotated[Session, Depends(get_session)],
):
    try:
        service = {{ classname }}Service(session, current_user)
        response = service.delete({{ tablename }}_id)

        return response
    except Exception as e:
        session.rollback()
        raise ExceptionHandler(e)


# ———————————————————————————————————LIST——————————————————————————————————————
list_checker = PermissionChecker(["{{ tablename }}_list"])
@router.get(
    "/list",
    summary="List {{ classname }} records"
)
def {{ tablename }}_list(
    current_user: Annotated[CurrentUserSchema, Depends(list_checker)],
    session: Annotated[Session, Depends(get_session)],
    page: int = 0,
    limit: int = 10,
    deleted: bool = False,
    filter_text: str | None = None,
    {{ tablename }}_ids: list[int] = Query(default=None),
):
    try:
        service = {{ classname }}Service(session, current_user)
        response = service.list(
            page * limit,
            limit,
            deleted,
            filter_text,
            {{ tablename }}_ids
        )

        return response
    except Exception as e:
        raise ExceptionHandler(e)
