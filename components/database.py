import logging
from models.arxiv import Article as ArxivArticle

log = logging.getLogger(__name__)

def exists_arxiv(cur, article_id):
    cur.execute(
        "select id from ARXIV \
            where id = %s",
        (article_id,))
    return cur.fetchone() is not None

def insert_arxiv(cur, article):
    aid = article.id
    published = article.published
    title = article.title
    authors = "; ".join(article.authors)
    summary = article.summary

    cur.execute(
        "insert into ARXIV (id, published, title, authors, summary) \
            values (%s, %s, %s, %s, %s) \
            on conflict do nothing",
        (aid, published, title, authors, summary))

def get_arxiv_latest(cur, limit=10):
    cur.execute(
        "select * from ARXIV \
            order by published desc \
            limit %s",
            (limit,))
    rows = cur.fetchall()

    articles = []
    for row in rows:
        try:
            authors = row[3].split('; ')
            article = ArxivArticle(
                row[0],
                row[1],
                row[2],
                authors,
                row[4])
            articles.append(article)
        except Exception as e:
            log.warning(e)

    return articles

def get_arxiv_after(cur, aid, limit=10):
    cur.execute(
        "select * from ARXIV \
            where published < (\
                select published from ARXIV \
                    where id = %s) \
            order by published desc \
            limit %s",
            (aid,limit))
    rows = cur.fetchall()

    articles = []
    for row in rows:
        try:
            authors = row[3].split('; ')
            article = ArxivArticle(
                row[0],
                row[1],
                row[2],
                authors,
                row[4])
            articles.append(article)
        except Exception as e:
            log.warning(e)

    return articles
