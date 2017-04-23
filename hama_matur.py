import codecs
import configparser
import datetime
import re

from bs4 import BeautifulSoup
from slackclient import SlackClient
from selenium import webdriver

config = configparser.ConfigParser();
config.read_file(codecs.open('config.ini', 'r', 'utf8'));

# Háma's site uses javascript to populate the table,
# so we need phantomjs to run the js before parsing the html
PHANTOMJS_PATH = config['phantomjs'].get('path');

SLACK_CHANNEL = config['slack'].get('channel');
SLACKBOT_TOKEN = config['slack'].get('token');

HAMA_URL = url = 'http://www.fs.is/is/hama/'

def parse_date(date_str):
	reg = re.compile('(\D*)\s*(\d{1,2})\.\s(.*)', re.IGNORECASE);
	return reg.match(date_str).groups();

def is_today(date_str):
	match = parse_date(date_str);
	date = datetime.date(2016, month_number(match[2]), int(match[1]));
	today = datetime.date.today();

	return date == today;

# This is crap, can be made better with pattern matching?
def month_number(month_str):
	return {
		'janúar': 1,
		'febrúar': 2,
		'mars': 3,
		'apríl': 4,
		'maí': 5,
		'júní': 6,
		'júlí': 7,
		'ágúst': 8,
		'september': 9,
		'október': 10,
		'nóvember': 11,
		'desember': 12
	}.get(month_str, -1);

def slack_notify(message, token=SLACKBOT_TOKEN, channel=SLACK_CHANNEL):
	print(message);
	client = SlackClient(token);
	if(client.rtm_connect()):
		client.rtm_send_message(channel, message);
	else:
		print('Could not send message');

def get_food_info():
	def parse_food(data):
		return data[1].text;

	return get_hama_info('hama_tab-1', parse_food);

def get_soups_info():
	def parse_soup(data):
		return (data[1].text, data[2].text);

	return get_hama_info('hama_tab-3', parse_soup);

def get_hama_info(div_id, parse_func):
	driver = webdriver.PhantomJS(executable_path = PHANTOMJS_PATH);
	driver.get(HAMA_URL);

	soup = BeautifulSoup(driver.page_source, 'html.parser');

	div = soup.find('div', {'id': div_id});
	table = div.find('table', {'class': 'hama_sedill'});
	rows = table.find_all('tr');

	for row in rows:
		data = row.find_all('td');

		try:
			if(is_today(data[0].text)):
				return parse_func(data);
		except:
			pass


if __name__ == '__main__':
	print('Getting food info');
	food = get_food_info();

	print('Getting soups info')
	soups = get_soups_info();

	today = datetime.date.today().strftime('%B %d, %Y');
	message = 'Good morning, today is {} and this is what Háma has to offer:\n\nFood: {}\n\nSoups: {}'.format(today, food, soups);
	
	print('')
	print(message)
	#slack_notify(message);

