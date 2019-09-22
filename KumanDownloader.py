# -*- coding:utf-8 -*-
import sys
import os
import requests
import re


def main():
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        print 'Usage:'
        print '%s <target url> [split folder=True]' % __file__
        print 'Example:'
        print '%s http://www.kuman.com/mh-1001733/' % __file__
        print '%s http://www.kuman.com/mh-1001733/ False' % __file__
        return

    url = sys.argv[1]
    split_folder = True
    if len(sys.argv) == 3 and sys.argv[2].lower()[0] == 'f':
        split_folder = False

    ret = requests.get(url)

    # Get title
    title = re.findall(
        '<title>(.*)?</title>',
        ret.content
    )[0].split()[0].strip()[:-6].decode('utf-8')
    if os.path.exists(title) is False:
        os.mkdir(title)
    os.chdir(title)
    print '[*] Title: ' + title

    # Get all chapters
    contents = list(set(
        map(int, re.findall(
                    '<a href="' + url + '(\d*)/" title="',
                    ret.content
                    ))
    ))
    print '[*] Totally %d chapters' % contents[-1]

    count = 0
    # For each chapter
    for i in contents:
        print '[+] Processing chapter %d...' % i,
        folder = ('第%d话' % i).decode('utf-8')

        if split_folder is True:
            count = 0
            if os.path.exists(folder) is False:
                os.mkdir(folder)

        # Get all pictures of this chapter
        pics = re.findall(
            '<img src="(.*?)" data-image_id="',
            requests.get(url + '%d/' % i).content
        )
        print ' [%d pictures]' % len(pics)

        # Save pictures
        for pic in pics:
            path = str(count) + '.' + pic.split('.')[-1].split('!')[0]
            if split_folder is True:
                path = folder + '/' + path
            with open(path, 'wb') as f:
                f.write(requests.get(pic).content)
            count += 1


if __name__ == '__main__':
    main()
