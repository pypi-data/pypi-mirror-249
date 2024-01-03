class BaseMiddleware:
    def __init__(self) -> None:
        try:
            if callable(self):
                self.apply = callable

            elif self.enter and self.exit:

    async def enter(self, )