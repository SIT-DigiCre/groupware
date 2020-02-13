import multiprocessing

bind = '0.0.0.0:8000'
accesslog = './log/gunicorn/access.log'
errorlog = './log/gunicorn/error.log'
capture_output = True
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 1000
max_requests_jitter = 100
