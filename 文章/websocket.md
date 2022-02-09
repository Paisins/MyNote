- websocket
- socketio

# 1、websocket的实现方式
参考: [WebSocket vs Socket.io](https://www.educba.com/websocket-vs-socket-io/)

当我开始看python中websocket的实现方式时，感到比较困惑的一个问题是Websockets和SocketIo有什么区别？由于工作的需要我不能选择Websockets这种纯粹发送消息的工具，必须要做到message、action等不同关键词定义的事件驱动，所以我选择了SocketIo，当然我实际上也不知道Websockets能不能做到事件驱动，我甚至以为这两个底层应该是一样的实现方式，但当我试着了解时却发现并不是。

- socketio

- import websocket

- import websockets

- from fastapi import websockets

- from starlette.websockets import WebSocket

而且似乎有很多websocket的实现方式，各个框架内部也有集成的，我比较想搞清楚这些实现方式有什么区别。但是首先从概念开始，在websocket开始之前，我以前看过tcp三次握手建立连接的方式，也已经看过一点socket模型的实现方式，现在从一个基本问题出发，websocket跟之前socket有什么区别，它是如何实现双向通信的？


## 1. websocket

描述一：websocket允许服务端主动向客户端推送消息，建立在tcp协议之上，与http协议有很好的兼容性，协议标识符号是ws，如果加密则为wss




# 2、socket io 客户端实践
在学习socket之后，实际项目中遇到了使用websocket的需求，但网上关于python中如何使用websocket的文章很少，所以自己尝试了不少，我的需求场景是使用python搭建一个websocket客户端连接到对方的服务端，据我了解，服务端是非python的语言搭建的

**参考**
[官网The Socket.IO Client](https://python-socketio.readthedocs.io/en/latest/client.html#creating-a-client-instance)

## 1、安装与简单使用
python socketio有两种类型，同步和异步的，因为项目需求所以我使用异步的
```
# 同步
pip install "python-socketio[client]"
# 异步
pip install "python-socketio[asyncio_client]"
```
官网的介绍确实比较简单
```python
import socketio

# asyncio
sio = socketio.AsyncClient()

@sio.event
async def message(data):
    print('I received a message!')

@sio.on('my message')
async def on_message(data):
    print('I received a message!')
    
# 连接到服务端
await sio.connect('http://localhost:5000')
print('my sid is', sio.sid)

# 发送消息
await sio.emit('my message', {'foo': 'bar'})
```
## 2、代码
项目中的部分代码，仅供参考，部分需要重写
```python
import asyncio
import socketio
import traceback
import logger


class MyWebSocket(BasicProxy):
    """websocket"""

    def __init__(self, socketio_url, namespace='/imchat'):
        self.namespace = namespace
        sio = socketio.AsyncClient(reconnection_delay=0)

        # 注册事件函数
        sio.on('message', self.message, namespace=self.namespace)
        sio.on('action', self.action, namespace=self.namespace)
        sio.on('chat', self.chat, namespace=self.namespace)
        sio.on('disconnect', self.disconnect, namespace=self.namespace)
        sio.on('connect_error', self.connect_error, namespace=self.namespace)
        self.sio = sio
        self.socketio_url = socketio_url

    # 事件函数
    async def message(self, data):
        logger.info(f'I received a message! {data}')

    async def action(self, data):
        logger.info(f'I received a action! {data}')

    async def chat(self, data):
        logger.info(f'I received a chat! {data}')

    @staticmethod
    async def connect_error():
        logger.error("The connection failed!")

    @staticmethod
    async def disconnect():
        logger.info(f"I'm disconnected!")

    async def emit_message(self, message_data: dict):
        await self.sio.emit('message', message_data, namespace=self.namespace)
        logger.info(f'message 已发送, {message_data}')

    async def emit_action(self, data: dict):
        await self.sio.emit('action', data, namespace=self.namespace)

    async def emit_chat(self, data: dict):
        await self.sio.emit('chat', data, namespace=self.namespace)

    async def handle_emit(self, event: str, data: dict):
        """
        调用发送请求
        """
        try:
            if event == 'message':
                await self.emit_message(data)
            elif event == 'action':
                await self.emit_action(data)
            elif event == 'chat':
                await self.emit_chat(data)
        except Exception:
            logger.error(f'发送失败: retry_times={retry_times}, data: {data}, error: {traceback.format_exc()}')

    async def run_socket(self):
        await self.sio.connect(self.socketio_url, transports='websocket', namespaces=['/', self.namespace])

        while True:
            # redis 队列获取任务
            res = await self.task_manager.handle_task_from_queue()
            if not res:
                logger.info('当前消息队列无任务')
                continue

            await self.handle_emit(res, retry_times)

```
## 3、具体使用中的问题
### 1、连接报错
```
Traceback (most recent call last):
  File "test.py", line 37, in <module>
    loop.run_until_complete(task)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/base_events.py", line 584, in run_until_complete
    return future.result()
  File "test.py", line 25, in work
    await sio.connect('test_url')
  File "/Users/jichengjian/venv/work_wechat_robot/lib/python3.7/site-packages/socketio/asyncio_client.py", line 144, in connect
    raise exceptions.ConnectionError(exc.args[0]) from None
socketio.exceptions.ConnectionError: Unexpected response from server
Unexpected response from server
The connection failed!
Unclosed client session
client_session: <aiohttp.client.ClientSession object at 0x7fd89e0fb978>
Unclosed connector
connections: ['[(<aiohttp.client_proto.ResponseHandler object at 0x7fd89e0e86c8>, 0.41660982)]']
connector: <aiohttp.connector.TCPConnector object at 0x7fd89e0fb9b0>
```
如果报错的时候可以使用logger查看详细信息
```python
sio = socketio.AsyncClient(logger=True, engineio_logger=True)
```
添加之后可以看到是因为polling模式，所以配置websocket
```python
await self.sio.connect(url, transports='websocket')
```
这样就可以连接了，假如报错ssl验证问题，可以加上
```python
sio = socketio.AsyncClient(ssl_verify=False)
```

### 2、发送后服务端无反应
我遇到这个情况后跟服务端的一方进行了沟通，排查后发现是因为没有指定namespace
``` python
await sio.connect(url, transports='websocket', namespaces=['/', your_namespace])
```

### 3、连接断开问题
一般服务端不会频繁断开连接的，但我所连接的服务端每隔一分钟左右就会断开连接，所以需要考虑这个问题
```python
sio = socketio.AsyncClient(reconnection_delay=0)
```
重连期间可能会接收到任务，所以会发送失败，因此异常捕捉和错误重试都是必要的，

# 3、socketio服务端实践
- 服务端的建立
- 客户端连接分组
- 广播
- 连接时间，资源占用评估
- 心跳检查机制
# 实现聊天室