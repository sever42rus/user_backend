from auth_lib.fastapi import NotConfirmedUserAuthDep
from auth_lib.fastapi import TempUserAuthDep
from fastapi import APIRouter
from fastapi import Body
from fastapi import status

from domains.update_action.models import UpdateActionCompleteModel
from domains.update_action.models import UpdateActionRequestModel
from domains.users.models import ChangePasswordModel
from domains.users.models import TokenPairModel
from domains.users.models import UserLoginCredentialsModel
from domains.users.models import UserRegisterCredentialsModel
from use_cases.confirm_email import confirm_email_use_cases
from use_cases.password_reset import password_reset_use_cases
from use_cases.temp_users import temp_user_use_case
from use_cases.update_action_complete import update_action_use_case
from use_cases.users import user_use_case

router = APIRouter()


@router.get("/get-access", status_code=status.HTTP_200_OK)
async def get_access(auth: TempUserAuthDep) -> str:
    """
    Получить уровень доступа для временного пользователя.
    Возвращает строку с уровнем доступа.
    """
    return auth.access_level


@router.post("/temp-token", status_code=status.HTTP_200_OK)
async def temp_token() -> TokenPairModel:
    """
    Авторизовать временного пользователя и вернуть пару токенов.
    """
    return await temp_user_use_case.login_temp_user()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(auth: TempUserAuthDep, credentials: UserRegisterCredentialsModel) -> TokenPairModel:
    """
    Создать нового пользователя, используя временного пользователя для аутентификации.
    Возвращает пару токенов для созданного пользователя.
    """
    return await user_use_case.create(auth=auth, credentials=credentials)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: UserLoginCredentialsModel) -> TokenPairModel:
    """
    Вход пользователя в систему по предоставленным учетным данным.
    Возвращает пару токенов.
    """
    return await user_use_case.login(credentials=credentials)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token: str = Body(..., embed=True)) -> TokenPairModel:
    """
    Обновить пару токенов, используя refresh-токен.
    Возвращает новую пару токенов.
    """
    return await user_use_case.refresh(refresh_token=refresh_token)


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(auth: NotConfirmedUserAuthDep, change_password: ChangePasswordModel) -> bool:
    """
    Изменить пароль пользователя.
    Требуется аутентификация с неподтвержденным пользователем.
    Возвращает True, если пароль успешно изменен.
    """
    return await user_use_case.change_password(access_token_payload=auth, change_password=change_password)


@router.post("/confirm-email-request", status_code=status.HTTP_200_OK)
async def confirm_email_request(auth: NotConfirmedUserAuthDep) -> UpdateActionRequestModel:
    """
    Запрос на подтверждение email.
    Требуется аутентификация с неподтвержденным пользователем.
    """
    return await confirm_email_use_cases.confirm_email_request(auth=auth)


@router.post("/update-action-complete", status_code=status.HTTP_200_OK)
async def update_action_complete(data: UpdateActionCompleteModel) -> bool:
    """
    Завершить процесс подтверждения email.
    Требуется аутентификация с неподтвержденным пользователем.
    """
    return await update_action_use_case.verify_and_complete(update_action_data=data)


@router.post("/password-reset-request", status_code=status.HTTP_200_OK)
async def password_reset_request(credentials: UserRegisterCredentialsModel) -> UpdateActionRequestModel:
    """
    Запрос на сброс пароля для обычного пользователя.
    Требуется аутентификация с обычным пользователем.
    """
    _, update_action = await password_reset_use_cases.password_reset_request(credentials=credentials)
    return update_action
