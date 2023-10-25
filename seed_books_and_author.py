import json

db_data = []
def find_author(name):
    for d in db_data:
        if d['model'] == 'main.author':
            if d['fields']['name'] == name:
                return d['pk']
    return -1

def main():
    with open('data.json', 'r') as f:
        data = json.load(f)
        for i, book in enumerate(data):
            # check if author exists
            for author in book['authors']:
                a_id = find_author(author["name"]) 
                if a_id == -1:
                    a_id = len(db_data) + 1
                    author_obj = {
                        "model": "main.author",
                        "pk": a_id,
                        "fields": {
                            "name": author["name"]
                        }
                    }
                    db_data.append(author_obj)
                book_obj = {
                    "model": "main.book",
                    "pk": len(db_data) + 1,
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