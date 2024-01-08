# Import necessary libraries
import requests  # For making HTTP requests
from lxml import html as HTML  # For parsing HTML
import time  # For tracking the time limit
import os  # For file path operations
import pandas as pd  # For data manipulation and saving as CSV
import config  # Importing configuration settings

# Function to download images
def download_image(image_url, folder_path, file_name):
    try:
        response = requests.get(image_url)  # Send a GET request to the image URL
        if response.status_code == 200:  # Check if the request was successful
            file_path = os.path.join(folder_path, file_name)  # Construct the file path
            with open(file_path, 'wb') as file:  # Open the file in write-binary mode
                file.write(response.content)  # Write the content of the response
            return file_path  # Return the file path where the image is saved
    except Exception as e:
        print(f"Error downloading image: {e}")  # Print any errors encountered
    return None  # Return None if the download was unsuccessful

# Function to crawl and extract product data
def crawl_vitamin_c_products(time_limit, source, download_images=True):
    start_time = time.time()  # Record the start time
    data = pd.DataFrame(columns=['Product Name', 'Price', 'Image URL', 'Image Path'])  # Initialize a DataFrame
    image_folder = 'downloaded_images'  # Set the folder name for downloaded images

    # Create the folder if it doesn't exist and if download_images is True
    if download_images and not os.path.exists(image_folder):
        os.makedirs(image_folder)

    try:
        response = requests.get(source)  # Send a GET request to the source URL
        # Check if the request was successful
        if response.status_code != 200:
            return "Failed to retrieve data from the source"

        # Parse the HTML content
        tree = HTML.fromstring(response.content)

        # Loop through each product item in the HTML
        for product in tree.xpath("//div[contains(@class, 'product-item')]"):
            # Extract product name, price, and image URL using XPath
            product_name = product.xpath("./input[@name='productName']/@value")[0].strip()
            price = product.xpath("./input[@name='productPrice']/@value")[0].strip()
            image_url = product.xpath('.//img/@src')[0]

            image_path = 'Not Downloaded'
            # Download the image if download_images is True
            if download_images:
                image_file_name = f"{product_name.replace('/', '_')}.jpg"
                image_path = download_image(image_url, image_folder, image_file_name)
                image_path = image_path if image_path else 'Not Found'

            # Create a DataFrame for the current product
            product_df = pd.DataFrame({
                'Product Name': [product_name],
                'Price': [price],
                'Image URL': [image_url],
                'Image Path': [image_path]
            })

            # Concatenate the current product DataFrame to the main DataFrame
            data = pd.concat([data, product_df], ignore_index=True)

            # Check if the time limit has been reached
            if time.time() - start_time > time_limit:
                break

    except Exception as e:
        return f"An error occurred: {e}"  # Print any errors encountered

    # Save data to CSV file
    csv_file_path = 'vitamin_c_products.csv'
    data.to_csv(csv_file_path, index=False, encoding='utf-8')  # Save the DataFrame as a CSV file
    print(f"Data saved to CSV file: {csv_file_path}")  # Notify that the data has been saved

    # Print the DataFrame
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(data)  # Print the DataFrame in a tabular format

    return data  # Return the DataFrame

# Example function call with parameters from the config file
crawl_vitamin_c_products(
    time_limit=config.TIME_LIMIT,
    source=config.SOURCE_URL,
    download_images=config.DOWNLOAD_IMAGES
)
