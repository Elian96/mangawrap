import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from urllib.parse import urlencode

BASE_URL = "https://mangadex.org"

### GET LATEST MANGA ###
def get_latest_manga(page=1):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_obj = browser.new_page()
        page_obj.goto(f"{BASE_URL}/titles/latest?page={page}", timeout=60000)
        page_obj.wait_for_selector(".chapter-feed__container", timeout=10000)

        containers = page_obj.query_selector_all(".chapter-feed__container")

        for container in containers:
            try:
                # Title and URL
                title_link = container.query_selector("a.chapter-feed__title")
                title = title_link.inner_text().strip()
                manga_url = BASE_URL + title_link.get_attribute("href")

                # Cover image
                img_tag = container.query_selector("a.chapter-feed__cover img")
                cover_url = img_tag.get_attribute("src")
                if cover_url.startswith("/"):
                    cover_url = BASE_URL + cover_url

                # Chapter info
                chapter_link = container.query_selector("a.chapter-grid")
                chapter_url = BASE_URL + chapter_link.get_attribute("href")

                chapter_title_tag = container.query_selector("span.chapter-link span")
                chapter_title = chapter_title_tag.inner_text().strip() if chapter_title_tag else "N/A"

                scanlator_tag = container.query_selector("a.group-tag")
                scanlator = scanlator_tag.inner_text().strip() if scanlator_tag else None

                uploader_tag = container.query_selector("a[href*='/user/']")
                uploader = uploader_tag.inner_text().strip() if uploader_tag else None

                timestamp_tag = container.query_selector("time")
                timestamp = timestamp_tag.get_attribute("datetime") if timestamp_tag else None

                results.append({
                    "title": title,
                    "manga_url": manga_url,
                    "cover_image": cover_url,
                    "latest_chapter": {
                        "title": chapter_title,
                        "url": chapter_url,
                        "scanlator": scanlator,
                        "uploaded_by": uploader,
                        "timestamp": timestamp
                    }
                })

            except Exception as e:
                print(f"Error parsing entry: {e}")
                continue

        browser.close()

    return {
        "page": page,
        "results_count": len(results),
        "results": results
    }

### GET RECENT MANGA ###
def get_recent_manga(page=1):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_obj = browser.new_page()
        page_obj.goto(f"{BASE_URL}/titles/recent?page={page}", timeout=60000)

        # Use new selector specific to the "recently added" page
        page_obj.wait_for_selector(".manga-card", timeout=10000)
        containers = page_obj.query_selector_all(".manga-card")

        for container in containers:
            try:
                # Title and URL
                title_tag = container.query_selector("a.title")
                title = title_tag.inner_text().strip()
                manga_href = title_tag.get_attribute("href")
                manga_url = BASE_URL + manga_href

                # Cover image
                cover_img = container.query_selector(".manga-card-cover img")
                cover_url = cover_img.get_attribute("src")
                if cover_url.startswith("/"):
                    cover_url = BASE_URL + cover_url

                # Tags/Genres (optional bonus)
                tag_elements = container.query_selector_all(".tags-row a.tag")
                tags = [tag.inner_text().strip() for tag in tag_elements]

                # Description (optional bonus)
                desc_container = container.query_selector(".description p")
                description = desc_container.inner_text().strip() if desc_container else None

                results.append({
                    "title": title,
                    "manga_url": manga_url,
                    "cover_image": cover_url,
                    "tags": tags,
                    "description": description
                })

            except Exception as e:
                print(f"Error parsing manga-card: {e}")
                continue

        browser.close()

    return {
        "page": page,
        "results_count": len(results),
        "results": results
    }

