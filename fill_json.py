import requests
import json
c = 0
d = []
url = "http://gutendex.com/books/?bookshelves=Children%27s%20Myths,%20Fairy%20Tales"
while c < 100:
    response = requests.get(url)
    data = response.json()
    for book in data['results']:
        d.append(book)
        print(book['title'])
        c += 1
        if c >= 100:
            break
    url = data['next']
    print(f"ZCZC {c}/100 >>> {url}")

with open('data.json', 'w') as f:
    json.dump(d, f, indent=4)