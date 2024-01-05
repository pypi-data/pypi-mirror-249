#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stdout
from io import StringIO, FileIO, BytesIO
from pathlib import PurePosixPath
from socket import socket
from urllib.request import urlopen
from tarfile import open
from paramiko import Transport, SSHException, SFTPClient
from asyncssh import create_connection, SSHClient, SSHClientSession
from git.cmd import Git
from logging import getLogger
from os.path import basename
from aiostream.stream import chain
from queue import Queue
from threading import Thread
from asyncio import sleep
from ipaddress import ip_address
from dns.resolver import Resolver
from random import choice

logger = getLogger()

def resolve(host):
    try:
        return str(ip_address(host))
    except ValueError:
        return choice(Resolver().resolve(host)).to_text()

class Src():
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        kwargs = self.kwargs
        if kwargs.get('firmware'):
            location = kwargs.get('firmware')
            io = BytesIO(urlopen(location).read())
        elif kwargs.get('version'):
            version = kwargs.get('version')
            location = f'''http://192.168.21.1:5080/APP/develop/develop/update/industry/crab/dists/crab-{version}.tar.xz'''
            io = BytesIO(urlopen(location).read())
        elif kwargs.get('branch'):
            version = BytesIO(urlopen(f'''http://192.168.21.1:5080/APP/develop/develop/update/industry/crab/heads/{kwargs.get('branch')}.txt''').read()).read().decode()
            location = f'''http://192.168.21.1:5080/APP/develop/develop/update/industry/crab/dists/crab-{version}.tar.xz'''
            io = BytesIO(urlopen(location).read())
        else:
            location = f'''var/crab-{Git().describe(tags=True, abbrev=True, always=True, long=True, dirty=True)}.tar.xz'''
            io = BytesIO(FileIO(location).read())
        self.location = location
        self.io = io

    def __iter__(self):
        yield (PurePosixPath('/tmp/firmware.bin'), self.io)

    def dump(self):
        stdout.buffer.write(self.io.read())

    def download(self):
        FileIO(basename(self.location), 'wb').write(self.io.read())
        logger.info(self.kwargs)
        logger.info(basename(self.location))

class Archive():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __iter__(self):
        kwargs = self.kwargs
        tar = open(mode='r:xz', fileobj=Src(**kwargs).io)
        for tarinfo in tar.getmembers():
            file = tar.extractfile(tarinfo)
            if file:
                yield (PurePosixPath(f'''/usr/local/crab/{tarinfo.name}'''), file)
        tar.close()
class ClientAsyncssh():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def create(self):
        kwargs = self.kwargs
        connnection, client = await create_connection(SSHClient, resolve(kwargs.get('host', '192.168.1.200')), port=kwargs.get('port', 22), username=kwargs.get('username', 'root'), password=kwargs.get('password', 'elite2014'), known_hosts=None)
        self.connnection = connnection

    async def putfo(self, files):
        connnection = self.connnection
        kwargs = self.kwargs
        async with connnection.start_sftp_client() as sftp:
            for (path, content) in files:
                    yield f'{path}\n'.encode()
                    try:
                        await sftp.chdir(str(path.parent))
                    except IOError:
                        await sftp.mkdir(str(path.parent))
                    async with sftp.open(str(path), 'wb+') as file:
                        await file.write(content.getbuffer())

    async def exec_command(self, commands):
        connnection = self.connnection
        for command in commands:
            yield command
            queue = Queue()
            JOB_DONE = object()
            class MySSHClientSession(SSHClientSession):
                def connection_lost(self, exc):
                    queue.put(f'{exc}\n'.encode())
                    queue.put(JOB_DONE)
                def data_received(self, data, datatype):
                    if isinstance(data, (bytes)):
                        queue.put(data)
                    elif isinstance(data, (str)):
                        queue.put(f'{data}\n'.encode())
                def eof_received(self):
                    queue.put(JOB_DONE)
                def exit_status_received(self, status):
                    queue.put(f'exit_status_received {status}\n'.encode())
                def __aiter__(self):
                    return self
                async def __anext__(self):
                    chunk = queue.get()
                    if chunk is JOB_DONE:
                        raise StopAsyncIteration
                    return chunk
            channel, session = await connnection.create_session(MySSHClientSession, command)
            await channel.wait_closed()
            async for item in session:
                yield item

            # try:
            #     await connnection.run(command, check=True)
            # except:
            #     pass

    async def exit(self):
        yield b'end\n'

