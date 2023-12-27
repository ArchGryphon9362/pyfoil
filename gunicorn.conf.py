import threading
from server import inf_loop

def when_ready(_):
    threading.Thread(target=inf_loop, daemon=True).start()
