📦 MangaWrap
MangaWrap is a Python-based web API that scrapes and exposes manga data from MangaDex.org. It provides structured and searchable endpoints for browsing titles, recently added manga, latest chapter updates, and more — with support for pagination, category filtering, and full-text search.

🚀 Features
📖 /titles — Browse all manga titles (with pagination & category filtering)

🔍 /titles/search — Search manga by title (e.g. ?q=Naruto)

🆕 /recent — Recently added manga

🔄 /latest — Latest manga updates and chapters

🏷 /categories — List of all available genres/tags

💬 Clean JSON responses for easy frontend integration

⚙️ Powered by Flask, Playwright, and BeautifulSoup

🛠 Built With
Flask – lightweight web framework

Playwright – for JS-rendered scraping

BeautifulSoup – for parsing static HTML

Python – pure Python 3 app, deployable anywhere

🌐 Use Cases
Build your own manga aggregator frontend

Create bots, notifications, or search tools

Power mobile apps or browser extensions

