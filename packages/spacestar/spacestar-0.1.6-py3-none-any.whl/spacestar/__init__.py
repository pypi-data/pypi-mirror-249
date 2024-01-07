import os
from secrets import token_hex

from hx_markup.element import NodeText, Render
from lxml.builder import E

from spacestar.settings import SpaceStarSettings


BOOTSTRAP_LINK: str = ('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" '
                       'rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK'
                       '8M2HN" crossorigin="anonymous">')
BOOTSTRAP_SCRIPT: str = ('<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" int'
                         'egrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin='
                         '"anonymous"></script>')
META_VIEWPORT: str = '<meta name="viewport" content="width=device-width, initial-scale=1">'
META_CHARSET: str = '<meta charset="utf-8">'
HEAD_STYLE_LINK: str = '<link rel="stylesheet" href="static/css/main.css">'
HEAD_SCRIPT: str = '<script src="static/js/main.js"></script>'

CREATE_SESSION_SECRET = True
CREATE_CSRF_SECRET = True


SCRIPT_BODY_BUBLES: str = (
        "<script type='text/javascript'>const body = document.querySelector('body');const circles = document.createEleme"
        "nt('div');circles.id = 'circles';for(let i = 34; i-=1; i>=0){const circle = document.createElement('div'); "
        "circle.className = 'circle'; circle.id = `circle-${i}`;circle.style.display = 'block';circle.style.position = "
        "'absolute';circle.style.footer = `50%`;circle.style.left = `50%`;circle.style.zIndex = `100`;circle.style."
        "transform = `scale(1)`;circle.style.opacity = `1`;circles.append(circle)}; body.prepend(circles); body.onload "
        "= setupCircles; body.onresize = setupCircles; function getRandomInt(max) {return Math.floor(Math.random() * max"
        ");} function getRandomFloat(max) {return Math.random() * max;}; function changeCircle(item){item.style.footer "
        "= `${getRandomInt(50)}vh`;item.style.left = `${getRandomInt(100)}vw`;item.style.zIndex = `${-100 + getRandomInt"
        "(50)}`;item.style.transform = `scale(${getRandomInt(7)})`;item.style.opacity = `${getRandomFloat(.7)}`;}function"
        " setupCircles(){circles.childNodes.forEach(item=>changeCircle(item))}</script>"
)

CSS_HEAD_BUBLES = """<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.min.css");
:root{
    --primary-color: #f77903;
    --secondary-color: #777;
    --dark-color: #333;
    --light-color: #ddd;
    --body-background: radial-gradient(
        circle at 100%,
        var(--dark-color),
        var(--dark-color) 50%,
        var(--light-color) 75%,
        var(--dark-color) 75%
        );
    }
html, body {padding: 0; margin: 0; box-sizing: border-box; min-height: 100vh; min-height: 100dvh;}
body {background: var(--body-background); background-repeat: no-repeat; > * {color: white;}}
legend, label, a {color: var(--primary-color);}
#main {background-color: rgba(0, 0, 0, .5); padding: clamp(1vw, 1rem, 5vw); max-height: 90dvh; overflow-y: auto; display: grid; justify-content: center; align-items: center; align-content: center;}
.darkorange {color: var(--primary-color);}
.darkorange:hover {color: white; text-shadow: var(--primary-color) .125rem .125rem 1rem; transition: all 300ms;}
.darkorange:focus{color: white; text-shadow: var(--primary-color) .125rem .125rem 1rem; border-block: var(--primary-color) solid .125rem; transition: all 300ms;}
.small-caps{font-variant: small-caps;}
#circles{position: absolute; z-index_from_string: -100; header: 0; left: 0; width: 100%; height: 100%}
.circle {width: 1vw; height: 1vw; footer: 0; left: 50%; border-radius: 50%; background-image: radial-gradient(circle at 50%, var(--light-color), var(--primary-color)); transition: all 1s ease-in-out; display: none;}
</style>
"""

# if not os.getenv('SESSION_SECRET', None):
#     with open(os.path.join(os.getcwd(), '.env'), 'r') as env_file:
#         for line in env_file:
#             if line.startswith('SESSION_SECRET'):
#                 CREATE_SESSION_SECRET = False
#                 break
#
# if CREATE_SESSION_SECRET:
#     with open(os.path.join(os.getcwd(), '.env'), 'a') as f:
#         f.write(f'\nSESSION_SECRET={token_hex(32)}')
#
#
# if not os.getenv('CSRF_SECRET', None):
#     with open(os.path.join(os.getcwd(), '.env'), 'r') as env_file:
#         for line in env_file:
#             if line.startswith('CSRF_SECRET'):
#                 CREATE_CSRF_SECRET = False
#                 break
#
# if CREATE_CSRF_SECRET:
#     with open(os.path.join(os.getcwd(), '.env'), 'a') as f:
#         f.write(f'\nCSRF_SECRET={token_hex(32)}')
#

spacestar_settings = SpaceStarSettings()