import csv


def file_write(data_to_write):
    """Writes a crawled data to a csv file using a DictWriter method."""
    with open('crawl_data.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['Property name', 'Property price', 'Auction end date', 'Highest bid', 'Auction link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_to_write)
