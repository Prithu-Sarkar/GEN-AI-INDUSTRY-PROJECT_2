import requests
from bs4 import BeautifulSoup

def fetch_pubmed_articles_with_metadata(query: str, max_results: int = 3, use_mock_if_empty: bool = True) -> list:
    """
    Search PubMed via the NCBI E-utilities API and return structured
    metadata for the top articles matching the query.

    Args:
        query:            Search term (space-joined symptoms work well).
        max_results:      Maximum number of articles to return.
        use_mock_if_empty: Return mock data if no real results are found.

    Returns:
        List of dicts with keys: title, abstract, authors,
        publication_date, article_url.
    """
    headers = {"User-Agent": "Mozilla/5.0 (ClinisightAI-Research-Tool)"}

    # Step 1: Search PubMed for article IDs
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    try:
        search_response = requests.get(
            search_url, params=search_params, headers=headers, timeout=10
        ).json()
        id_list = search_response["esearchresult"]["idlist"]
        print("Found PubMed IDs:", id_list)

        if not id_list:
            raise ValueError("No IDs found for this query.")

        ids = ",".join(id_list)

        # Step 2: Fetch full XML records
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        fetch_params = {"db": "pubmed", "id": ids, "retmode": "xml"}
        fetch_response = requests.get(
            fetch_url, params=fetch_params, headers=headers, timeout=10
        )
        soup = BeautifulSoup(fetch_response.text, "lxml")
        articles_xml = soup.find_all("pubmedarticle")
        print("Articles found in XML:", len(articles_xml))

        articles_info = []
        for article, pmid in zip(articles_xml, id_list):
            title_tag    = article.find("articletitle")
            abstract_tag = article.find("abstract")
            date_tag     = article.find("pubdate")
            author_tags  = article.find_all("author")

            title    = title_tag.get_text(strip=True) if title_tag else "No title"
            abstract = abstract_tag.get_text(separator=" ", strip=True) if abstract_tag else "No abstract available"

            authors = []
            for author in author_tags:
                last = author.find("lastname")
                fore = author.find("forename")
                if last and fore:
                    authors.append(f"{fore.get_text()} {last.get_text()}")
                elif last:
                    authors.append(last.get_text())
            authors = authors if authors else ["No authors listed"]

            pub_date = "No date"
            if date_tag:
                year  = date_tag.find("year")
                month = date_tag.find("month")
                if year and month:
                    pub_date = f"{month.get_text()} {year.get_text()}"
                elif year:
                    pub_date = year.get_text()

            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            print(f"""Article: {title}
   - Authors: {authors}
   - Date: {pub_date}
   - URL: {url}
""")

            articles_info.append({
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "publication_date": pub_date,
                "article_url": url
            })

        if not articles_info and use_mock_if_empty:
            print("No valid articles found, returning mock data.")
            return _mock_data()

        return articles_info

    except Exception as e:
        print(f"Error during PubMed fetch: {e}")
        return _mock_data() if use_mock_if_empty else [{"message": f"Error: {e}"}]


def _mock_data() -> list:
    """Return a fallback mock article when PubMed is unreachable."""
    return [{
        "title": "Simulated Study on Fever",
        "abstract": "This is a simulated abstract on the treatment of fever in adults.",
        "authors": ["John Doe", "Jane Smith"],
        "publication_date": "March 2024",
        "article_url": "https://pubmed.ncbi.nlm.nih.gov/12345678/"
    }]