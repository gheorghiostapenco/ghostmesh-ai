import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
API_IP = "130.61.235.138"  # <--- PUT YOUR SERVER IP HERE
LEARN_URL = f"http://{API_IP}/learn"
ASK_URL = f"http://{API_IP}/ask"

def scrape_hacker_news():
    """Scrapes the top 5 headlines from Hacker News"""
    print("🕷️  Scraping Hacker News...")
    try:
        response = requests.get("https://news.ycombinator.com/")
        soup = BeautifulSoup(response.text, "html.parser")
        
        headlines = []
        # CSS selector to find titles on Hacker News
        for item in soup.select(".titleline > a")[:5]:
            headlines.append(item.get_text())
            
        return headlines
    except Exception as e:
        print(f"Error scraping: {e}")
        return []

def feed_memory(headlines):
    """Sends headlines to the /learn API endpoint"""
    print(f"\n🧠 Feeding {len(headlines)} headlines into the AI Memory...")
    
    for title in headlines:
        payload = {
            "text": f"Breaking Tech News: {title}",
            "source": "hacker_news_scraper"
        }
        try:
            # This is the M2M automation power!
            r = requests.post(LEARN_URL, json=payload)
            if r.status_code == 200:
                print(f"   [LEARNED] {title[:30]}...")
            else:
                print(f"   [FAIL] {r.status_code}")
        except Exception as e:
            print(f"   [ERROR] {e}")

def ask_for_summary():
    """Asks the AI to report back on what it learned"""
    print("\n🤖 Asking AI for a summary...")
    
    prompt = "Based on the breaking tech news you just learned, list the main topics."
    
    try:
        r = requests.post(ASK_URL, json={"prompt": prompt})
        data = r.json()
        
        print("\n" + "="*40)
        print("📝 AI REPORT:")
        print(data.get("answer"))
        print("="*40)
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    news = scrape_hacker_news()
    if news:
        feed_memory(news)
        ask_for_summary()
