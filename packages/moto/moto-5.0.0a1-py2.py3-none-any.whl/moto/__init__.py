from typing import TYPE_CHECKING, Callable, Dict, Optional, TypeVar, Union, overload

from moto import settings
from moto.core.models import MockAWS, ProxyModeMockAWS, ServerModeMockAWS

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    P = ParamSpec("P")

T = TypeVar("T")


@overload
def mock_aws(func: "Callable[P, T]") -> "Callable[P, T]":
    ...


@overload
def mock_aws(
    func: None = None, config: Optional[Dict[str, Dict[str, bool]]] = None
) -> "MockAWS":
    ...


def mock_aws(
    func: "Optional[Callable[P, T]]" = None,
    config: Optional[Dict[str, Dict[str, bool]]] = None,
) -> Union["MockAWS", "Callable[P, T]"]:
    clss = (
        ServerModeMockAWS
        if settings.TEST_SERVER_MODE
        else (ProxyModeMockAWS if settings.test_proxy_mode() else MockAWS)
    )
    if func is not None:
        return clss().__call__(func=func)
    else:
        return clss(config)


__title__ = "moto"
__version__ = "5.0.0alpha1"


try:
    # Need to monkey-patch botocore requests back to underlying urllib3 classes
    from botocore.awsrequest import (  # type: ignore[attr-defined]
        HTTPConnection,
        HTTPConnectionPool,
        HTTPSConnectionPool,
        VerifiedHTTPSConnection,
    )
except ImportError:
    pass
else:
    HTTPSConnectionPool.ConnectionCls = VerifiedHTTPSConnection
    HTTPConnectionPool.ConnectionCls = HTTPConnection
