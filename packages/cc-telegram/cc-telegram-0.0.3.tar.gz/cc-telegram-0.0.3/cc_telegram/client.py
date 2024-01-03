#!/usr/bin/env python3

import asyncio
import prettytable as pt
import tracemalloc
from telegram import Bot
from telegram.constants  import ParseMode
from telegram.ext import CallbackContext, Updater


tracemalloc.start()


class TeleGramClient:

    def __init__(self, api_key, chat_id):
        self.api_key = api_key
        self.chat_id = chat_id
        self.session = self._create_session()
    
    def _create_session(self):
        return Bot(token=self.api_key)
    
    def send_message_markdown(self, message):
        asyncio.run(self.session.send_message(chat_id=self.chat_id, text=message, parse_mode=ParseMode.MARKDOWN_V2))

    def send_message_html(self, message, topic_id):
        if isinstance(message, list):
            message = ''.join(message)
        if topic_id:
            asyncio.run(self.session.send_message(chat_id=self.chat_id, text=message, parse_mode=ParseMode.HTML, message_thread_id=topic_id))
        else:
            asyncio.run(self.session.send_message(chat_id=self.chat_id, text=message, parse_mode=ParseMode.HTML))

    def send_table(self, update: Updater=Updater, context: CallbackContext=CallbackContext):
        table = pt.PrettyTable(['Symbol', 'Price', 'Change'])
        table.align['Symbol'] = 'l'
        table.align['Price'] = 'r'
        table.align['Change'] = 'r'
        data = [
            ('ABC', 20.85, 1.626),
            ('DEF', 78.95, 0.099),
            ('GHI', 23.45, 0.192),
            ('JKL', 98.85, 0.292),
        ]
        for symbol, price, change in data:
            table.add_row([symbol, f'{price:.2f}', f'{change:.3f}'])
        
        update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)
        # or use markdown
        update.message.reply_text(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

if __name__ == '__main__':
    api_key = '111111:XXXX'
    chat_id = '-11111'
    tg_client = TeleGramClient(api_key=api_key, chat_id=chat_id)

    message = [
        f'<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji><b>服务器开机提醒</b>\n\n',
        f'<b>hostname</b>: test\n',
        f'<b>ip</b>: test\n',
    ]

    tg_client.send_message_html(message)
