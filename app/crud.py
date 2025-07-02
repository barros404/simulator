from .models import Log
from .monitor import enviar_debug

async def insert_log(session, log_data):
    new_log = Log(data=log_data.data)
    session.add(new_log)
    await session.commit()
    await session.refresh(new_log)

    await enviar_debug(f"LOG INSERIDO: {new_log.data}")

    return new_log
