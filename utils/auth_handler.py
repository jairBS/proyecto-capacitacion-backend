from fastapi import Depends

from fastapi.security import HTTPBearer

from fastapi.security.http import HTTPAuthorizationCredentials

from fastapi import HTTPException

from jose import jwt, JWTError

from dotenv import load_dotenv

import os


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"


security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )