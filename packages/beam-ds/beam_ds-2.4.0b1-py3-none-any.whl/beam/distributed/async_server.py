import json
import time
from threading import Thread
import io

from .dispatcher import BeamDispatcher
from .worker import BeamWorker
from ..serve.http_server import HTTPServer
from ..serve.server import BeamServer
from ..logger import beam_logger as logger
import websockets
import asyncio
from celery.result import AsyncResult
from flask import request, jsonify, send_file
from ..utils import ThreadSafeDict, find_port


class AsyncServer(HTTPServer):

    def __init__(self, obj, routes=None, name=None, broker=None, backend=None,
                 broker_username=None, broker_password=None, broker_port=None, broker_scheme=None, broker_host=None,
                 backend_username=None, backend_password=None, backend_port=None, backend_scheme=None,
                 backend_host=None, use_torch=True, batch=None, max_wait_time=1.0, max_batch_size=10,
                 tls=False, n_threads=4, application=None, postrun=None, ws_tls=False,
                 n_workers=1, broker_log_level='INFO', **kwargs):

        if routes is None:
            routes = []
        self.worker = BeamWorker(obj, *routes, name=name, n_workers=n_workers, daemon=True,
                                 broker=broker, backend=backend,
                                 broker_username=broker_username, broker_password=broker_password,
                                 broker_port=broker_port,
                                 broker_scheme=broker_scheme, broker_host=broker_host,
                                 backend_username=backend_username, backend_password=backend_password,
                                 backend_port=backend_port,
                                 backend_scheme=backend_scheme,
                                 backend_host=backend_host, log_level=broker_log_level)

        predefined_attributes = {k: 'method' for k in self.worker.routes}
        self.dispatcher = BeamDispatcher(name=self.worker.name, broker=broker, backend=backend,
                                         broker_username=broker_username, broker_password=broker_password,
                                         broker_port=broker_port, broker_scheme=broker_scheme, broker_host=broker_host,
                                         backend_username=backend_username, backend_password=backend_password,
                                         backend_port=backend_port, backend_scheme=backend_scheme,
                                         backend_host=backend_host, serve='remote', log_level=broker_log_level)

        application = application or 'distributed_async'
        super().__init__(obj=self.dispatcher, name=name, use_torch=use_torch, batch=batch,
                        max_wait_time=max_wait_time, max_batch_size=max_batch_size,
                        tls=tls, n_threads=n_threads, application=application,
                        predefined_attributes=predefined_attributes, **kwargs)

        self.app.add_url_rule('/poll/<client>/', view_func=self.poll)

        self.tasks = ThreadSafeDict()
        self.ws_clients = ThreadSafeDict()
        # task_postrun.connect(self.postprocess)

        if ws_tls:
            import ssl
            # Create an SSL context for wss
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            # self.ssl_context.load_cert_chain(certfile='path/to/cert.pem', keyfile='path/to/key.pem')
        else:
            self.ssl_context = None

        self.ws_application = 'ws' if not ws_tls else 'wss'
        self.ws_port = None

        if postrun is None:
            self.postrun_callback = self.postrun
        else:
            self.postrun_callback = postrun

    def poll(self, client):

        task_id = request.args.get('task_id')
        result = self.dispatcher.poll(task_id)

        if client == 'beam':
            io_results = io.BytesIO()
            self.dump_function(result, io_results)
            io_results.seek(0)
            return send_file(io_results, mimetype="text/plain")
        else:
            return jsonify(result)

    async def websocket_handler(self, ws):
        # Wait for the client to send its client_id

        client_id = await ws.recv()
        logger.info(f"New WebSocket client connected: {client_id}")
        self.ws_clients[client_id] = ws
        await ws.wait_closed()
        # self.ws_clients.pop(client_id)

    def run_ws_server(self, host, port):

        logger.info("Starting...")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        start_server = websockets.serve(self.websocket_handler, host, port, ssl=self.ssl_context)
        loop.run_until_complete(start_server)
        loop.run_forever()

    def run(self, ws_host=None, ws_port=None, enable_websocket=True, **kwargs):

        self.worker.run()

        if enable_websocket:
            if ws_host is None:
                ws_host = "0.0.0.0"
            ws_port = find_port(port=ws_port, get_port_from_beam_port_range=True, application=self.ws_application)
            self.ws_port = ws_port
            logger.info(f"Opening a Websocket ({self.ws_application}) serve on port: {ws_port}")

            # Run the WebSocket server as an asyncio task
            Thread(target=self.run_ws_server, args=(ws_host, ws_port)).start()

        super().run(non_blocking=True, **kwargs)

        while True:
            try:
                sleep = True
                for task_id in self.tasks.keys():
                    res = AsyncResult(task_id)
                    if res.ready():
                        sleep = False
                        task_inf = self.tasks.pop(task_id)
                        self.postprocess(task_id=task_id, task=res, task_inf=task_inf)
                if sleep:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt, exiting...")
                break

    @property
    def metadata(self):
        return {'ws_application': self.ws_application, 'ws_port': self.ws_port}

    def query_algorithm(self, client, method, *args, **kwargs):

        if client == 'beam':
            postrun_args = request.files['postrun_args']
            postrun_kwargs = request.files['postrun_kwargs']
            args = request.files['args']
            kwargs = request.files['kwargs']
            ws_client_id = request.files['ws_client_id']

            postrun_args = self.load_function(postrun_args)
            postrun_kwargs = self.load_function(postrun_kwargs)
            ws_client_id = self.load_function(ws_client_id)

        else:
            data = request.get_json()
            postrun_args = data.pop('postrun_args', [])
            postrun_kwargs = data.pop('postrun_kwargs', {})
            ws_client_id = data.pop('ws_client_id', None)

            args = data.pop('args', [])
            kwargs = data.pop('kwargs', {})

        if method not in ['poll']:
            task_id = BeamServer.query_algorithm(self, client, method, args, kwargs, return_raw_results=True)
            if type(task_id) is not str:
                print(task_id)
            metadata = self.request_metadata(client=client, method=method)
            self.tasks[task_id] = {'metadata': metadata, 'postrun_args': postrun_args,
                                   'postrun_kwargs': postrun_kwargs, 'ws_client_id': ws_client_id}

            if client == 'beam':
                io_results = io.BytesIO()
                self.dump_function(task_id, io_results)
                io_results.seek(0)
                return send_file(io_results, mimetype="text/plain")
            else:
                return jsonify(task_id)

        else:
            return BeamServer.query_algorithm(self, client, method, args, kwargs)

    def postprocess(self, task_id=None, task_inf=None, task=None):

        state = task.state
        args = task.args
        kwargs = task.kwargs
        retval = task.result

        logger.info(f"Task {task_id} finished with state {state}.")

        if task_inf is None:
            logger.warning(f"Task {task_id} not found in tasks dict")
            return

        # Send notification to the client via WebSocket
        if task_inf['ws_client_id'] is not None:
            client_id = task_inf['ws_client_id']
            ws = self.ws_clients.get(client_id)
            if ws and ws.open:
                asyncio.run(ws.send(json.dumps({"task_id": task_id, "state": state})))
            else:
                if ws:
                    asyncio.run(ws.close())
                    self.ws_clients.pop(client_id)

        self.postrun_callback(task_args=args, task_kwargs=kwargs, retval=retval, state=state, task=task, **task_inf)

    def postrun(self, task_args=None, task_kwargs=None, retval=None, state=None, task=None, metadata=None,
                postrun_args=None, postrun_kwargs=None, **kwargs):
        pass
