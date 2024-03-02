## Required packages
```bash
pip install -q -U google-generativeai
```
## Get URL
- Navigate to google.com and search for "CNN Gaza war [month/day/year]", for example, "CNN Gaza war 2/12/2024".
- Copy the URL of the relevant search result.
## Use the url in the script like the following
By running the following command the summary of the news from the URL be generated in ```summary.json``` file:
```bash
python generate_summary.py -s "https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-02-12-24/index.html"
```
For multiple URLs, use comma separated URLs like the following:
```bash
python generate_summary.py -s "https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-02-11-24/index.html, https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-02-12-24/index.html"
```
For multiple URLs, use comma separated URLs like the following:
```bash
python generate_summary.py -s "https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-02-11-24/index.html, https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-02-12-24/index.html"
```
Additionally, for multiple URLs, a file that contains new line separated URLs could be used:
```bash
python generate_summary.py -f "url_list.txt"
```