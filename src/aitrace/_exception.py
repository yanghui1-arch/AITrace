
class APIKeyException(Exception):
    def __init__(self, error_msg: str, url: str | None =None):
        super().__init__(error_msg)
        self.url = url
    
    def __str__(self):
        error_msg = super().__str__()
        if self.url:
            return error_msg + f"(Pass url: {self.url})"
        return error_msg + f"(Pass url: None)"