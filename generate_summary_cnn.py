from cnn_scraper import get_cnn_headlines
from llm_response_generator import get_llm_response
import time
from tqdm import tqdm
import json
import re
import argparse
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

def get_day_top_data(day_url):
    try:
        date = re.search(r"\d+-\d+-\d+", day_url).group(0)
        if len(date.split("-")[2]) == 2:
            date = date[:-2] + "20" + date[-2:]
        date = time.strftime("%B %d, %Y", time.strptime(date, "%m-%d-%Y"))
    except:
        print("Error in url date: {}".format(day_url))
        date = 'No date found'

    try:
      day_headlines_list = get_cnn_headlines(day_url)
    except:
      print("Error in url content: {}".format(day_url))
      return [], [], date

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

def write_output_to_file(days_urls, filename):
    days_json = []
    for day_url in tqdm(days_urls):
        day_top_headlines, day_top_urls, date = get_day_top_data(day_url)
        day_json = get_day_top_json(day_top_headlines, day_top_urls, date)
        days_json.append(day_json)
        # For backup
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(days_json, indent=2))
    # Finalize
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(days_json, indent=2))

def get_json_output(days_urls):
    days_json = []
    for day_url in tqdm(days_urls):
        day_top_headlines, day_top_urls, date = get_day_top_data(day_url)
        day_json = get_day_top_json(day_top_headlines, day_top_urls, date)
        days_json.append(day_json)
    return days_json

#--------------------Code Usage--------------------#
def get_output_from_string_list_and_write_to_file(urls, output_file):
  write_output_to_file(urls, output_file)

def get_output_from_string_list_and_return_as_json(urls):
  return get_json_output(urls)

def get_output_from_file_and_write_to_file(input_file, output_file):
  with open(input_file, 'r') as file:
    urls = file.read().splitlines()
  write_output_to_file(urls, output_file)

def get_output_from_file_and_return_as_json(input_file):
  with open(input_file, 'r') as file:
    urls = file.read().splitlines()
  return get_json_output(urls)

#--------------------Terminal Usage--------------------#
def parse_arguments():
  parser = argparse.ArgumentParser(description='Process command line arguments.')
  parser.add_argument('-s', '--string', type=str, help='Input URLs separated by comma')
  parser.add_argument('-f', '--file', type=str, help='Input file containing URLs separated by new line')
  parser.add_argument('-o', '--output', type=str, default='summary.json', help='Output file name')
  parser.add_argument('-t', '--terminal', action='store_true', help='Print output to terminal')
  return parser.parse_args()

def main():
  args = parse_arguments()
  urls = []
  if args.string:
    urls = args.string.split(',')
  elif args.file:
    with open(args.file, 'r') as file:
      urls = file.read().splitlines()
  else:
    print('Please provide input URLs using -s or -f flag.')
    return
  
  if args.terminal:
    # Print output to terminal
    output = get_json_output(urls)
    print(output)
  else:
    # Write output to file
    output = get_json_output(urls)
    with open(args.output, 'w') as file:
      file.write(json.dumps(output, indent=2))

if __name__ == '__main__':
  main()
