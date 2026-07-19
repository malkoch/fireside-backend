from fastapi.templating import Jinja2Templates

from web.core.filters import FILTERS


templates = Jinja2Templates(directory='web/templates')
for name, func in FILTERS.items():
    templates.env.filters[name] = func