### GET ALL TITLES ###
def get_all_titles(page=1, category=None):
    results = []

    # If user passed a category name, convert it to ID
    if category:
        cat_map = get_category_map()
        category_id = cat_map.get(category.lower())
        if not category_id:
            return {
                "page": page,
                "category": category,
                "results_count": 0,
                "results": [],
                "error": f"Category '{category}' not found"
            }
    else:
        category_id = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_obj = browser.new_page()

        # Build the URL with optional category
        base_params = {
            "page": page
        }

        if category:
            base_params["includedTags[]"] = category_id
            base_params["includedTagsMode"] = "AND"

        query_string = urlencode(base_params, doseq=True)
        url = f"{BASE_URL}/titles?{query_string}"

        page_obj.goto(url, timeout=60000)
        page_obj.wait_for_selector(".manga-card", timeout=10000)
        containers = page_obj.query_selector_all(".manga-card")

        for container in containers:
            try:
                title_tag = container.query_selector("a.title")
                title = title_tag.inner_text().strip()
                manga_href = title_tag.get_attribute("href")
                manga_url = BASE_URL + manga_href

                cover_img = container.query_selector(".manga-card-cover img")
                cover_url = cover_img.get_attribute("src")
                if cover_url.startswith("/"):
                    cover_url = BASE_URL + cover_url

                tag_elements = container.query_selector_all(".tags-row a.tag")
                tags = [tag.inner_text().strip() for tag in tag_elements]

                status_tag = container.query_selector(".status span")
                status = status_tag.inner_text().strip() if status_tag else "Unknown"

                rating_tag = container.query_selector(".stat")
                rating = rating_tag.inner_text().strip() if rating_tag else "N/A"

                desc_tag = container.query_selector(".description p")
                description = desc_tag.inner_text().strip() if desc_tag else None

                results.append({
                    "title": title,
                    "manga_url": manga_url,
                    "cover_image": cover_url,
                    "tags": tags,
                    "status": status,
                    "rating": rating,
                    "description": description
                })

            except Exception as e:
                print(f"Error parsing manga-card: {e}")
                continue

        browser.close()

    return {
        "page": page,
        "category": category,
        "results_count": len(results),
        "results": results
    }

### SEARCH TITLE ###
def search_titles(query, page=1):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_obj = browser.new_page()

        # Encode query safely for the URL
        from urllib.parse import quote
        query_param = quote(query)

        url = f"{BASE_URL}/titles?page={page}&q={query_param}&onlyAvailableChapters=false"
        page_obj.goto(url, timeout=60000)
        page_obj.wait_for_selector(".manga-card", timeout=10000)

        containers = page_obj.query_selector_all(".manga-card")

        for container in containers:
            try:
                # Title and URL
                title_tag = container.query_selector("a.title")
                title = title_tag.inner_text().strip()
                manga_href = title_tag.get_attribute("href")
                manga_url = BASE_URL + manga_href

                # Cover image
                cover_img = container.query_selector(".manga-card-cover img")
                cover_url = cover_img.get_attribute("src")
                if cover_url.startswith("/"):
                    cover_url = BASE_URL + cover_url

                # Tags
                tag_elements = container.query_selector_all(".tags-row a.tag")
                tags = [tag.inner_text().strip() for tag in tag_elements]

                # Status
                status_tag = container.query_selector(".status span")
                status = status_tag.inner_text().strip() if status_tag else "Unknown"

                # Rating (optional cleanup)
                rating_tag = container.query_selector(".stat")
                rating = rating_tag.inner_text().strip() if rating_tag else "N/A"

                # Description
                desc_tag = container.query_selector(".description p")
                description = desc_tag.inner_text().strip() if desc_tag else None

                results.append({
                    "title": title,
                    "manga_url": manga_url,
                    "cover_image": cover_url,
                    "tags": tags,
                    "status": status,
                    "rating": rating,
                    "description": description
                })

            except Exception as e:
                print(f"Error parsing search result: {e}")
                continue

        browser.close()

    return {
        "query": query,
        "page": page,
        "results_count": len(results),
        "results": results
    }

### VATEGORY MAPPING ###
def get_category_map():
    category_map = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"{BASE_URL}/titles", timeout=60000)
        page.wait_for_selector("a.tag", timeout=10000)
        tag_elements = page.query_selector_all("a.tag")

        for tag in tag_elements:
            try:
                name = tag.inner_text().strip().lower()
                href = tag.get_attribute("href")
                if not href or not href.startswith("/tag/"):
                    continue

                parts = href.split("/")
                tag_id = parts[2] if len(parts) > 2 else None

                if name and tag_id:
                    category_map[name] = tag_id

            except Exception as e:
                print(f"Error parsing tag: {e}")
                continue

        browser.close()

    return category_map

### GET ALL CATEGORIES ###
def get_categories():
    categories = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"{BASE_URL}/titles", timeout=60000)

        # Wait for tags to load
        page.wait_for_selector("a.tag", timeout=10000)
        tag_elements = page.query_selector_all("a.tag")

        for tag in tag_elements:
            try:
                name = tag.inner_text().strip()
                href = tag.get_attribute("href")  # e.g. /tag/{uuid}/romance

                if not href or not href.startswith("/tag/"):
                    continue

                # Extract ID and slug
                parts = href.split("/")
                tag_id = parts[2] if len(parts) > 2 else None
                slug = parts[3] if len(parts) > 3 else None

                categories.append({
                    "id": tag_id,
                    "slug": slug,
                    "name": name
                })

            except Exception as e:
                print(f"Error parsing tag: {e}")
                continue

        browser.close()

    return {
        "total": len(categories),
        "categories": categories
    }
