from dataclasses import dataclass
from typing import AnyStr, Dict, Any

from nicegui import ui
from nicegui.awaitable_response import AwaitableResponse


@dataclass
class KeycloakConfig:
    url: AnyStr
    realm: AnyStr
    client_id: AnyStr


class Keycloak(ui.element, component='keycloak.js'):
    config: KeycloakConfig = None
    require_login: bool = None

    def __init__(self,
                 config: KeycloakConfig,
                 js_source: AnyStr = '/static/keycloak.js',
                 init_options: Dict = None):
        super().__init__()

        ui.add_head_html(f'<script src="{js_source}"></script>')

        props: Dict[str, Any] = self._props
        props['url'] = config.url
        props['realm'] = config.realm
        props['clientId'] = config.client_id

        props['initOptions'] = init_options if init_options else {}

    def token(self) -> AwaitableResponse:
        return self.run_method('token')

    def refresh_token(self) -> AwaitableResponse:
        return self.run_method('refreshToken')

    def authenticated(self) -> AwaitableResponse:
        return self.run_method('authenticated')

    def login(self, options=None) -> AwaitableResponse:
        return self.run_method('login', options if options else {})

    def logout(self, options=None) -> AwaitableResponse:
        return self.run_method('logout', options if options else {})
