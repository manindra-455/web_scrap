import random
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# List of user agents for rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    # Add more user agents as we needed
]

# Function to get a random user-agent
def get_random_user_agent():
    return random.choice(user_agents)

# Initialize Chrome WebDriver with options to prevent blocking
def init_driver(user_agent=None):
    options = Options()
    options.headless = False  # Set to True for headless scraping
    if user_agent:
        options.add_argument(f'user-agent={user_agent}')
    
    # Disable the use of proxies
    options.add_argument('--no-proxy-server')
    options.add_argument('--proxy-bypass-list=*')
    
    # Disable webdriver detection flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Disable image loading for faster load times
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    
    # Randomize window size to mimic real user interaction
    width, height = random.randint(800, 1200), random.randint(600, 900)
    options.add_argument(f"--window-size={width},{height}")
    
    # Create driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Additional settings to prevent detection
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# Initialize the WebDriver with a random user-agent
user_agent = get_random_user_agent()
driver = init_driver(user_agent)

# Set a URL and navigate with random pauses to avoid detection
url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
driver.get(url)
time.sleep(random.uniform(3, 5))  # Add a random delay between requests

# Function to get product links
def get_product_links():
    return driver.find_elements(By.XPATH, "//a[@class='a-link-normal s-no-outline']")

# Open a CSV file to write the extracted data
with open('web_scraping/data/products_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price", "Rating", "Seller Name", "Stock Status"])  # Write header

    # Loop through product links and extract data
    product_links = get_product_links()

    for link in product_links:
        try:
            product_url = link.get_attribute('href')
            driver.get(product_url)
            time.sleep(random.uniform(3, 5))  # Random delay for each product

            # Extracting product details 
            try:
                title = driver.find_element(By.ID, "productTitle").text
                price = driver.find_element(By.XPATH, "//span[@class='a-price-whole']").text
                
                # Extract rating
                rating = driver.find_element(By.XPATH, "//span[@data-hook='rating-out-of-text']")
                rating_text = rating.text
                rating_value = rating_text.split(" ")[0] if rating else "N/A"
                
                # Check if the product is in stock
                stock_status = driver.find_element(By.ID, "availability").text
                in_stock = "In Stock" if "In stock" in stock_status else "Out of Stock"
                
                # Extract the seller's name only if the product is in stock
                if in_stock == "In Stock":
                    seller_name = driver.find_element(By.XPATH, "//span[@class='a-size-small tabular-buybox-text-message']//a[@id='sellerProfileTriggerId']").text
                else:
                    seller_name = "N/A"
            
            except Exception as e:
                print(f"Error extracting data for {product_url}: {e}")
                title, price, rating_value, seller_name, in_stock = "N/A", "N/A", "N/A", "N/A", "N/A"

            # Write the extracted data into CSV
            writer.writerow([title, price, rating_value, seller_name, in_stock])

            # Print extracted details
            print("Product Name:", title)
            print("Price:", price)
            print("Rating:", rating_value)
            print("Seller:", seller_name)
            print("Stock Status:", in_stock)

        except Exception as e:
            print(f"Error with link: {e}")
            continue

        # Go back to the listing page
        driver.back()
        time.sleep(random.uniform(2, 4))  # Random delay to prevent rapid navigation
        
        # Refetch the product links after going back
        product_links = get_product_links()

# Close the driver after operations are complete
driver.quit()
print("Script executed successfully.")
