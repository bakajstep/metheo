import time

# Dictionary to track the number of requests per IP address
rate_limiters = {}


def rate_limit(max_requests, window_seconds):
    def decorator(handler):
        def limit(request, *args, **kwargs):
            client_ip = request.client_addr[0]
            current_time = time.time()
            print(client_ip)
            print(current_time)

            if client_ip not in rate_limiters:
                rate_limiters[client_ip] = {'count': 1, 'time': current_time}
            else:
                if current_time - rate_limiters[client_ip]['time'] < window_seconds:
                    rate_limiters[client_ip]['count'] += 1
                    if rate_limiters[client_ip]['count'] > max_requests:
                        return {'error': 'Rate limit exceeded'}, 429
                else:
                    rate_limiters[client_ip] = {'count': 1, 'time': current_time}

            return handler(request, *args, **kwargs)

        return limit

    return decorator
