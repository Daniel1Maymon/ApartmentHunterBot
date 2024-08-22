from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os, time, random

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
            
            if len(post_text) > 0 and  any(post_link == post[1] for post in posts) is not True:
                post_content = post.query_selector("div[data-ad-preview='message']").inner_text()
                posts.append([post_content, post_link])
                # posts.append(post_text)
                print("---\n")
                print(f"{post_link}")
                print(f"{post_content}")  # Print or store the post content
                
        except Exception as e:
            print(f"Error extracting post: {e}")

    return posts

def make_login_and_get_posts(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        username = os.getenv("FB_USERNAME")
        password = os.getenv("FB_PASSWORD")

        login_to_facebook(page, username, password)

        group_url = "https://www.facebook.com/groups/647901439404148/?sorting_setting=CHRONOLOGICAL"  # Replace with your group URL
        posts = scrape_group_posts(page, group_url)

        print(f"Scraped {len(posts)} posts")
        
        browser.close()
        
def main():
    # Enter your user credentials here (remember to secure this information)
    username = os.getenv("FB_USERNAME")
    password = os.getenv("FB_PASSWORD")

    # run_multiple_logins(1, username, password)
    make_login_and_get_posts(username, password)
    

    

if __name__ == "__main__":
    main()
