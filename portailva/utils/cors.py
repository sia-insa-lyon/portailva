from django.utils.deprecation import MiddlewareMixin


class CorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith("/api/v1/directory/") and request.method == "GET":
            response["Access-Control-Allow-Origin"] = "*"
        return response
