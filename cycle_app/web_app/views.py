from fastapi import Request
from fastapi.responses import HTMLResponse
from loguru import logger

from cycle_app.web_app import app, templates
from cycle_app.web_app.database import table_handler, database


@app.get('/{user}', response_class=HTMLResponse)
async def main_page(user: int, request: Request):
    database.connect()

    with database.atomic():
        # for i in range(100):
        #     if i % 2 == 0:
        #         status = True
        #     else:
        #         status = False
        #     table_handler.insert(i, status, {4: i})
        select = table_handler.get_active_cycles()
        for x in select:
            logger.info(f'{x}')

    response = templates.TemplateResponse('main_page.html', {'request': request, 'user': user})
    database.close()
    return response
