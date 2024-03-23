import arxiv

def main():
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 10 most recent articles
    search = arxiv.Search(
        query="cat:cs.AI",
        max_results = 10,
        sort_by = arxiv.SortCriterion.SubmittedDate,
    )
    print(search)

    results = client.results(search)

    for r in client.results(search):
        print(r.title)


if __name__ == '__main__':
    main()
