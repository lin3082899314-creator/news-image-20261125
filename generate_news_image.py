#!/usr/bin/env python3
"""Generate one newspaper front-page image summing up 25 November 2026 world news.

Entry for make.fun bounty "Sum up 25 November's world news in one image"
(news-image-20261125, $100, 50 places, closes 27 Nov 2026 08:00 CST).

Run:  python3 generate_news_image.py
Out:   world-news-25-nov-2026.png  (1800 x 2600)

All 24 stories are dated 25 Nov 2026 in the cited reporting (AP, Reuters,
Just Security, The Jerusalem Post, Anadolu Agency, Xinhua, PINA,
La Mediterranee, NEXA). Preliminary/claimed items are attributed in the
text ("says", "reports say", "according to").
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1800, 3600  # cropped to content after drawing
M = 64  # margin
BG = (250, 248, 242)      # newsprint
INK = (18, 18, 18)
RED = (158, 27, 27)
GREY = (90, 86, 80)
RULE = (60, 58, 52)
ACCENT = (31, 58, 95)     # deep blue for section bars

F_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# (region, headline, summary, source)
LEADS = [
    ("MIDDLE EAST  ·  LEAD",
     "Tankers ablaze in Hormuz: mines strike two ships as Iran war widens",
     "Iran's Revolutionary Guard said two oil tankers struck naval mines, exploded "
     "and caught fire in the Strait of Hormuz, saying the vessels had tried to use "
     "an unauthorised route. The attack raises the stakes for shipping and energy markets.",
     "IRGC / Just Security"),
    ("MARKETS  ·  LEAD",
     "Trump's tariff bombshell: new levies on 14 partners, China hit hardest",
     "Washington proposed fresh tariffs on 14 major trading partners to counter what "
     "it calls structural excess factory capacity, with the steepest rates aimed at "
     "China. US stock futures slid, with the Nasdaq 100 down 3.1%.",
     "Reuters"),
]

SECTIONS = [
    ("NORTH AMERICA", [
        ("US jury convicts Huawei of trade-secret theft",
         "A federal jury found Huawei guilty of conspiracy to steal trade secrets and bank fraud over its Iran business, but cleared it of the overarching racketeering charge.", "Reuters"),
        ("US consumer confidence at near two-year high",
         "American consumer confidence jumped to its highest level in nearly two years heading into the holidays, despite rising turkey prices.", "Reuters"),
        ("Trump spares turkeys Freedom and Feathers",
         "The president spared turkeys Freedom and Feathers from the Thanksgiving table in the traditional White House pardon.", "Reuters"),
        ("Thanksgiving storm bears down on East Coast",
         "A storm is set to bring rain and strong winds to the US East Coast over the Thanksgiving holiday, forecasters said.", "Reuters"),
        ("Abrego Garcia leaves the US for Spain",
         "Salvadoran migrant Kilmar Abrego Garcia left the United States for Spain, ending a long-running deportation case.", "Reuters"),
    ]),
    ("EUROPE", [
        ("Zelenskyy awaits date for four-way peace talks",
         "Ukraine is waiting for the US to set a date for a new round of peace talks with Russia that would include European partners for the first time.", "Anadolu / RBC-Ukraine"),
        ("Poland plans no-fly zone on Ukraine border",
         "Poland is planning a no-fly zone along its border with Ukraine to strengthen NATO's eastern flank after airspace violations.", "Reuters"),
        ("Union strikes disrupt Eurostar trains",
         "Strikes disrupted Eurostar services and travel connecting France and Britain, stranding passengers ahead of the holiday.", "La Mediterranee"),
        ("BBC journalists strike over cuts and workload",
         "BBC journalists took industrial action over reductions in staff and rising workloads, the union said.", "La Mediterranee"),
    ]),
    ("MIDDLE EAST", [
        ("Houthis say they hit Saudi oil refinery",
         "Yemen's Houthis said they attacked Saudi Arabia's Ras Tanura oil refinery, causing fires, as the regional war widened.", "Just Security"),
        ("Houthis say they struck two Saudi ports",
         "The Houthis said they hit the Saudi ports of Jeddah and Jazan in response to coalition strikes on the Red Sea port of Hodeida.", "Times of Israel"),
        ("Israel kills Hamas security colonel in Gaza",
         "Israel's military killed Hamas colonel Mohammad Abuelouf, who headed the militants' interior security service, along with his wife and two children, Gaza medics said.", "Just Security"),
        ("IS attack kills two Syrian officers in Hasaka",
         "An Islamic State attack killed two Syrian internal security personnel and wounded five others in the northeastern city of Hasaka, state media said.", "Reuters"),
        ("Saudi national kidnapped by suspected IS in Niger",
         "Militants suspected to be from an Islamic State affiliate kidnapped a Saudi national in Niger at the weekend and are holding the person hostage, sources said.", "Reuters"),
    ]),
    ("ASIA-PACIFIC", [
        ("Shenzhou-24 docks; Pakistani joins Tiangong crew",
         "China's Shenzhou-24 docked at the Tiangong station, making Pakistan's Zeeshan Ali the first foreign astronaut aboard a Chinese crewed mission.", "Reuters / Xinhua"),
        ("Solomons sign treaty barring foreign bases",
         "Australia and Solomon Islands signed a landmark treaty that would preclude a foreign military or security base on the islands.", "PINA / Just Security"),
        ("Japan aims to be world's No. 3 AI power",
         "Japan's government intends to position itself as one of the world's top three AI forces after the United States and China.", "La Mediterranee"),
        ("Seoul watches N. Korea vessel near sea border",
         "South Korea is watching troop activities after a North Korean vessel labelled a coast-guard ship was located near the Northern Limit Line.", "La Mediterranee"),
    ]),
    ("AFRICA & LATIN AMERICA", [
        ("30 killed as fuel tanker sets Cairo road ablaze",
         "At least 30 people were killed when a fuel tanker crashed and caught fire on Cairo's ring road.", "Standard Topic"),
        ("Ramaphosa impeachment threat lifted in court",
         "A Cape Town court removed the impeachment threat against President Cyril Ramaphosa over the 'farmgate' scandal.", "No Bullshit Follows"),
        ("Mexico used US drones to catch 'El Chapo Isidro'",
         "Mexico used American drones to capture suspected drug trafficker known as 'El Chapo Isidro', officials said.", "La Mediterranee"),
    ]),
    ("TECH, SCIENCE & MARKETS", [
        ("AI trade collapses again as Nvidia relapses",
         "A day after Nvidia surged on Jensen Huang's return, the AI trade collapsed again: the Nasdaq fell 1.5% and Nvidia gave back about 6%.", "Reuters"),
        ("Anthropic sinks below its $83 IPO price",
         "Anthropic shares tumbled below their $83 IPO price days after the largest listing in history, on track to lose nearly $200bn in value.", "Reuters"),
        ("Microsoft declares 'Code Red' after outage",
         "Microsoft declared a 'Code Red' after a historic outage, internal memos show, as retailers brace for AI cyberattacks ahead of Black Friday.", "Reuters"),
    ]),
]

ALSO = [
    ("SUDAN", "Paramilitary drone strikes kill 19 civilians and wound 20 more in two cities, a Sudanese rights group said."),
    ("VATICAN", "Pope Leo XIV laments the failure of the UN COP31 climate talks to reach an agreement."),
    ("JERUSALEM", "Israeli judges suggest dropping a key corruption case against Prime Minister Benjamin Netanyahu."),
    ("MUSIC", "Duran Duran guitarist Andy Taylor dies aged 65."),
]

SOURCES = ("Sources: AP · Reuters · Just Security · The Jerusalem Post · Anadolu Agency · "
           "RBC-Ukraine · Xinhua · PINA · La Mediterranee · Standard Topic · NEXA · "
           "No Bullshit Follows (2026-11-25). Claims marked 'says / reported' are "
           "attributed and preliminary. All stories dated 25 November 2026.")

# ---------------------------------------------------------------- drawing
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- masthead
f_mast = font(F_SERIF_B, 96)
f_sub = font(F_SANS, 26)
f_date = font(F_SANS_B, 27)
y = 58
d.text((M, y), "THE WORLD IN ONE PAGE", font=f_mast, fill=INK)
y += 118
d.line([(M, y), (W - M, y)], fill=RULE, width=3)
y += 14
d.text((M, y), "WEDNESDAY, 25 NOVEMBER 2026", font=f_date, fill=INK)
right = "24 STORIES  ·  6 REGIONS"
d.text((W - M - d.textlength(right, font=f_date), y), right, font=f_date, fill=RED)
y += 44
d.line([(M, y), (W - M, y)], fill=RULE, width=3)
y += 26

# --- lead stories, two columns
col_w = (W - 2 * M - 48) // 2
f_kick = font(F_SANS_B, 24)
f_lead_h = font(F_SERIF_B, 40)
f_lead_b = font(F_SERIF, 26)
lead_top = y
lead_bottom = lead_top
for i, (kick, head, body, src) in enumerate(LEADS):
    x = M + i * (col_w + 48)
    yy = lead_top
    d.text((x, yy), kick, font=f_kick, fill=RED)
    yy += 38
    yy = draw_wrapped(d, x, yy, head, f_lead_h, col_w, leading=50)
    yy += 10
    yy = draw_wrapped(d, x, yy, body, f_lead_b, col_w, leading=35)
    yy += 8
    d.text((x, yy), "— " + src, font=font(F_SANS, 21), fill=GREY)
    lead_bottom = max(lead_bottom, yy + 30)
d.line([(M, lead_bottom), (W - M, lead_bottom)], fill=RULE, width=2)
y = lead_bottom + 22

# --- "also on 24 November" strip
f_also_h = font(F_SANS_B, 24)
d.text((M, y), "ALSO ON 25 NOVEMBER", font=f_also_h, fill=ACCENT)
y += 40
f_also_k = font(F_SANS_B, 22)
f_also_t = font(F_SERIF, 23)
also_bottom = y
for i, (k, t) in enumerate(ALSO):
    x = M + i * ((W - 2 * M) // 4)
    w = (W - 2 * M) // 4 - 28
    yy = y
    d.text((x, yy), k, font=f_also_k, fill=RED)
    yy += 32
    yy = draw_wrapped(d, x, yy, t, f_also_t, w, leading=30)
    also_bottom = max(also_bottom, yy)
y = also_bottom + 18
d.line([(M, y), (W - M, y)], fill=RULE, width=2)
y = y + 24

# --- body: 3 columns, sections assigned to balance height
cols = [[0, 1], [2, 5], [3, 4]]  # section indices per column
f_sec = font(F_SANS_B, 28)
f_num = font(F_SANS_B, 26)
f_head = font(F_SERIF_B, 27)
f_body = font(F_SERIF, 22)
f_src = font(F_SANS, 19)
body_top = y
n = 1
col_x = [M, M + (W - 2 * M) // 3 + 16, M + 2 * (W - 2 * M) // 3 + 32]
col_wid = (W - 2 * M) // 3 - 32
body_bottom = body_top
for ci, sec_idx in enumerate(cols):
    x = col_x[ci]
    yy = body_top
    for si in sec_idx:
        sec, stories = SECTIONS[si]
        # section bar
        d.rectangle([x, yy, x + col_wid, yy + 44], fill=ACCENT)
        d.text((x + 14, yy + 6), sec, font=f_sec, fill=(255, 255, 255))
        yy += 44 + 14
        for head, body, src in stories:
            d.text((x, yy), f"{n:02d}", font=f_num, fill=RED)
            hx = x + 52
            hw = col_wid - 52
            yy2 = draw_wrapped(d, hx, yy, head, f_head, hw, leading=32)
            yy2 = draw_wrapped(d, hx, yy2 + 3, body, f_body, hw, leading=27)
            yy2 += 3
            d.text((hx, yy2), src.upper(), font=f_src, fill=GREY)
            yy = yy2 + 20
            n += 1
        yy += 4
    body_bottom = max(body_bottom, yy)
    # column rule
    if ci < 2:
        d.line([(x + col_wid + 16, body_top), (x + col_wid + 16, body_bottom)], fill=(200, 196, 188), width=1)

# --- footer, placed after the tallest column
fy = body_bottom + 26
d.line([(M, fy), (W - M, fy)], fill=RULE, width=2)
fy += 16
fy = draw_wrapped(d, M, fy, SOURCES, font(F_SANS, 20), W - 2 * M, fill=GREY, leading=27)
fy += 10
d.text((M, fy), "THE WORLD IN ONE PAGE  ·  25 NOVEMBER 2026  ·  Generated by a program for the make.fun news-image bounty",
       font=font(F_SANS_B, 20), fill=INK)
fy += 34

img = img.crop((0, 0, W, fy + 24))
img.save("world-news-25-nov-2026.png")
print("saved world-news-25-nov-2026.png", img.size, "stories:", n - 1)
