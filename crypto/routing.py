from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import core.routing as core_routing

application = ProtocolTypeRouter({
	'websocket': AuthMiddlewareStack(
		URLRouter(
			core_routing.websocket_patterns
		)
	)
})
