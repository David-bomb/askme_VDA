def application(environ, start_response):
    # Обработка GET-параметров
    get_params = environ.get('QUERY_STRING', '')

    # Обработка POST-параметров
    post_data = {}
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    if request_body_size > 0:
        request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
        post_data = dict(param.split('=') for param in request_body.split('&') if '=' in param)

    # Формирование ответа
    status = '200 OK'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    response = [
        f"GET-параметры: {get_params}\n".encode('utf-8'),
        f"POST-данные: {post_data}".encode('utf-8')
    ]

    start_response(status, headers)
    return response