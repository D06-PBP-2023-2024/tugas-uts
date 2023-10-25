import requests
import json
c = 0
d = []
url = "https://gutendex.com/books?bookshelves=Children's%20Literature"
while c < 100:
    response = requests.get(url)
    data = response.json()
    for book in data['results']:
        d.append(book)
        print(book['title'])
        c += 1
    url = data['next']
    print(f"ZCZC {c}/100 >>> {url}")

with open('data.json', 'w') as f:
    json.dump(d, f, indent=4)