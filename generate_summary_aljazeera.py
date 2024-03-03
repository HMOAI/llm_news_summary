from aljazeera_scraper import get_aljazeera_headlines
from aljazeera_scraper import get_date
from llm_response_generator import get_llm_response
import time
from tqdm import tqdm
import json
import re
import json

def generate_day_headlines_string(day_object):
    headlines = [f"- {item['headline']}\n" for item in day_object if item.get('headline')]
    return "\n".join(headlines)

def get_headline_link(headline_text, day_object):
    for item in day_object:
        if item.get('headline'):
            headline_text = re.sub('\W', '', headline_text).lower()
            item_text = re.sub('\W', '', item.get('headline')).lower()
            if headline_text in item_text or item_text in headline_text:
                return item.get('link')

def get_day_top_json(top_headline_text_list, top_headline_link_list, date):
    events = []
    for headline, link in zip(top_headline_text_list, top_headline_link_list):
        event = {
            "text": headline,
            "link": link,
            "description": "",
            "images": [],
        }
        events.append(event)
    if date != 'No date found':
      title = (time.mktime(time.strptime(date, "%B %d, %Y")) - time.mktime(time.strptime("October 7, 2023", "%B %d, %Y"))) / (60 * 60 * 24)
      title = "Day " + str(int(title)+1)
      result = {
          "date": date,
          "title": title,
          "events": events,
      }
    else:
      result = {
          "date": date,
          "title": date,
          "events": events,
      }
    return result

def get_day_top_data(link_id, header_short_link_id):
    try:
        date = re.search(r"\d+-\d+-\d+", get_date(link_id)).group(0)
        date = time.strftime("%B %d, %Y", time.strptime(date, "%Y-%m-%d"))
    except:
        print("Error in url date: {}".format(day_url))
        date = 'No date found'

    try:
      day_headlines_list = get_aljazeera_headlines(link_id, header_short_link_id)
    except:
      print("Error in url content: {}".format(day_url))
      return [], [], date

    # Generate LLM response

    with open("prompt.md", "r") as f: #Read base prompt from file (prompt.md)
        base_prompt = f.read()
    prompt = base_prompt.format(generate_day_headlines_string(day_headlines_list))
    day_top_headlines = get_llm_response(prompt)
    # Clean LLM response
    day_top_headlines = day_top_headlines.split("\n") # Split by new line
    day_top_headlines = [item for item in day_top_headlines if item] # Remove empty items
    day_top_headlines = [item.strip() for item in day_top_headlines] # Remove leading and trailing spaces
    day_top_headlines = [re.sub(r"\d+\.", "", item).strip() for item in day_top_headlines] # Remove order numbers
    # Get urls
    day_top_urls = [get_headline_link(headline, day_headlines_list) for headline in day_top_headlines] 
    return day_top_headlines, day_top_urls, date

def write_output_to_file(ids, filename):
    days_json = []
    for link_id, header_short_link_id in tqdm(ids):
        day_top_headlines, day_top_urls, date = get_day_top_data(link_id, header_short_link_id)
        day_json = get_day_top_json(day_top_headlines, day_top_urls, date)
        days_json.append(day_json)
        # For backup
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(days_json, indent=2))
    # Finalize
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(days_json, indent=2))

def get_json_output(ids):
    days_json = []
    for link_id, header_short_link_id in tqdm(ids):
        day_top_headlines, day_top_urls, date = get_day_top_data(link_id, header_short_link_id)
        day_json = get_day_top_json(day_top_headlines, day_top_urls, date)
        days_json.append(day_json)
    return days_json

#--------------------Code Usage--------------------#
def get_output_from_string_list_and_write_to_file(ids, output_file):
  write_output_to_file(ids, output_file)

def get_output_from_string_list_and_return_as_json(ids):
  return get_json_output(ids)

def get_output_from_file_and_write_to_file(input_file, output_file):
  with open(input_file, 'r') as file:
    ids_line = file.read().splitlines()
  ids = [tuple(item.split(' ')) for item in ids_line]
  ids_new = []
  for link_id, header_short_link_id in ids:
    header_short_link_id = header_short_link_id[15:21]
    link_id = re.search(r"((?:[\w\d]+\-)+[\w\d]+)", link_id).group(0)
    ids_new.append((link_id, header_short_link_id))
  write_output_to_file(ids_new, output_file)

def get_output_from_file_and_return_as_json(input_file):
  with open(input_file, 'r') as file:
    ids_line = file.read().splitlines()
  ids = [tuple(item.split(' ')) for item in ids_line]
  return get_json_output(ids)
