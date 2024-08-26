from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os, time, random
from flaskr.database import mongo

group_links = ["https://www.facebook.com/groups/1380680752778760/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/1870209196564360/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/520940308003364/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/647901439404148/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/186810449287215/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/2098391913533248/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/1998122560446744/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/1424244737803677/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/1068642559922565/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/1380680752778760/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/654949551249110/?sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/564985183576779/?sorting_setting=CHRONOLOGICAL"
               ]

filters = [
    "רמת גן", 
    'ר"ג', 
    "רמת-גן", 
    "שותף", 
    "שותפה", 
    "שותפ"
    "סטודיו", 
    "יחידת דיור",  
    "4 חד",
    "5 חד", 
    "2 חד"
    "מתפנה חדר", 
    "הרצל", 
    "ז'בוטינסקי", 
    "ברמת גן", 
    'אצ"ל',
    "מרום נווה",
    "מחליף",
    "קונה ברזל",
    "2 שותפים",
    "3 שותפים",
    "גלריה",
    "ללא מקלט",
    "אין מקלט",
    'ללא בע',
    "אסור בע",
    "בת ים",
    "פנטאוז",
    "מחפש דירה",
    "מחפש דירת",
    "מחפשת דירה",
    "מחפשת דירת",
    "רמת חן",
    "מתפנה חדר"
]

def get_env_path() -> str:
    # Get the directory of the current script
    current_directory = os.path.dirname(__file__)

    # Navigate to the parent directory (ApartmentHunterBot)
    parent_directory = os.path.dirname(current_directory)

    # Create the full path to the .env file
    env_path = os.path.join(parent_directory, '.env')

    return env_path


# Load the .env file
load_dotenv(dotenv_path=get_env_path())

def login_to_facebook(page, username, password):
    # Navigate to Facebook's website
    page.goto("https://www.facebook.com/")

    # Fill in the email/phone field
    page.fill("input[name='email']", username)

    # Fill in the password field
    page.fill("input[name='pass']", password)

    # Click on the Login button
    page.click("button[name='login']")

    # Wait for the page to load completely after logging in
    page.wait_for_load_state("networkidle")
    
    if page.url == "https://www.facebook.com/":
        
        if check_text_presence(page, "See more on Facebook"):
            login_to_facebook(page, username, password)
        
        else:
            print("Login successful")
            # page.goto("https://www.facebook.com/groups/647901439404148/?sorting_setting=CHRONOLOGICAL")
        
    else:
        print("Login failed")


def run_multiple_logins(times, username, password):
    # Create a Playwright session
    with sync_playwright() as p:
        for i in range(times):
            browser = p.chromium.launch(headless=False)  # Set headless=False to see the login process
            page = browser.new_page()
            
            print(f"Attempt {i + 1}: Logging in...")
            login_to_facebook(page, username, password)
            
            # Keep the browser open for a while in case you want to check what happened
            page.wait_for_timeout(5000)
            
            # Generate a random sleep time between 3 to 10 seconds
            sleep_time = random.uniform(2, 5)
            print(f"Waiting for {sleep_time:.2f} seconds before the next attempt...")
            time.sleep(sleep_time)
            
            browser.close()

def check_text_presence(page, text) -> bool:
    # Check if the specific text exists anywhere on the page
    return page.locator(f"text={text}").is_visible()

def find_see_more_button(post):
    # Locate the div with role='button' and text 'See more'
    see_more_button = post.locator("div[role='button']:has-text('See more'), div[role='button']:has-text('עוד'), div[role='button']:has-text('ראה עוד')")
    return see_more_button 

def click_on_see_more_button(page, post):
    # Look for the "See more" or "ראה עוד" button within the specific post element
    # see_more_button = post.locator("div[role='button']:has-text('See more'), div[role='button']:has-text('קרא עוד'), div[role='button']:has-text('ראה עוד')")

    # Use the page object to find the "See more" button within the post
    see_more_button = post.query_selector("div[role='button']:has-text('See more'), div[role='button']:has-text('קרא עוד'), div[role='button']:has-text('ראה עוד')")

    # Click the "See more" button if it exists
    if see_more_button and see_more_button.is_visible():
        see_more_button.click()
        page.wait_for_timeout(1000)  # Wait for content to expand
 
def post_contain_unwanted_words(post_content):
    for word in filters:
        if word in post_content:
            print(f"------\nThe word [{word}] is in [{post_content}]\n-------\n")
            return True
        
    return False
    
def get_post_link(post):
    link_elements = post.query_selector_all("a[href]")    
    links = [link.get_attribute("href") for link in link_elements]
    
    # Save the post's link
    post_link = ""
    for link in links:
        if "groups" in link and "posts" in link:
            post_link = link
            
    # Clean the url from unnecessary additions
    cleaned_url = "/".join(post_link.split("/")[:7])
    return cleaned_url

def scrape_group_posts(page, group_url, max_posts=10):
    page.goto(group_url)
    time.sleep(5)  # Wait for the page to load

    posts = []
    
    # Select all posts visible on the page
    post_elements = page.query_selector_all("div[role='article']")
    
    # Scroll down to load more posts
    if len(post_elements) < 5:
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(random.randint(2, 4))  # Give some time for posts to load
        post_elements = page.query_selector_all("div[role='article']")
            
    
    # Clear empty posts
    post_elements = [post for post in post_elements if len(post.inner_text()) > 0]

    for post in post_elements:
        try:
            # Click on the "See More" button if it exists
            click_on_see_more_button(page=page, post=post)
            
            # Extract text content from the post
            post_text = post.inner_text()
            post_link = get_post_link(post)
            post_url_id = post_link.split("/")[-1]
            post_link_exists = mongo.db.collection.find_one({"link": {"$regex": post_url_id}})
            
            
            if len(post_text) > 0 and not post_link_exists:    
                post_content_element = post.query_selector("div[data-ad-preview='message']")
                if post_content_element:  
                    post_content = post_content_element.inner_text()
                    print(f"---\npost_text[:10]= {post_text[:10]}")
                    print(f"---\npost_text[:10]= {post_content[:10]}")
                    post_content_exists = mongo.db.collection.find_one({"content": post_content})
                    if not post_contain_unwanted_words(post_content) and not post_content_exists:
                        _post = {
                            "link": post_link,
                            "content": post_content,
                            "hasBeenSent": False
                        }
                        posts.append(_post)
                    
                print(":: END OF post_content ::")
                # posts.append(post_text)
                print("---\n")
                print(f"{post_link}")
                print(f"{post_content}")  # Print or store the post content
                
        except Exception as e:
            print(f"Error extracting post: {e}")

    return posts

def make_login_and_get_posts():
    posts = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        username = os.getenv("FB_USERNAME")
        password = os.getenv("FB_PASSWORD")

        login_to_facebook(page, username, password)

        group_url = "https://www.facebook.com/groups/647901439404148/?sorting_setting=CHRONOLOGICAL"  # Replace with your group URL
        posts = []
        for link in group_links:
            posts.extend(scrape_group_posts(page, link))
            pass
            
        print(f"Scraped {len(posts)} posts")
        browser.close()
        
    return posts
    
def run_scraper():
    start_time = time.time()
    posts = make_login_and_get_posts() 
    end_time = time.time()
    total_time = end_time-start_time
    print(f"\n---------\ntotal running time: {total_time} ({(total_time/60):.2f} minutes)\n---------\n")
    return posts
 
def main():

    # run_multiple_logins(1, username, password)
    make_login_and_get_posts()
    

    

if __name__ == "__main__":
    main()
