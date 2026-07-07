 ✔ Image ioc_threat_agent-ui        Built                                                                                                                  2.1s 
 ✔ Image ioc_threat_agent-api       Built                                                                                                                  2.1s 
 ✔ Network ioc_threat_agent_default Created                                                                                                                0.0s 
 ✔ Container ioc-threat-api         Created                                                                                                                0.1s 
 ✔ Container ioc-threat-ui          Created                                                                                                                0.1s 
Attaching to ioc-threat-api, ioc-threat-ui
ioc-threat-ui  | 
ioc-threat-ui  | Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.
ioc-threat-ui  | 
ioc-threat-ui  | 
ioc-threat-ui  |   You can now view your Streamlit app in your browser.
ioc-threat-ui  | 
ioc-threat-ui  |   URL: http://0.0.0.0:8501
ioc-threat-ui  | 
ioc-threat-api  | INFO:     Started server process [1]
ioc-threat-api  | INFO:     Waiting for application startup.
ioc-threat-api  | INFO:     Application startup complete.
ioc-threat-api  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
ioc-threat-ui   | 2026-07-07 12:53:53.060 Uncaught app execution
ioc-threat-ui   | Traceback (most recent call last):
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/connection.py", line 204, in _new_conn
ioc-threat-ui   |     sock = connection.create_connection(
ioc-threat-ui   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/util/connection.py", line 85, in create_connection
ioc-threat-ui   |     raise err
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/util/connection.py", line 73, in create_connection
ioc-threat-ui   |     sock.connect(sa)
ioc-threat-ui   | ConnectionRefusedError: [Errno 111] Connection refused
ioc-threat-ui   | 
ioc-threat-ui   | The above exception was the direct cause of the following exception:
ioc-threat-ui   | 
ioc-threat-ui   | Traceback (most recent call last):
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/connectionpool.py", line 788, in urlopen
ioc-threat-ui   |     response = self._make_request(
ioc-threat-ui   |                ^^^^^^^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/connectionpool.py", line 493, in _make_request
ioc-threat-ui   |     conn.request(
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/connection.py", line 500, in request
ioc-threat-ui   |     self.endheaders()
ioc-threat-ui   |   File "/usr/local/lib/python3.11/http/client.py", line 1318, in endheaders
ioc-threat-ui   |     self._send_output(message_body, encode_chunked=encode_chunked)
ioc-threat-ui   |   File "/usr/local/lib/python3.11/http/client.py", line 1078, in _send_output
ioc-threat-ui   |     self.send(msg)
ioc-threat-ui   |   File "/usr/local/lib/python3.11/http/client.py", line 1016, in send
ioc-threat-ui   |     self.connect()
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/connection.py", line 331, in connect
ioc-threat-ui   |     self.sock = self._new_conn()
ioc-threat-ui   |                 ^^^^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/connection.py", line 219, in _new_conn
ioc-threat-ui   |     raise NewConnectionError(
ioc-threat-ui   | urllib3.exceptions.NewConnectionError: HTTPConnection(host='127.0.0.1', port=8000): Failed to establish a new connection: [Errno 111] Connection refused
ioc-threat-ui   | 
ioc-threat-ui   | The above exception was the direct cause of the following exception:
ioc-threat-ui   | 
ioc-threat-ui   | Traceback (most recent call last):
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/requests/adapters.py", line 667, in send
ioc-threat-ui   |     resp = conn.urlopen(
ioc-threat-ui   |            ^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/connectionpool.py", line 842, in urlopen
ioc-threat-ui   |     retries = retries.increment(
ioc-threat-ui   |               ^^^^^^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/urllib3/util/retry.py", line 543, in increment
ioc-threat-ui   |     raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
ioc-threat-ui   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ioc-threat-ui   | urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='127.0.0.1', port=8000): Max retries exceeded with url: /analyze (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=8000): Failed to establish a new connection: [Errno 111] Connection refused"))
ioc-threat-ui   | 
ioc-threat-ui   | During handling of the above exception, another exception occurred:
ioc-threat-ui   | 
ioc-threat-ui   | Traceback (most recent call last):
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 88, in exec_func_with_error_handling
ioc-threat-ui   |     result = func()
ioc-threat-ui   |              ^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 579, in code_to_exec
ioc-threat-ui   |     exec(code, module.__dict__)
ioc-threat-ui   |   File "/app/ui/streamlit_app.py", line 33, in <module>
ioc-threat-ui   |     resp = requests.post(f"{API_BASE}/analyze", json={"ioc": ioc}, timeout=60)
ioc-threat-ui   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/requests/api.py", line 115, in post
ioc-threat-ui   |     return request("post", url, data=data, json=json, **kwargs)
ioc-threat-ui   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/requests/api.py", line 59, in request
ioc-threat-ui   |     return session.request(method=method, url=url, **kwargs)
ioc-threat-ui   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/requests/sessions.py", line 589, in request
ioc-threat-ui   |     resp = self.send(prep, **send_kwargs)
ioc-threat-ui   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/requests/sessions.py", line 703, in send
ioc-threat-ui   |     r = adapter.send(request, **kwargs)
ioc-threat-ui   |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ioc-threat-ui   |   File "/usr/local/lib/python3.11/site-packages/requests/adapters.py", line 700, in send
ioc-threat-ui   |     raise ConnectionError(e, request=request)
ioc-threat-ui   | requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=8000): Max retries exceeded with url: /analyze (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=8000): Failed to establish a new connection: [Errno 111] Connection refused"))


v View in Docker Desktop   o View Config   w Enable Watch   d Detach
