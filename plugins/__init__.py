#_________mdbotz___________________#
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import IMDB_TEMPLATE
CALCULATE_TEXT = "Made by @FayasNoushad"
CALCULATE_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("DEL", callback_data="DEL"),
        InlineKeyboardButton("AC", callback_data="AC"),
        InlineKeyboardButton("(", callback_data="("),
        InlineKeyboardButton(")", callback_data=")")
        ],[
        InlineKeyboardButton("7", callback_data="7"),
        InlineKeyboardButton("8", callback_data="8"),
        InlineKeyboardButton("9", callback_data="9"),
        InlineKeyboardButton("÷", callback_data="/")
        ],[
        InlineKeyboardButton("4", callback_data="4"),
        InlineKeyboardButton("5", callback_data="5"),
        InlineKeyboardButton("6", callback_data="6"),
        InlineKeyboardButton("×", callback_data="*")
        ],[
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
        InlineKeyboardButton("3", callback_data="3"),
        InlineKeyboardButton("-", callback_data="-"),
        ],[
        InlineKeyboardButton(".", callback_data="."),
        InlineKeyboardButton("0", callback_data="0"),
        InlineKeyboardButton("=", callback_data="="),
        InlineKeyboardButton("+", callback_data="+"),
        ]]
    )

CAPTION = InlineKeyboardMarkup([[InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://t.me/venombotupdates')]])


FORMAT= IMDB_TEMPLATE.format(

            h,

            title = imdb['title'],

            votes = imdb['votes'],

            aka = imdb["aka"],

            seasons = imdb["seasons"],

            box_office = imdb['box_office'],

            localized_title = imdb['localized_title'],

            kind = imdb['kind'],

            imdb_id = imdb["imdb_id"],

            cast = imdb["cast"],

            runtime = imdb["runtime"],

            countries = imdb["countries"],

            certificates = imdb["certificates"],

            languages = imdb["languages"],

            director = imdb["director"],

            writer = imdb["writer"],

            producer = imdb["producer"],

            composer = imdb["composer"],

            cinematographer = imdb["cinematographer"],

            music_team = imdb["music_team"],

            distributors = imdb["distributors"],

            release_date = imdb['release_date'],

            year = imdb['year'],

            genres = imdb['genres'],

            poster = imdb['poster'],

            plot = imdb['plot'],

            rating = imdb['rating'],

            url = imdb['url'],

            **locals()

        )
