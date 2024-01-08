# Configuration for crawling Vitamin C products

# Time limit for the crawling process in seconds
TIME_LIMIT = 100

# The source URL from which the data will be crawled
SOURCE_URL = "https://www.gintarine.lt/search?q=vitaminas+c"

# The format for returning data ('csv' or any other format you might implement)
RETURN_FORMAT = 'csv'

# Boolean to determine whether to download images or not
DOWNLOAD_IMAGES = True

# The folder path where images will be downloaded
IMAGE_FOLDER = 'downloaded_images'

# The file path for the CSV file, if CSV format is chosen
CSV_FILE_PATH = 'vitamin_c_products.csv'