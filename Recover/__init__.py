import argparse
import requests
import hashlib
import calendar
import sys
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

DOMAIN_LIST = ['https://vod-secure.twitch.tv', 'https://vod-metro.twitch.tv', 'https://vod-pop-secure.twitch.tv',
               'https://d2e2de1etea730.cloudfront.net', 'https://dqrpb9wgowsf5.cloudfront.net',
               'https://ds0h3roq6wcgc.cloudfront.net', 'https://d2nvs31859zcd8.cloudfront.net',
               'https://d2aba1wr3818hz.cloudfront.net', 'https://d3c27h4odz752x.cloudfront.net',
               'https://dgeft87wbj63p.cloudfront.net', 'https://d1m7jfoe9zdc1j.cloudfront.net',
               'https://d3vd9lfkzbru3h.cloudfront.net', 'https://d2vjef5jvl6bfs.cloudfront.net',
               'https://d1ymi26ma8va5x.cloudfront.net', 'https://d1mhjrowxxagfy.cloudfront.net',
               'https://ddacn6pr5v0tl.cloudfront.net', 'https://d3aqoihi2n8ty8.cloudfront.net',
               'https://dgeft87wbj63p.cloudfront.net']
URL_REGEX_EXPRESSION = "https?://twitchtracker[/:%#\$&\?\(\)~\.=\+\-]+"


def create_parser():
    parser = argparse.ArgumentParser(
        description='twitchtracker 링크로 m3u8를 복구합니다.')
    parser.add_argument('link', help='twitchtracker 방송 링크를 입력해주세요', type=str)

    return parser


def get_m3u8_links(_link):
    from ThreadRunner import ThreadRunner
    match = re.compile(URL_REGEX_EXPRESSION).match(_link)

    if not match:
        raise ValueError('올바른 링크를 입력해주세요')

    link_split = _link.split('/')
    broadcaster_login, stream_id = link_split[3], link_split[5]
    epoch_started_at = get_timestamp(_link)

    value = f'{broadcaster_login}_{stream_id}_{str(epoch_started_at)}'

    sha_hash = hashlib.sha1(value.encode('utf-8')).hexdigest()[:20]

    thread_runner = ThreadRunner()
    thread_runner.run(task, DOMAIN_LIST, broadcaster_login, epoch_started_at, sha_hash, stream_id)


def get_timestamp(_link):
    soup = BeautifulSoup(requests.get(url=_link, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'
    }).text, 'html.parser')

    timestamp = soup.select_one('div.stream-timestamp-dt')

    if timestamp is None:
        raise ValueError('방송 시작 시간을 찾을 수 없습니다.')
    epoch_started_at = calendar.timegm(datetime.strptime(timestamp.text,
                                                         '%Y-%m-%d %H:%M:%S').timetuple())
    return epoch_started_at


def task(domain_list, broadcaster_login, epoch_started_at, sha_hash, stream_id):
    for domain in domain_list:
        m3u8_link = f'{domain}/{sha_hash}_{broadcaster_login}_{stream_id}_{epoch_started_at}/chunked/index-dvr.m3u8'
        if requests.get(url=m3u8_link).status_code == 200:
            print(m3u8_link)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        arg_parser = create_parser()
        link = arg_parser.parse_args().link
        get_m3u8_links(link)
        exit(0)

    get_m3u8_links(input('트위치 트래커 실시간 방송 링크를 입력해주세요 '))
