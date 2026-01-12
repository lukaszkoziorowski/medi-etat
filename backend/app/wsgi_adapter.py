"""
WSGI adapter for FastAPI (ASGI) application.
This allows FastAPI to run in WSGI environments like PythonAnywhere.
"""
import asyncio
import io
from typing import Dict, List, Tuple, Callable, Any
from urllib.parse import parse_qs


class ASGI2WSGI:
    """Convert ASGI application to WSGI application."""
    
    def __init__(self, asgi_app: Callable):
        self.asgi_app = asgi_app
        self.loop = None
    
    def _get_or_create_loop(self):
        """Get or create event loop."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop
    
    def _wsgi_to_asgi_scope(self, environ: Dict[str, Any]) -> Dict[str, Any]:
        """Convert WSGI environ to ASGI scope."""
        method = environ['REQUEST_METHOD']
        path = environ.get('PATH_INFO', '/')
        query_string = environ.get('QUERY_STRING', '').encode('latin-1')
        
        # Parse headers
        headers = []
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                header_name = key[5:].replace('_', '-').title()
                headers.append([header_name.encode('latin-1'), value.encode('latin-1')])
        
        # Add Origin header explicitly if present (important for CORS)
        if 'HTTP_ORIGIN' in environ:
            headers.append([b'origin', environ['HTTP_ORIGIN'].encode('latin-1')])
        
        # Add content-type and content-length if present
        if 'CONTENT_TYPE' in environ:
            headers.append([b'content-type', environ['CONTENT_TYPE'].encode('latin-1')])
        if 'CONTENT_LENGTH' in environ:
            headers.append([b'content-length', environ['CONTENT_LENGTH'].encode('latin-1')])
        
        scope = {
            'type': 'http',
            'asgi': {'version': '3.0', 'spec_version': '2.1'},
            'http_version': '1.1',
            'method': method,
            'scheme': environ.get('wsgi.url_scheme', 'http'),
            'path': path,
            'raw_path': path.encode('utf-8'),
            'query_string': query_string,
            'root_path': environ.get('SCRIPT_NAME', ''),
            'headers': headers,
            'client': (environ.get('REMOTE_ADDR', ''), int(environ.get('REMOTE_PORT', 0))),
            'server': (environ.get('SERVER_NAME', ''), int(environ.get('SERVER_PORT', 80))),
        }
        return scope
    
    def _read_body(self, environ: Dict[str, Any]) -> bytes:
        """Read request body from WSGI environ."""
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError,):
            request_body_size = 0
        
        if request_body_size > 0:
            return environ['wsgi.input'].read(request_body_size)
        return b''
    
    def __call__(self, environ: Dict[str, Any], start_response: Callable) -> List[bytes]:
        """WSGI application interface."""
        loop = self._get_or_create_loop()
        
        # Convert WSGI to ASGI
        scope = self._wsgi_to_asgi_scope(environ)
        body = self._read_body(environ)
        
        # Create message queue
        receive_queue = asyncio.Queue()
        send_queue = asyncio.Queue()
        
        # Send initial request
        receive_queue.put_nowait({
            'type': 'http.request',
            'body': body,
            'more_body': False,
        })
        
        # Run ASGI app
        async def run_app():
            await self.asgi_app(scope, receive_queue.get, send_queue.put)
        
        # Execute in event loop
        try:
            loop.run_until_complete(run_app())
        except Exception as e:
            # Handle errors
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'text/plain')]
            start_response(status, headers)
            return [f'Error: {str(e)}'.encode('utf-8')]
        
        # Get response from queue
        response_data = []
        status_code = 200
        response_headers = []
        
        try:
            while True:
                message = send_queue.get_nowait()
                if message['type'] == 'http.response.start':
                    status_code = message['status']
                    response_headers = [(h[0].decode('latin-1'), h[1].decode('latin-1')) 
                                       for h in message['headers']]
                elif message['type'] == 'http.response.body':
                    response_data.append(message.get('body', b''))
                    if not message.get('more_body', False):
                        break
        except asyncio.QueueEmpty:
            pass
        
        # Format status properly (include status text)
        if status_code == 200:
            status = '200 OK'
        elif status_code == 204:
            status = '204 No Content'
        elif status_code == 404:
            status = '404 Not Found'
        elif status_code >= 500:
            status = f'{status_code} Internal Server Error'
        else:
            status = f'{status_code} Error'
        
        # Start WSGI response
        start_response(status, response_headers)
        
        return response_data
