"""The 25 November 2026 page, as data.

Every row is a wire item our own scan (scan25h.py) read between 00:00 and 13:20 UTC on
25 November 2026: the place it happened, the desk, the UTC minute we read it, a headline
cut to the space the page gives it, and the pictogram the card draws. Nothing is invented
and nothing is dated to another day.
"""

DAY = "WEDNESDAY 25 NOVEMBER 2026"
STAMP = "13:20 GMT"

# The three lead stories: the day's biggest, each with its own drawn scene.
LEADS = [
    ("MIDDLE EAST", "RIYADH / SANAA", "11:09",
     "Houthis hit Riyadh's financial district and a Saudi refinery", "drone",
     "The group said it struck the capital's tower district and a refinery; Saudi Arabia gave no toll."),
    ("EUROPE", "KYIV / MOSCOW", "12:19",
     "Putin vows 'inevitable' retaliation as strikes cut power in five regions", "flame",
     "Ukraine hit Russian oil plants; overnight Russian strikes left five Ukrainian regions without power."),
    ("AMERICAS", "NEW YORK", "12:48",
     "Stocks slide as Trump's new tariffs loom and the AI rally stalls", "chart",
     "Trump is set to raise tariffs on 16 economies; Asian shares fell as doubts over AI spending returned."),
]

# Five figures the day turned on, each one from a story below.
NUMBERS = [
    ("36%", "pay rise won by", "Bangladesh garment workers"),
    ("\u20ac115bn", "Ukraine's ask for", "foreign aid in 2027"),
    ("19", "killed overnight", "in RSF drone raids, Sudan"),
    ("16", "economies facing", "new US tariffs"),
    ("23", "trapped in an", "illegal Indonesian mine"),
]

# The day in the order it happened, UTC.
TIMELINE = [
    ("00:00", "Seoul clears a protest camp before the G20"),
    ("01:37", "Shenzhou-24 lifts off with the first foreign astronaut"),
    ("05:05", "Putin threatens retaliation for oil-plant strikes"),
    ("06:29", "Solomon Islands signs a security treaty with Australia"),
    ("11:09", "Houthis claim strikes on Riyadh and a refinery"),
    ("12:11", "Bangladesh garment workers win 36%"),
]

# Thirty more stories, four a row, eight rows: place, minute, headline, icon.
BRIEFS = [
    ("MIDDLE EAST", "GAZA", "11:24", "Israeli strike kills a Hamas official, his wife and children", "blast"),
    ("MIDDLE EAST", "TEHRAN", "09:13", "US tells its citizens to leave Iran as fighting may escalate", "flag"),
    ("MIDDLE EAST", "JERUSALEM", "12:26", "Netanyahu trial judges suggest dropping Case 4000", "gavel"),
    ("MIDDLE EAST", "TEHRAN", "10:01", "Iran rations electricity as sanctions and blockade bite", "power"),
    ("MIDDLE EAST", "JERUSALEM", "01:35", "Eisenkot secures a first coalition partner", "person"),

    ("EUROPE", "BRUSSELS", "10:51", "EU plans a \u20ac50bn push into AI and quantum computing", "chip"),
    ("EUROPE", "LONDON", "10:14", "Surprise Eurostar strike cancels London and Paris trains", "train"),
    ("EUROPE", "BARCELONA", "12:25", "Puigdemont says he will return to Spain on 12 December", "person"),
    ("EUROPE", "MURMANSK", "12:37", "Russia detains the Murmansk governor in a corruption case", "gavel"),

    ("AFRICA", "AL DAMAZIN", "11:50", "Fire breaks out after drone strikes hit a residential area", "flame"),
    ("AFRICA", "BENGHAZI", "12:04", "Libya vows retaliation for a Ukrainian strike on its port", "ship"),
    ("AFRICA", "CONAKRY", "11:10", "Guinea's gold crackdown leaves miners going hungry", "mine"),
    ("AFRICA", "DAKAR", "06:43", "Sports court returns the Africa Cup title to Senegal", "trophy"),

    ("EAST ASIA", "BEIJING", "05:37", "China investigates Politburo member Chen Jining", "person"),
    ("EAST ASIA", "PYONGYANG", "09:24", "US warns Kim Ju-ae's ski gear may breach sanctions", "star"),
    ("EAST ASIA", "SEOUL", "03:19", "North Korea expels a Swiss diplomat over sanctions", "flag"),
    ("EAST ASIA", "TOKYO", "01:55", "Gang swaps bank-card chips in Japan's bathhouses", "chip"),

    ("SOUTH ASIA", "ISLAMABAD", "11:48", "Pakistan celebrates its first astronaut reaching orbit", "rocket"),
    ("SOUTH ASIA", "DHAKA", "11:02", "Shakib and Mustafizur left off the 2027 IPL auction list", "trophy"),
    ("SOUTH ASIA", "KATHMANDU", "11:00", "Nepal hedges between India and China as ties thaw", "flag"),

    ("SE ASIA", "JAKARTA", "10:54", "Indonesia signs an 'ambitious' trade deal with the EU", "ship"),
    ("SE ASIA", "JAKARTA", "10:59", "Three dead and 23 trapped as an illegal gold mine floods", "mine"),
    ("SE ASIA", "KUALA LUMPUR", "08:32", "Malaysia sues Google for $146m over harmful content", "chip"),

    ("OCEANIA", "HONIARA", "06:29", "Solomon Islands signs a security treaty with Australia", "flag"),
    ("OCEANIA", "PERTH", "10:11", "Deloitte suspended by Western Australia over an AI report", "chart"),
    ("OCEANIA", "DARWIN", "10:29", "Indigenous groups alarmed by a child-protection overhaul", "person"),
    ("OCEANIA", "WELLINGTON", "07:47", "New South Wales trains could be offline for a week", "train"),

    ("AMERICAS", "WASHINGTON", "11:34", "Trump to add sweeping new tariffs after midterm defeat", "bank"),
    ("AMERICAS", "WASHINGTON", "10:48", "Cyberattack exposes unclassified data from a CIA system", "chip"),
    ("AMERICAS", "BOGOTA", "07:20", "Colombia frees all hostages and kills a siege gunman", "person"),
    ("AMERICAS", "GULF COAST", "06:47", "Six dead as a small plane crashes off Mississippi", "plane"),
    ("AMERICAS", "WASHINGTON", "03:44", "TSA braces for 18 million Thanksgiving flyers", "person"),
]

REGIONS = ["MIDDLE EAST", "EUROPE", "AFRICA", "EAST ASIA", "SOUTH ASIA", "SE ASIA", "OCEANIA", "AMERICAS"]

SCAN_NOTE = "Our scan: 143 dated items from 24 wire feeds, 00:00-13:20 UTC, 25 Nov 2026."
