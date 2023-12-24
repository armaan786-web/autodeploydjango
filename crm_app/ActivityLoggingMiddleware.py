from .models import ActivityLog

class ActivityLoggingMiddleware:
    EXCLUDED_USER_TYPES = ["1"]
    EXCLUDED_URL_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"]
    

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        
        if user.is_authenticated and user.user_type not in self.EXCLUDED_USER_TYPES:
            
            if (
                not any(request.path.endswith(extension) for extension in self.EXCLUDED_URL_EXTENSIONS)
                and request.path not in self.EXCLUDED_URLS
            ):
                
                ActivityLog.objects.create(
                    user=user,
                    action=f"{request.path}",
                    details=request.method,
                )

        response = self.get_response(request)
        return response
