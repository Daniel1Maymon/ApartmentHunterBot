import asyncio
import json
import logging
import re
import traceback
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os, time, random
# from etc import email_functions
from etc import email_functions
from etc.openai_model import extract_info
from flaskr.data_access.post_repository import check_exists, save_post_on_db
from flaskr.database import mongo
from flask import current_app

from flaskr.models.post import get_posts_by_filter, insert_post, update_posts_by_filter
# from flaskr.extensions import socketio  # Import socketio

group_links = [
                "https://www.facebook.com/groups/1380680752778760/?# sorting_setting=CHRONOLOGICAL",
               "https://www.facebook.com/groups/1870209196564360/?sorting_setting=CHRONOLOGICAL",
                "https://www.facebook.com/groups/520940308003364/?sorting_setting=CHRONOLOGICAL",
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
    "ר״ג",
    "נווה יהושע",
    "תל אביב",
    "שותפים"
    "רמת-גן", 
    "שותף", 
    "שותפה", 
    "שותפ"
    "סטודיו", 
    "יחידת דיור",  
    "4 חד",
    "5 חד", 
    "2 חד",
    "2 חדרים",
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
            browser = p.chromium.launch(headless=True)  # Set headless=False to see the login process
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
    logging.info(f"Checking if text '{text}' is present on the page")
    # Check if the specific text exists anywhere on the page
    return page.locator(f"text={text}").is_visible()

def find_see_more_button(post):
    # Locate the div with role='button' and text 'See more'
    see_more_button = post.locator("div[role='button']:has-text('See more'), div[role='button']:has-text('עוד'), div[role='button']:has-text('ראה עוד')")
    return see_more_button 

def click_on_see_more_button(page, post):
    logging.info(f"Clicking on 'See more' button if exists")
    
    try:
        # Use the page object to find the "See more" button within the post
        see_more_button = post.query_selector("div[role='button']:has-text('See more'), div[role='button']:has-text('קרא עוד'), div[role='button']:has-text('ראה עוד')")

        # Click the "See more" button if it exists
        if not see_more_button:
            # logging.warning("See more button not found")
            return
        
        elif see_more_button.is_visible():
            see_more_button.click(force=True)
            logging.info("Clicked on 'See more' button")
            
        else:
            logging.warning("See more button not visible")
                
    
    except TimeoutError:
        logging.warning("Timed out waiting for the 'See more' button")
    
    except Exception as e:
        logging.error(f" |Error clicking on 'See more' button: {e}| ")
 
def post_contain_unwanted_words(post_content):
    for word in filters:
        if word in post_content:
            # print(f"\n------The word [{word}] is in [{post_content}]-------\n")
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
                    if (not post_contain_unwanted_words(post_content)) and not post_content_exists:
                        _post = {
                            "link": post_link,
                            "content": post_content,
                            "hasBeenSent": False
                        }
                        posts.append(_post)
                        # socketio.emit("new_post", _post)
                    
                    print(":: END OF post_content ::")
                    # posts.append(post_text)
                    print("---\n")
                    print(f"{post_link}")
                    print(f"{post_content}")  # Print or store the post content
                
        except Exception as e:
            print(f"Error extracting post: {e}")

    return posts

def mark_posts_as_sent():
    filter_criteria = {'hasBeenSent': False}
    update_values = {'hasBeenSent': True}
    return update_posts_by_filter(filter_criteria, update_values)

def make_login_and_get_new_posts():
    posts = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        username = os.getenv("FB_USERNAME")
        password = os.getenv("FB_PASSWORD")

        login_to_facebook(page, username, password)

        posts = []
        for link in group_links:
            group_posts = scrape_group_posts(page, link)
            posts.extend(group_posts)
            pass
            
        print(f"Scraped {len(posts)} posts")
        browser.close()
    
    return posts

def send_email_with_new_posts():
    # Read new posts from DB ("hasBeenSend:'false'")
    filter = {"hasBeenSent": False}
    
    new_posts = get_posts_by_filter(filter_criteria=filter)
    
    sender = 'daniel1maymon@gmail.com'
    recipients = [sender]
    subject = "פוסטים לדירות בפייסבוק"
    
    if not new_posts:
        print("No new posts found")
        
    else:
        print(f"\n--------- Sending email with the new posts ({len(new_posts)} found) --------- \n")
        msg = email_functions.format_posts_for_email(posts=new_posts)
        
        email_functions.send_email(subject=subject, body=msg, sender=sender, recipients=recipients)
    
        # Marking the nre posts as sent
        mark_posts_as_sent()
        
    
def run_scraper():
    print(f"\n---------\nRun Scraper\n---------\n")
    start_time = time.time()
    new_posts = make_login_and_get_new_posts() 
    end_time = time.time()
    total_time = end_time-start_time
    print(f"\n---------\ntotal running time: {total_time} ({(total_time/60):.2f} minutes)\n---------\n")
    
    return new_posts

def collect_group_posts_to_sql_db(page, group_url, max_posts=10):
    page.goto(group_url, timeout=30000)  # 30 seconds timeout
    time.sleep(5)  # Wait for the page to load
    
    # Select all posts visible on the page
    logging.info(f"Collecting posts from {group_url}")
    post_elements = page.query_selector_all("div[role='article']")
    
    # Scroll down to load more posts
    if len(post_elements) < 5:
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(random.randint(2, 4))  # Give some time for posts to load
        post_elements = page.query_selector_all("div[role='article']")
            
            
    # Clear empty posts
    post_elements = [post for post in post_elements if len(post.inner_text()) > 0]
    
    logging.info(f"Collected {len(post_elements)} posts from {group_url}")
    
      
    for post in post_elements:
        logging.info(f"Collecting post from {group_url}")
        try:
            # Click on the "See More" button if it exists
            click_on_see_more_button(page=page, post=post)
            
            # Extract text content from the post
            post_text = post.inner_text()
            post_link = get_post_link(post)
            post_url_id = post_link.split("/")[-1]
            

            # if len(post_text) > 0 and not post_link_exists:    
            if len(post_text) > 0:   
                post_content_element = post.query_selector("div[data-ad-preview='message']")
                if post_content_element and not check_exists(f'posts/{post_url_id}'):  
                    post_content = post_content_element.inner_text()
                    # print(f"---\npost_text[:10]= {post_text[:10]}")
                    print(f"---\npost_text[:10]= {post_content[:10]}")
                    post_content_exists = mongo.db.collection.find_one({"content": post_content})
                    # if (not post_contain_unwanted_words(post_content)) and not post_content_exists:
                    _post = {
                        "link": post_link,
                        "content": post_content,
                        "hasBeenSent": False
                    }
                    insert_post(_post)
                    
                    # Send post to GPT:
                    extracted_info = extract_info(post_content)
                    
                    if 'false' not in str.lower( extracted_info):
                        extracted_info_in_json = json.loads(extracted_info)
                        '''
                        extracted_info_in_json = {
                            'price': 5000,
                            'rooms': 3,
                            'size': 70,
                            'city': 'Givataim',
                            'address':'shenkin',
                            'url': 'www....'
                        }
                        '''
                        extracted_info_in_json['url'] = post_link
                        extracted_info_in_json['description'] = post_content
                        # print(extracted_info_in_json)
                        
                        save_post_on_db(extracted_info_in_json)
                        
                        print(":: END OF post_content ::")
                        # posts.append(post_text)
                        print("---\n")
                        # print(f"{post_link}")
                        # print(f"{post_content}")  # Print or store the post content
                
        except Exception as e:
            print(f"Error extracting post: {e}")
            print("Detailed traceback:")
            traceback.print_exc()

            

def scrape_and_store_posts():
    print(f"\n---------\nscrape_and_store_posts()\n---------\n")
    start_time = time.time()
    # new_posts = make_login_and_get_new_posts() 
    

    with sync_playwright() as p:
        print("Starting browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Login:
        username = os.getenv("FB_USERNAME")
        password = os.getenv("FB_PASSWORD")
        
        print("Logging in...")
        login_to_facebook(page, username, password)
        
        # Save posts on db
        print("Scraping posts...")
        for link in group_links:
            try:
                collect_group_posts_to_sql_db(page, link)
            except Exception as e:
                logging.error(f"Error scraping posts from {link}: {e}")
                continue
            

async def main():

    # run_multiple_logins(1, username, password)
    await make_login_and_get_new_posts()
    

    

if __name__ == "__main__":
    # main()
    asyncio.run(scrape_and_store_posts())