class ClientParamiko():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def create(self):
        kwargs = self.kwargs
        sock = socket()
        sock.connect((resolve(kwargs.get('host', '192.168.1.200')), kwargs.get('port', 22)))
        transport = Transport(sock)
        transport.start_client()
        try:
            if not kwargs.get('password'):
                raise SSHException
            transport.auth_password(kwargs.get('username', 'root'), kwargs.get('password', 'elite2014'))
        except SSHException:
            transport.auth_none(kwargs.get('username', 'root'))
        self.transport = transport

    async def putfo(self, files):
        client = SFTPClient.from_transport(self.transport)
        for (path, content) in files:
            try:
                client.chdir(str(path.parent))
            except IOError:
                client.mkdir(str(path.parent))
            queue = Queue(maxsize=1)
            JOB_DONE = object()
            def callback(transferred, total):
                queue.put('{0:.3f}\n'.format(transferred / total, 2).encode())
            def task():
                client.putfo(content, str(path), content.getbuffer().nbytes, callback)
                queue.put(JOB_DONE)
            thread = Thread(target=task)
            thread.start()
            while True:
                chunk = queue.get()
                if chunk is JOB_DONE:
                    break
                yield chunk
            thread.join()

    async def exec_command(self, commands):
        for command in commands:
            try:
                yield command
                await sleep(1)
                channel = self.transport.open_session()
                channel.set_combine_stderr(True)
                channel.exec_command(command.decode())
                line = b''
                while True:
                    self.transport.send_ignore()
                    if channel.recv_ready():
                        char = channel.recv(1)
                        line += char
                        if char == b'\n':
                            yield line
                            line = b''
                    if channel.exit_status_ready():
                        break
                channel.close()
            except EOFError:
                pass

    async def exit(self):
        yield b'end\n'


class Client():
    def __init__(self, *args, **kwargs):
        self.client = ClientAsyncssh(*args, **kwargs)
        # self.client = ClientParamiko(*args, **kwargs)

class Distcrab():
    def __init__(self, host='192.168.1.200', port=22, username='root', password=None, download=False, dump=False, firmware=None, version=None, branch=None, *args, **kwargs):
        self.client = Client(host=host, port=port, username=username, password=password).client
        self.download = download
        self.dump = dump
        self.firmware = firmware
        self.version = version
        self.branch = branch

    async def __aiter__(self):
        client = self.client
        download = self.download
        dump = self.dump
        firmware = self.firmware
        version = self.version
        branch = self.branch
        src = Src(firmware=firmware, version=version, branch=branch)
        if download:
            src.download()
        elif dump:
            src.dump()
        elif firmware:
            await client.create()
            async with chain(client.putfo(src), client.exec_command([
                b'/bin/mount -o rw,remount /\n',
                b'/bin/sync\n',
                b'/rbctrl/prepare-update.sh /tmp\n',
                b'/etc/init.d/rbctrl.sh stop\n',
                b'PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin /var/volatile/update/chrt-sqfs.sh /update/updater /mnt/tmp/update-final.sh\n'
            ]), client.exit()).stream() as stream:
                async for item in stream:
                    yield item
        else:
            await client.create()
            async with chain(client.exec_command([
                b'/usr/local/bin/elite_local_stop.sh\n',
            ]), client.putfo(src), client.exec_command([
                b'/bin/rm -rf /usr/local/crab/\n',
                b'/bin/mkdir -p /usr/local/crab/\n',
                b'/bin/sync\n',
                b'/bin/tar -xJf /tmp/firmware.bin -C /usr/local/crab/\n',
                b'/bin/rm -rf /tmp/firmware.bin\n',
                b'/bin/sync\n',
                b'/usr/local/bin/elite_local_start.sh\n',
            ]), client.exit()).stream() as stream:
                async for item in stream:
                    yield item
