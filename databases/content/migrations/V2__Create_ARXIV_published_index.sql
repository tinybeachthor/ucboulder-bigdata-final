create index INDEX_ARXIV_published_BRIN
on ARXIV
using brin(published)
;
