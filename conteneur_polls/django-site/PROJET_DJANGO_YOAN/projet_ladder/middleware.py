class SetIsApiFlagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifie si l'URL contient "api"
        if request.path.startswith('/api/'):
            request.is_api = True
        else:
            request.is_api = False

        response = self.get_response(request)
        return response
# distinction navbar api -front