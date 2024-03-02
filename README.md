## Required packages
```bash
pip install -q -U google-generativeai
```
## Get URL
- CNN:
  - Navigate to google.com and search for "CNN Gaza war [month/day/year]", for example, "CNN Gaza war 2/12/2024".
  - Copy the URL of the relevant search result.
- Aljazeera:
  - Navigate to google.com and search for "Aljazeera Gaza war [month/day/year]", for example "Aljazeera Gaza war 2/12/2024"
  - Copy the URL of the relevant search result.
  - Get the last string of the URL (the higlighted part), for example:
    - https://www.aljazeera.com/news/liveblog/2024/2/28/**israels-war-on-gaza-live-thousands-could-die-in-days-as-israel-blocks-aid**
    - https://www.aljazeera.com/news/liveblog/2024/2/28/**israels-war-on-gaza-live-thousands-could-die-in-days-as-israel-blocks-aid**?update=2736768
  - Get the short link of the headders
## Use the url in the script like the following
```pyhton
# url_list.txt: file that contains new line separated URLs
# summary.json: file that contains the summary of the URLs
get_output_from_file_and_write_to_file("url_list.txt", "summary.json")
```
Note:
CNN: The url_list.txt has new line separated URLs
```txt
https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-02-14-24/index.html
https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-02-14-24/index.html
```
Aljazeera: The url_list.txt has new line separated link_id header_short_link
```txt
israels-war-on-gaza-live-thousands-could-die-in-days-as-israel-blocks-aid k5c04g
israels-war-on-gaza-live-thousands-could-die-in-days-as-israel-blocks-aid k5c04g
```