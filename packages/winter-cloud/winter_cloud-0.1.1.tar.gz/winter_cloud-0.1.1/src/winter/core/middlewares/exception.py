from winter.common import exception


class ExceptionMixin:

    def exception_handlers(self):
        """ 注册异常处理器 """
        self.app.add_exception_handler(exception.RequestValidationError, exception.request_validation_exception_handler)
        self.app.add_exception_handler(exception.ValidationError, exception.request_validation_exception_handler)
        self.app.add_exception_handler(exception.HTTPException, exception.error_exception_handler)
        self.app.add_exception_handler(exception.NotFoundException, exception.error_exception_handler)
        self.app.add_exception_handler(exception.ExistException, exception.error_exception_handler)
        self.app.add_exception_handler(Exception, exception.error_exception_handler)
