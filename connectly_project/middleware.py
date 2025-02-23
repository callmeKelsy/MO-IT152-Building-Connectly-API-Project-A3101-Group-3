from django.utils.deprecation import MiddlewareMixin
from connectly_project.singletons.logger_singleton import LoggerSingleton

logger = LoggerSingleton().get_logger()

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(f"Incoming request: {request.method} {request.path}")

    def process_response(self, request, response):
        logger.info(f"Outgoing response: {response.status_code} for {request.method} {request.path}")
        return response

    def process_exception(self, request, exception):
        logger.error(f"Unhandled exception: {str(exception)}", exc_info=True)
