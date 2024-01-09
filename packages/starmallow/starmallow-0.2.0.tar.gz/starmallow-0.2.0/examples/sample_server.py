from dataclasses import asdict
from typing import Annotated, Optional, Iterable

import aiofiles.tempfile
import marshmallow.fields as mf
import orjson
from marshmallow.validate import Range
from marshmallow_dataclass import dataclass as ma_dataclass
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette_context import middleware, plugins

from starmallow.applications import StarMallow
from starmallow.params import Body, Cookie, Header, Path, Query, Security, ResolvedParam
from starmallow.security.http import HTTPBearer, HTTPAuthorizationCredentials
from starmallow.security.oauth2 import OAuth2PasswordBearer

from starlette.requests import Request, HTTPException
from starmallow.security.http import HTTPBearer, HTTPAuthorizationCredentials
from typing import Mapping

from techlock.common.api.auth.claim import ClaimSpec
from techlock.common.api.auth.jwt import JWTDecoder
from techlock.common.api.auth.user_loader import JWTUserLoader, AuthInfo
from techlock.common.api.auth.utils import SYSTEM_TENANT_ID
from techlock.common.orm.sqlalchemy.base import BaseModel


app = StarMallow(
    title="My API",
    version="1.0.0",
    middleware=[
        # Order matters!
        Middleware(GZipMiddleware, minimum_size=500),
        Middleware(
            middleware.ContextMiddleware,
            plugins=(
                plugins.RequestIdPlugin(),
                plugins.CorrelationIdPlugin(),
            ),
        ),
    ],
)

jwks_urls = ['http://172.16.40.238:6081/.well-known/jwks.json']
app.ndr_audience = None
app.ndr_jwt_decoder = JWTDecoder(
    jwks_urls,
    # audience='https://ndr.techlockinc.com/',
    # issuer='https://techlock.auth0.com/',
)


class NDR_JWTBearer(HTTPBearer):

    def __init__(
        self,
        access_models: Mapping[ClaimSpec | BaseModel, str | Iterable[str]],
        default_tenants: str | list[str] = SYSTEM_TENANT_ID,
        replace_wildcard_tenants: bool = True,
        # Bool if exact match for all access models. otherwise flag per access model
        exact_match_only: bool | Mapping[ClaimSpec | BaseModel, bool] = False,
        # All flags are required! (AND operation)
        required_flags: str | list[str] = None,
        auto_error: bool = True,
    ):
        super().__init__(auto_error=auto_error)

        self.jwt_extractor = JWTUserLoader(
            access_models=access_models,
            default_tenants=default_tenants,
            replace_wildcard_tenants=replace_wildcard_tenants,
            exact_match_only=exact_match_only,
            required_flags=required_flags,
        )

    async def __call__(self, request: Request) -> AuthInfo:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            jwt_decoder: JWTDecoder = request.app.ndr_jwt_decoder
            jwt_data = await jwt_decoder.decode(credentials.credentials)
            return self.jwt_extractor.get_user_from_jwt(jwt_data, request.headers, getattr(request.app, 'ndr_audience'))

        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


jwt_scheme = HTTPBearer()
ndr_schema = NDR_JWTBearer({ClaimSpec(actions=['read'], resource_name='foo'): 'read'})
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


@ma_dataclass
class CreateRequest:
    my_string: str
    my_int: int = 5


@ma_dataclass
class CreateResponse:
    my_string: str


@app.get('/oauth_test')
def oauth_test(
    token: str = ResolvedParam(oauth2_scheme),
):
    print(token)


@app.get('/auth_test')
def auth_test(
    token: HTTPAuthorizationCredentials = ResolvedParam(jwt_scheme),
):
    print(token)


@app.get('/ndr_auth_test')
def auth_test(
    auth_info: AuthInfo = ResolvedParam(ndr_schema),
):
    print(auth_info)


@app.post('/test')
async def test(
    create_request: CreateRequest,
    limit: Annotated[int, Query()],
    offset: int = 0,
    offset2: int = Query(0, model=mf.Integer(validate=[Range(min=0, max=50)])),
    my_string: str = Body('foobar'),
    email: str = Body(..., model=mf.Email()),
    foobar: str = Header(...),
    preference: Optional[str] = Cookie(...),
) -> CreateResponse:
    print(create_request)
    print(limit)
    print(offset)
    print(offset2)
    print(foobar)
    print(my_string)
    print(email)
    print(preference)

    return create_request


# Test path parameters
@app.get('/test/{id}')
def test_id(
    id: int = Path(...),
) -> CreateResponse:
    print(id)

    return None


# Test basic JSON request body and JSON response body
@app.put('/test2')
def test2(create_request: CreateRequest) -> CreateResponse:
    print(create_request)

    return asdict(create_request)


# Test basic JSON request body and JSON response body with request defaults
@app.patch('/test3')
def test3(
    create_request: CreateRequest = CreateRequest(my_string='foobar', my_int=10),
) -> CreateResponse:
    print(create_request)

    return asdict(create_request)


# Test request query from schema where the entire schema is required
@app.get('/test4')
def test4(
    create_request: CreateRequest = Query(...),
) -> CreateResponse:
    print(create_request)

    return asdict(create_request)


# Test request query from schema where the entire schema has a default
@app.get('/test5')
def test5(
    create_request: CreateRequest = Query(CreateRequest(my_string='default_string', my_int=101)),
) -> CreateResponse:
    print(create_request)

    return asdict(create_request)


# Test basic JSON request body and JSON response body
@app.put('/tmp_file')
async def put_tmp_file(create_request: CreateRequest) -> CreateResponse:
    async with aiofiles.tempfile.TemporaryFile('wb') as f:
        await f.write(orjson.dumps(create_request))

    return asdict(create_request)
