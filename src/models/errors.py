from pydantic import BaseModel

#ALL ERRORS
class ErrorDetail(BaseModel):
    code: str
    message: str



class ErrorResponse(BaseModel):
    error: ErrorDetail

    @property
    def code(self):
        return self.error.code

    @property
    def message(self):
        return self.error.message


#HOW WILL USE IN TESTS
#assert error.code
#assert error.message