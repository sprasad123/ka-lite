# updates the file in static/data/subtitledata/video_srts.json
# can completely remap from Amara API or only re-check the ones
# from our data file that had HTTP errors during the previous API request

import argparse
import datetime
import json
import logging
import os
import pdb
import sys
import time

import requests

import amara_headers

data_path = os.path.dirname(os.path.realpath(
    __file__)) + "/../../static/data/subtitledata/"

logger = logging.getLogger('generate_subtitles_map.py')

headers = amara_headers.headers


class OutDatedSchema(Exception):

    def __str__(value):
        return "The current data schema is outdated and doesn't store the important bits. Please run 'generate_subtitles_map.py -N' to generate a totally new file and the correct schema."


class InvalidDateFormat(Exception):

    def __str__(value):
        return "Invalid date format. Please format your date (-d) flag like this: 'MM/DD/YYYY'"


def create_new_mapping():
    """Write a new JSON file of mappings from YouTube ID to Amara code"""
    nodecache = json.load(open(data_path + '../nodecache.json', 'r'))
    videos = nodecache['Video']
    new_json = {}
    counter = 0
    for video, data in videos.iteritems():
        youtube_id = data['youtube_id']
        new_json.update(update_video_entry(youtube_id))
        # TODO(dylan) 3000+ videos - can't expect process to complete before
        # saving. HELP: is this the best interim step?
        if counter%200 == 0:
            temp_file = "temp_video_srts.json"
            logger.info("On loop %s dumping dictionary into temp file in subtitledata folder: %s" %(str(counter), temp_file))
            with open(data_path + temp_file, 'wb') as fp:
                json.dump(new_json, fp)
        counter += 1
    logger.info("Great success! Stored %s fresh entries.")
    with open(data_path + 'video_srts.json', 'wb') as fp:
        json.dump(new_json, fp)
    logger.info("Deleting temp file....")
    os.remove(data_path + temp_file)


def update_subtitle_map(code_to_check, date_to_check):
    """Update JSON dictionary of subtitle information based on arguments provided"""
    srts_dict = json.loads(open(data_path + "video_srts.json").read())
    for youtube_id, data in srts_dict.items():
        # ensure response code and date exists
        response_code = data.get("api-response")
        last_attempt = data.get("last_attempt")
        if not (response_code or last_attempt):
            raise OutDatedSchema()

        # HELP: why does the below if statement suck so much? does it suck? it feels like it sucks
        # case: -d AND -s
        if date_to_check and code_to_check:
            if date_to_check < last_attempt and code_to_check == "all" or code_to_check == response_code:
                srts_dict.update(update_video_entry(youtube_id))
        # case: -d only
        elif date_to_check and not code_to_check:
            if date_to_check < last_attempt:
                srts_dict.update(update_video_entry(youtube_id))
        # case: -s only
        elif code_to_check and not date_to_check:
            if code_to_check == "all" or code_to_check == response_code:
                srts_dict.update(update_video_entry(youtube_id))


def update_video_entry(youtube_id):
    """Return a dictionary to be appended to the current schema:
            youtube_id: {
                            "amara_code": "3x4mp1e",
                            "language_codes": ["en", "es", "etc"],
                            "api-response": "success",
                            "last_successful_attempt": "2013-07-06 ",
                            "last_attempt": "",
                        }

    """
    request_url = "https://www.amara.org/api2/partners/videos/?format=json&video_url=http://www.youtube.com/watch?v=%s" % (
        youtube_id)
    r = make_request(request_url)
    # add api response first to prevent empty json on errors
    entry = {}
    entry["last_attempt"] = unicode(datetime.datetime.now())
    if r == "client-error" or r == "server-error":
        entry["api-response"] = r
    else:
        entry["api-response"] = "success"
        entry["last_successful_attempt"] = unicode(datetime.datetime.now())
        content = json.loads(r.content)
        # index into data to extract languages and amara code, then add them
        if content.get("objects"):
            languages = json.loads(r.content)['objects'][0]['languages']
            if languages:  # ensuring it isn't an empty list
                amara_code = languages[0].get("subtitles_uri").split("/")[4]
                assert len(amara_code) == 12  # in case of future API change
                entry["amara_code"] = amara_code
                entry["language_codes"] = []
                for language in languages:
                    entry["language_codes"].append(language['code'])
    return entry


def make_request(url):
    """Return response from url; retry up to 5 times for server errors; when returning an error, return human-readable status code."""
    for retries in range(1, 5):
        r = requests.get(url, headers=headers)
        time.sleep(1) # HELP: is this ok on the server?
        if r.status_code > 499:
            logging.warning("Server error: %s at %s" % (
                str(r.status_code), url))
            if retries == 4:
                logging.info(
                    "Maxed out retries: adding %s to bad urls list" % url)
                r = "server-error"
        elif r.status_code > 399:
            logging.warning("Client error: %s at %s" % (
                str(r.status_code), url))
            logging.info("Adding %s to bad urls list" % url)
            r = "client-error"
            break
        else:
            logging.info("Good request: %s at %s" % (str(r.status_code), url))
            break
    return r


def convert_date_input(date_to_convert):
    # convert from MM/DD/YYYY to Unix timestamp to compare against JSON file
    if date_to_convert:
        try:
            converted_date = datetime.datetime.strptime(
                date_to_convert, '%m/%d/%Y')
        except:
            raise InvalidDateFormat()
    return converted_date


def create_parser():
    # parses command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', '--new', action='store_true',
                        help="Force a new mapping. Fetches new data for every one of our videos and overwrites current data with fresh data from Amara. Should really only ever be run once, because it can be updated from then on with '-s all'.")
    parser.add_argument('-r', '--response_code', default=None,
                        help="Which api-response code to recheck. Can be combined with -d. USAGE: '-s all', '-s client-error', or '-s server-error'. ")
    parser.add_argument('-d', '--date_since_attempt',
                        help="Setting a date flag will update only those entries which have not been attempted since that date. Can be combined with -s. This could potentially be useful for updating old subtitles. USAGE: '-d MM/DD/YYYY'")
    return parser


def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s - %(levelname)s: %(message)s',
                        datefmt='%m-%d %H:%M')


if __name__ == '__main__':
    setup_logging()
    parser = create_parser()
    args = parser.parse_args()
    if args.new and not (args.response_code or args.date_since_attempt):
        create_new_mapping()
    elif not args.new and (args.response_code or args.date_since_attempt):
        converted_date = convert_date_input(args.date_since_attempt)
        update_subtitle_map(args.response_code, converted_date)
    else:
        logger.info(
            "Invalid input. Please read the usage instructions more carefully and try again.")
        parser.print_help()
        sys.exit(1)
    logger.info("Process complete.")
    sys.exit(1)