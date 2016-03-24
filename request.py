import requests
import Models
import gevent.monkey
import gevent

schedule_tasks = Models.Schedule.select()
gevent.monkey.patch_socket()


def do_request(task):
    gevent.sleep(10)
    response = requests.get(task.url)
    response_time = str(response.elapsed)[:11]
    content_len = len(response.content)
    aRequest = Models.Request(url_id=task.id, status_code=response.status_code,
                              response_time=response_time, content_len=content_len)
    # server_name = response.headers['servername_intern']
    # server_name = response.cookies['SRV']

    aRequest.save()
    print 'url ' + str(task.url) + ' -- time: ' + str(response_time)
    return

if __name__ == '__main__':
    threads = {}
    while True:
        threads = []
        for task in schedule_tasks:
            threads.append(gevent.spawn(do_request, task))
        gevent.joinall(threads)
