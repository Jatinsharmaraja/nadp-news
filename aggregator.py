import feedparser
import json
import time
from datetime import datetime
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def aggregate():
    try:
        print("--- FETCHING NEWS ---")
        with open('sources.json', 'r') as f:
            sources = json.load(f)
        
        all_articles = []
        for source in sources:
            if not source.get('enabled', True): continue
            try:
                feed = feedparser.parse(source['url'])
                for entry in feed.entries[:6]:
                    pub = datetime.utcnow().isoformat()
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub = time.strftime('%Y-%m-%dT%H:%M:%SZ', entry.published_parsed)
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub = time.strftime('%Y-%m-%dT%H:%M:%SZ', entry.updated_parsed)
                    
                    summary = entry.summary if hasattr(entry, 'summary') else ""
                    summary = summary.replace('<p>', '').replace('</p>', '')[:200] + "..."

                    all_articles.append({
                        "source_name": source['name'],
                        "category": source['category'],
                        "title": entry.title,
                        "link": entry.link,
                        "summary": summary,
                        "published": pub
                    })
            except: pass

        with open('news.json', 'w') as f:
            json.dump(all_articles, f)
        print(f"--- SUCCESS: {len(all_articles)} ARTICLES SAVED ---")
    except Exception as e:
        print(f"FATAL ERROR: {e}")

if __name__ == "__main__":
    aggregate()