import json
import urllib.request
import urllib.error


def get(path):
    try:
        resp = urllib.request.urlopen(path, timeout=5)
        print('GET', path, '->', resp.status)
        print(resp.read().decode())
    except Exception as e:
        print('GET', path, 'ERROR', e)


def post(payload):
    url = 'http://127.0.0.1:5000/api/coupons/calculate'
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type':'application/json'}, method='POST')
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        print('POST', payload, '->', resp.status)
        print(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode()
        except Exception:
            body = '<no body>'
        print('POST', payload, '->', e.code)
        print(body)
    except Exception as e:
        print('POST', payload, 'ERROR', e)


if __name__ == '__main__':
    get('http://127.0.0.1:5000/health')
    post({'original_price':100,'discount_rate':0.8})
    post({'original_price':100,'discount_rate':0})
    post({'original_price':100})
    post({'original_price':100,'discount_rate':-0.1})
    post({'original_price':'a','discount_rate':'b'})
