#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import pytest

import pyrogram
from pyrogram import raw
from pyrogram.parser import Parser
from pyrogram.parser.html import HTML


# expected: the expected unparsed HTML
# text: original text without entities
# entities: message entities coming from the server

def test_html_unparse_bold():
    expected = "<b>bold</b>"
    text = "bold"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BOLD, offset=0, length=4)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_italic():
    expected = "<i>italic</i>"
    text = "italic"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.ITALIC, offset=0, length=6)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_underline():
    expected = "<u>underline</u>"
    text = "underline"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.UNDERLINE, offset=0, length=9)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_strike():
    expected = "<s>strike</s>"
    text = "strike"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.STRIKETHROUGH, offset=0, length=6)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_spoiler():
    expected = "<spoiler>spoiler</spoiler>"
    text = "spoiler"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.SPOILER, offset=0, length=7)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_url():
    expected = '<a href="https://pyrogram.org/">URL</a>'
    text = "URL"
    entities = pyrogram.types.List([pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.TEXT_LINK,
                                                                 offset=0, length=3, url='https://pyrogram.org/')])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_code():
    expected = '<code>code</code>'
    text = "code"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.CODE, offset=0, length=4)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_pre():
    expected = """<pre language="python">for i in range(10):
    print(i)</pre>"""

    text = """for i in range(10):
    print(i)"""

    entities = pyrogram.types.List([pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.PRE, offset=0,
                                                                 length=32, language='python')])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_mixed():
    expected = "<b>aaaaaaa<i>aaa<u>bbbb</u></i></b><u><i>bbbbbbccc</i></u><u>ccccccc<s>ddd</s></u><s>ddddd<spoiler>dd" \
               "eee</spoiler></s><spoiler>eeeeeeefff</spoiler>ffff<code>fffggggggg</code>ggghhhhhhhhhh"
    text = "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhh"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BOLD, offset=0, length=14),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.ITALIC, offset=7, length=7),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.UNDERLINE, offset=10, length=4),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.UNDERLINE, offset=14, length=9),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.ITALIC, offset=14, length=9),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.UNDERLINE, offset=23, length=10),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.STRIKETHROUGH, offset=30, length=3),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.STRIKETHROUGH, offset=33, length=10),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.SPOILER, offset=38, length=5),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.SPOILER, offset=43, length=10),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.CODE, offset=57, length=10)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_escaped():
    expected = "<b>&lt;b&gt;bold&lt;/b&gt;</b>"
    text = "<b>bold</b>"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BOLD, offset=0, length=11)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_escaped_nested():
    expected = "<b>&lt;b&gt;bold <u>&lt;u&gt;underline&lt;/u&gt;</u> bold&lt;/b&gt;</b>"
    text = "<b>bold <u>underline</u> bold</b>"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BOLD, offset=0, length=33),
         pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.UNDERLINE, offset=8, length=16)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_no_entities():
    expected = "text"
    text = "text"
    entities = []

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_custom_emoji():
    expected = '<emoji id="6307513400956030852">💵</emoji>'
    text = "💵"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(
            type=pyrogram.enums.MessageEntityType.CUSTOM_EMOJI,
            offset=0,
            length=2,
            custom_emoji_id=6307513400956030852
        )])

    assert HTML.unparse(text=text, entities=entities) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "markup",
    [
        '<emoji id="6307513400956030852">💵</emoji>',
        '<tg-emoji emoji-id="6307513400956030852">💵</tg-emoji>',
    ]
)
async def test_html_parse_custom_emoji_syntaxes(markup):
    parsed = await HTML(None).parse(markup)

    assert parsed["message"] == "💵"
    assert len(parsed["entities"]) == 1

    entity = parsed["entities"][0]
    assert isinstance(entity, raw.types.MessageEntityCustomEmoji)
    assert entity.offset == 0
    assert entity.length == 2
    assert entity.document_id == 6307513400956030852


@pytest.mark.asyncio
async def test_html_parse_bot_api_custom_emoji_uses_utf16_offsets():
    parsed = await HTML(None).parse(
        '😀余额：<tg-emoji emoji-id="6307513400956030852">💵</tg-emoji>10'
    )

    assert parsed["message"] == "😀余额：💵10"

    entity = parsed["entities"][0]
    assert entity.offset == 5
    assert entity.length == 2
    assert entity.document_id == 6307513400956030852


@pytest.mark.asyncio
async def test_default_parse_mode_supports_nested_bot_api_custom_emoji():
    parsed = await Parser(None).parse(
        '<b>余额：<tg-emoji emoji-id="6307513400956030852">💵</tg-emoji></b>',
        pyrogram.enums.ParseMode.DEFAULT
    )

    assert parsed["message"] == "余额：💵"
    assert any(
        isinstance(entity, raw.types.MessageEntityBold)
        for entity in parsed["entities"]
    )

    custom_emoji = next(
        entity
        for entity in parsed["entities"]
        if isinstance(entity, raw.types.MessageEntityCustomEmoji)
    )
    assert custom_emoji.offset == 3
    assert custom_emoji.length == 2
    assert custom_emoji.document_id == 6307513400956030852


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "markup",
    [
        "<tg-emoji>💵</tg-emoji>",
        '<tg-emoji emoji-id="not-a-number">💵</tg-emoji>',
    ]
)
async def test_html_parse_invalid_custom_emoji_keeps_fallback_text(markup):
    parsed = await HTML(None).parse(markup)

    assert parsed == {
        "message": "💵",
        "entities": None
    }
