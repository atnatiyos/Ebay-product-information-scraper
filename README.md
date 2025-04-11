🛒 Product Info Scraper

A Python script that scrapes product details from e-commerce websites using Selenium and stores the extracted data into a CSV file using Pandas.
🔍 Features

    Extracts key product information:

        ✅ Product Name

        💵 Product Price

        🏷️ Product Condition

        🌍 Product Origin

        🖼️ Product Image URL

    Saves the data neatly in a CSV file for easy analysis or integration

    Built with Selenium for dynamic content handling

    Uses Pandas for data manipulation and CSV export

🛠️ Tech Stack

    Python 3

    Selenium (for web automation and scraping)

    Pandas (for data processing and export)

📁 Output

The script creates a products.csv file with the following columns:
Product Name	Price	Condition	Origin	Image URL
🚀 How to Use

    Install the required libraries:

pip install requirements.txt

Make sure you have the correct browser driver (e.g., ChromeDriver) installed and in your PATH.

Run the script:

    python scraper.py

    💡 Note: Update the target product in the script based on the product you're scraping.
