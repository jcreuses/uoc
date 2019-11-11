from scraper import NewsScraper

output_file = "dataset.csv"

scraper = NewsScraper();
scraper.scrape();
scraper.data2csv(output_file);
