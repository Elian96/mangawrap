# 📚 MangaWrap

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-API-lightgrey?style=flat-square&logo=flask)
![Playwright](https://img.shields.io/badge/Powered%20By-Playwright-green?style=flat-square&logo=microsoft)
![License](https://img.shields.io/github/license/your-username/mangawrap?style=flat-square)

> A powerful and flexible Python API that scrapes [MangaDex.org](https://mangadex.org) and wraps it in clean, searchable, paginated JSON endpoints. Designed for developers, bot creators, manga fans, and frontend builders.

---

## 🚀 Features

- 🔍 **Search Manga** by title with `/titles/search?q=...`
- 📖 **Browse Titles** with pagination & category filters
- 🆕 **Recently Added Manga** `/recent`
- 🔄 **Latest Chapter Updates** `/latest`
- 🏷 **Category/Genre Lookup** `/categories`
- 📦 Pure Python – no external APIs used
- ⚙️ Easily extendable & self-hosted

---

## 📦 Endpoints

| Route                | Description                         | Example                                 |
|---------------------|-------------------------------------|-----------------------------------------|
| `/titles`           | Browse all manga titles             | `?page=1` `?category=Romance`           |
| `/titles/search`    | Search by title keyword             | `?q=Naruto&page=1`                      |
| `/latest`           | Latest manga updates                | `?page=2`                               |
| `/recent`           | Recently added manga                | `?page=3`                               |
| `/categories`       | List all genres/categories          | -                                       |

---

## 🛠 Setup & Installation

> Requires Python 3.8+ and Chrome (Playwright will auto-install it)

```bash
# Clone the repo
git clone https://github.com/your-username/mangawrap.git
cd mangawrap

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install

# Run the server
python app.py
```

## 🧪 Example Response

```bash
{
  "title": "Naruto",
  "manga_url": "https://mangadex.org/title/...",
  "cover_image": "https://mangadex.org/covers/...",
  "tags": ["Shounen", "Action"],
  "status": "Completed",
  "rating": "8.67",
  "description": "A story about a ninja boy named Naruto..."
}
```

## 🧠 Use Cases
- Build custom manga frontends

- Create bots and recommendation engines

- Integrate with mobile apps

- Collect stats, reviews, genres, and more

## 🤝 Contributing
Pull requests and ideas are always welcome. Feel free to fork and extend!

## 📄 License
MIT

## ❤️ Acknowledgments
- MangaDex for the content

- Playwright for JS rendering

- BeautifulSoup for HTML parsing


