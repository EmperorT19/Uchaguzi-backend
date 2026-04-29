class CorsMiddleware:
    """
    Production Security Layer:
    Handles Cross-Origin Resource Sharing (CORS) to allow the Netlify frontend 
    to securely communicate with the Railway backend.
    This bypasses django-cors-headers for faster processing.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Handle preflight OPTIONS request immediately
        if request.method == 'OPTIONS':
            response = self._build_options_response()
            self._add_cors_headers(response)
            return response

        response = self.get_response(request)
        self._add_cors_headers(response)
        return response

    def _add_cors_headers(self, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
        response['Access-Control-Max-Age'] = '86400'

    def _build_options_response(self):
        from django.http import HttpResponse
        return HttpResponse(status=200)
