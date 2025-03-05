import os
import sys
import json

# Add the app directory to sys.path to import sn_xml_downloader
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "..", "app")
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

import sn_xml_downloader

def load_test_articles():
    """
    Loads the JSON list of articles from:
    ../app/system_data/json_references/test_articles.json
    """
    json_path = os.path.join(app_dir, "system_data", "json_references", "test_articles.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading test articles: {e}")
        return []

def save_found_articles(found_articles):
    """
    Saves the list of found articles to:
    ../app/system_data/sn_open_access_articles.json
    """
    output_path = os.path.join(app_dir, "system_data", "sn_open_access_articles.json")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(found_articles, f, indent=4)
        print(f"\nFound articles successfully saved to: {output_path}")
    except Exception as e:
        print(f"Error saving found articles: {e}")

def main():
    articles = load_test_articles()
    if not articles:
        print("No test articles found. Exiting.")
        return

    found_articles = []
    for article in articles:
        doi = article.get("doi")
        if not doi:
            print(f"Article missing DOI: {article}")
            continue

        print(f"\nChecking existence for DOI: {doi}")
        result = sn_xml_downloader.check_article_existence(doi)
        if result:
            print(f"Article with DOI {doi} exists in Springer Nature Open Access.")
            # Store a summary; you may choose to store result or a combination of test article info and API response.
            found_articles.append({
                "doi": doi,
                "title": article.get("title"),
                "found_metadata": result
            })
        else:
            print(f"Article with DOI {doi} does NOT exist in Springer Nature Open Access.")

    count = len(found_articles)
    print(f"\nTotal articles found in Springer Nature Open Access: {count}")
    save_found_articles(found_articles)

if __name__ == '__main__':
    main()
