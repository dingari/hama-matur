# Háma matur

This is a small script that scrapes information about the daily lunch menu in Háma (University of Iceland's canteen) and informs the user.

This was written as more of a novelty when I was working on campus, but might be handy for someone.

## Requirements

This project requires PhantomJS to be installed (http://phantomjs.org/) and the path to the executable be set up in the `config.ini` file as such

    [phantomjs]
    path = C:/path/to/phantomjs/folder/phantomjs.exe

## Usage

Simply run the `hama_matur.py` script

## TODO

* Add config template
* Add support for PhantomJS environment variable lookup
* Scrape more information from the site (such as Háma Heimshorn menu)
* Add command line flags for more versatile configuration (e.g. --loop-forever, --print-results, --slack-message)
* Add more ways of getting alerts (email, etc.)
