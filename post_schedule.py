#! /usr/bin/env python

import config
from slack_helper import SlackHelper
from sheet_helper import GSheetHelper

from datetime import datetime

sh = SlackHelper(config.SLACK_TOKEN)

gh = GSheetHelper(config.CREDENTIALS_FILE)

# Read meta tab
meta_rows = gh.get_rows(config.WORKBOOK, config.WORKSHEET_META_TAB)

for row in meta_rows:
    tab, message, date_col, user_cols = [row[x] for x in ('Tab', 'Message', 'Date Column', 'User Columns')]
    print tab, message, date_col, user_cols

    msg = message + '\n'
    today = datetime.today()
    all_rows = gh.get_rows(config.WORKBOOK, tab)
    for i, rowmap in enumerate(all_rows):
        current = False
        if i+1 < len(all_rows):
            # TODO: Make date more generic
            curr_date = datetime.strptime(rowmap[date_col], "%m/%d/%Y")
            next_date = datetime.strptime(all_rows[i+1][date_col], "%m/%d/%Y")
            if today >= curr_date and today < next_date:
                current = True
                print 'Current:', rowmap[date_col]

        if current:
            for squad in user_cols.split(','):
                squad = squad.strip()
                msg += squad + ': ' + '@' + sh.get_username_for_fullname(rowmap[squad])  + '\n'

    sh.send_message(msg, config.USERNAME, config.CHANNEL, config.ICON_URL)
