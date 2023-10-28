import json

db_data = []
book_cnt = 0
author_cnt = 0
def find_author(name):
    for d in db_data:
        if d['model'] == 'main.author':
            if d['fields']['name'] == name:
                return d['pk']
    return -1

def main():
    global author_cnt, book_cnt
    with open('data.json', 'r') as f:
        data = json.load(f)
        for i, book in enumerate(data):
            # check if author exists
            for author in book['authors']:
                a_id = find_author(author["name"]) 
                if a_id == -1:
                    author_cnt += 1
                    author_obj = {
                        "model": "main.author",
                        "pk": author_cnt,
                        "fields": {
                            "name": author["name"]
                        }
                    }
                    a_id = author_cnt
                    db_data.append(author_obj)
                book_cnt += 1
                book_obj = {
                    "model": "main.book",
                    "pk": book_cnt,
                    "fields": {
                        "title": book['title'],
                        "author": a_id,
                        "cover_url": book['formats']["image/jpeg"],
                        "download_count": book['download_count'],
                        "content": book['formats'].get("text/html", None)
                    }
                }
                db_data.append(book_obj)
                print(f"{i}/{len(data)}")
    with open('db.json', 'w') as f:
        json.dump(db_data, f, indent=4)

if __name__ == "__main__":
    main()