import uvicorn

from cycle_app.web_app.settings import settings


if __name__ == '__main__':
    uvicorn.run(
        'cycle_app.web_app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
        use_colors=True
    )
