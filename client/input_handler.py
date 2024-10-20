import ast
import asyncio
import pyautogui

# Fonction pour interpréter les événements reçus
# TODO: mettre une queue de asyncio ?
async def read_data(data, logger):
    try:
        while '/' in data:
            line, data = data.split('/', 1)
            line = ast.literal_eval(line.strip())
            asyncio.create_task(process_event(line))
    except KeyError:
        logger.warning("No data received, closing connection.", flush=True)
        raise KeyError('No data received, closing connection.')

# Process the event received
async def process_event(line):
    if line:
        event_type = line['type']
        args = line['args']

        await asyncio.to_thread(getattr(pyautogui, event_type), *args)


   
