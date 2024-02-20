from mailingstat.celery import app

from .mailing_to_clients import MailingProcesser
from mailing.models import Mailing

import asyncio


@app.task
def send_mailing_task(mailing_id: int) -> None:
    def run_async_mailing():
        # Ensure an event loop is available in this thread
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as e:
            if "There is no current event loop in thread" in str(e):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            else:
                raise

        async def async_mailing():
            mailing = await Mailing.objects.aget(pk=mailing_id)
            mailing_processer = MailingProcesser(mailing=mailing)
            await mailing_processer.process_mailing()

        loop.run_until_complete(async_mailing())

    run_async_mailing()