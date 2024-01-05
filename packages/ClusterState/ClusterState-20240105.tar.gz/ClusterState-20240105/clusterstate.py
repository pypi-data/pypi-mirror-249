import os
import gzip
import time
import json
import uuid
import hmac
import sqlite3
import logging
import httprpc
import hashlib
import argparse
from logging import critical as log


def connect_db(db):
    os.makedirs('clusterstate', exist_ok=True)

    db = sqlite3.connect(os.path.join('clusterstate', db + '.sqlite3'))
    db.execute('''create table if not exists paxos(
                      key          text,
                      version      int,
                      promised_seq int,
                      accepted_seq int,
                      value        blob,
                      primary key(key, version)
                  )''')
    return db


async def fetch(ctx, db, key=None):
    db = connect_db(db)
    try:
        if key is None:
            return db.execute('''select key, version from paxos
                                 where accepted_seq > 0
                              ''').fetchall()
        else:
            row = db.execute('''select version, accepted_seq, value from paxos
                                where key=? and accepted_seq > 0
                                order by version desc limit 1
                             ''', [key]).fetchone()
            return row if row else [0, 0, None]
    finally:
        db.close()


async def paxos_server(ctx, db, key, version, proposal_seq, octets=None):
    version = int(version)
    proposal_seq = int(proposal_seq)

    if version < 1:
        raise Exception(f'INVALID_VERSION - {version}')

    db = connect_db(db)
    try:
        db.execute('insert or ignore into paxos values(?,?,0,0,null)',
                   [key, version])

        if octets is None:
            # Paxos PROMISE - Block stale writers and return the most recent
            # accepted value. Client will propose the most recent across
            # servers in the accept phase
            promised_seq, accepted_seq, value = db.execute(
                '''select promised_seq, accepted_seq, value
                   from paxos where key=? and version=?
                ''', [key, version]).fetchone()

            if proposal_seq <= promised_seq:
                raise Exception(f'PROMISE_SEQ {key}:{version} {proposal_seq}')

            db.execute('''update paxos set promised_seq=?
                          where key=? and version=?
                       ''', [proposal_seq, key, version])
            db.commit()

            return dict(accepted_seq=accepted_seq, value=value)
        else:
            # Paxos ACCEPT - Client has sent the most recent value from the
            # promise phase.
            promised_seq = db.execute(
                'select promised_seq from paxos where key=? and version=?',
                [key, version]).fetchone()[0]

            if proposal_seq < promised_seq:
                raise Exception(f'ACCEPT_SEQ {key}:{version} {proposal_seq}')

            db.execute('delete from paxos where key=? and version<?',
                       [key, version])

            db.execute('''update paxos
                          set promised_seq=?, accepted_seq=?, value=?
                          where key=? and version=?
                       ''', [proposal_seq, proposal_seq, octets, key, version])

            db.execute('''delete from paxos
                          where key=? and version < (
                              select max(version)
                              from paxos
                              where key=? and accepted_seq > 0)
                       ''', [key, key])
            db.commit()

            count = db.execute(
              'select count(*) from paxos where key=? and version=?',
              [key, version]).fetchone()[0]

            if 1 != count:
                raise Exception(f'CONSTRAINT_VIOLATED count({count})')

            return count
    finally:
        db.rollback()
        db.close()


# PROPOSE - Drives the paxos protocol
async def paxos_client(rpc, db, key, version, obj=b''):
    seq = int(time.strftime('%Y%m%d%H%M%S'))
    url = f'db/{db}/key/{key}/version/{version}/proposal_seq/{seq}'

    if obj != b'':
        # value to be set should always be json serializable
        value = gzip.compress(json.dumps(obj).encode())

    # Paxos PROMISE phase - block stale writers
    res = await rpc.quorum_invoke(f'promise/{url}')

    # CRUX of the paxos protocol - Find the most recent accepted value
    accepted_seq = 0
    for v in res.values():
        if v['accepted_seq'] > accepted_seq:
            accepted_seq, value = v['accepted_seq'], v['value']

    # Paxos ACCEPT phase - propose the value found above
    res = await rpc.quorum_invoke(f'accept/{url}', value)

    return dict(db=db, key=key, version=version,
                value=json.loads(gzip.decompress(value).decode()),
                status='CONFLICT' if accepted_seq > 0 else 'OK')


async def get(ctx, db, key=None):
    rpc = ctx.get('rpc', RPCClient(G.cert, G.cert, G.servers))

    if key is None:
        res = await rpc.quorum_invoke(f'fetch/db/{db}')

        keys = dict()
        for values in res.values():
            for key, version in values:
                if version > keys.get(key, 0):
                    keys[key] = version

        return dict(db=db, keys=keys)
    else:
        for i in range(rpc.quorum):
            res = await rpc.quorum_invoke(f'fetch/db/{db}/key/{key}')

            vlist = [v for v in res.values()]
            if all([vlist[0] == v for v in vlist]):
                result = dict(db=db, key=key, version=vlist[0][0])

                if vlist[0][0] > 0:
                    value = gzip.decompress(vlist[0][2])
                    result['value'] = json.loads(value.decode())

                return result

            await paxos_client(rpc, db, key, max([v[0] for v in vlist]))


def get_hmac(secret, salt):
    return hmac.new(secret.encode(), salt.encode(), hashlib.sha256).hexdigest()


async def put(ctx, db, secret, key, version, obj):
    ctx['rpc'] = RPCClient(G.cert, G.cert, G.servers)

    res = await get(ctx, db, '#')
    if res['value']['hmac'] == get_hmac(secret, res['value']['salt']):
        return await paxos_client(ctx['rpc'], db, key, version, obj)

    raise Exception('Authentication Failed')


# Initialize the db and generate api key
async def init(ctx, db, secret=''):
    ctx['rpc'] = RPCClient(G.cert, G.cert, G.servers)

    res = await get(ctx, db, '#')
    if 0 == res['version']:
        salt = str(uuid.uuid4())
        res['value'] = dict(salt=salt, hmac=get_hmac('', salt))

    if res['value']['hmac'] == get_hmac(secret, res['value']['salt']):
        salt = str(uuid.uuid4())
        secret = str(uuid.uuid4())

        res = await paxos_client(ctx['rpc'], db, '#', res['version'] + 1,
                                 dict(salt=salt, hmac=get_hmac(secret, salt)))
        if 'OK' == res['status']:
            res['secret'] = secret

        return res

    raise Exception('Authentication Failed')


class RPCClient(httprpc.Client):
    def __init__(self, cacert, cert, servers):
        super().__init__(cacert, cert, servers)

    async def quorum_invoke(self, resource, octets=b''):
        res = await self.cluster(resource, octets)
        result = dict()

        exceptions = list()
        for s, r in zip(self.conns.keys(), res):
            if isinstance(r, Exception):
                log(f'{s} {type(r)} {r}')
                exceptions.append(f'\n-{s}\n{r}')
            else:
                result[s] = r

        if len(result) < self.quorum:
            raise Exception('\n'.join(exceptions))

        return result


if '__main__' == __name__:
    logging.basicConfig(format='%(asctime)s %(process)d : %(message)s')

    G = argparse.ArgumentParser()
    G.add_argument('--cert', help='certificate path')
    G.add_argument('--port', help='port number for server')
    G.add_argument('--servers', help='comma separated list of server ip:port')
    G = G.parse_args()

    httprpc.run(G.port, dict(init=init, get=get, put=put, fetch=fetch,
                             promise=paxos_server, accept=paxos_server),
                cacert=G.cert, cert=G.cert)
