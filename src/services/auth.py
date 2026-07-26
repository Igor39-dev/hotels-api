from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from src.config import settings
from src.exceptions import (
    EmailNotRegisteredException,
    IncorrectPasswordException,
    IncorrectTokenException,
    ObjectAlreadyExistsException,
    UserAlreadyExistsException
)
from src.services.base import BaseServie
from src.shemas.users import UserAdd, UserRequestAdd


class AuthService(BaseServie):
    password_hash = PasswordHash.recommended()

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAdd):
            hashed_password = AuthService().hash_password(data.password)
            new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
            try:
                await self.db.users.add(new_user_data)
                await self.db.commit()
            except ObjectAlreadyExistsException as ex:
                raise UserAlreadyExistsException from ex

    async def login_user(self, data: UserRequestAdd):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
