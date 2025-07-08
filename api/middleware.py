class NgrokSkipWarningMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        skip_warning = request.headers.get('ngrok-skip-browser-warning')
        if skip_warning == 'true':
            print("Ngrok skip browser warning header detected!")
            # ทำอะไรเพิ่มเติมได้ เช่น ข้ามบาง middleware หรือ log
        response = self.get_response(request)
        return response
