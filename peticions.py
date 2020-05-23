import requests

def
if __name__ == __main__ :
    args = { 'nom1' : 'guifre', 'nom2' : 'victor' }
    res = requests.get("https://postman-echo.com/get",params=args)

    print(res.json()['args']['nom1'])