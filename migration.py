import json
from hello import app, db, Article


app.app_context().push()


with open('fdb/lastindex.txt', 'r') as f:
    lastindex=int(f.read())
for x in range(lastindex, 0, -1):
    with open('fdb/' + str(x) + '.txt', 'r') as f:
        d=json.loads(f.read())
    a = Article()
    a.author = d['author']
    a.subject = d['subject']
    a.content = d['content']
    a.is_deleted = d.get('is_deleted', False)
    db.session.add(a)

db.session.commit()
