
from random import randint
import time
from spade import run, wait_until_finished
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template

XMPP_server = "localhost"
Agent_prefix = "agent"



class MyAgent(Agent):
    def __init__(self, neighbours=[], ifleader=False, value: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.neighbours = neighbours
        self.parent_jid = None
        self.leader = ifleader
        if self.leader:
            self.parent_jid = self.name
        self.childs = []
        self.value = value
        self.counter = 0
        self.childs_values = []
        self.has_on_send_value_behaviour = False
        self.messages = 0

    def stop(self):
        if self.leader:
            print(self.name + f" sent {self.messages} messages and used {len(self.neighbours)  + len(self.childs) + len(self.childs_values)} memory cells" );
        return super().stop()

    class on_make_child_reply(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                if self.agent.parent_jid is None:
                    self.agent.parent_jid = str(msg.sender).split('@')[0]
                    msg = msg.make_reply()
                    msg.set_metadata("action", "answer")
                    msg.body = "True"
                    if self.agent.leader == False:
                        self.agent.add_behaviour(self.agent.send_make_child())

                else:
                    msg.make_reply()
                    msg.set_metadata("action", "answer")
                    msg.body = ""
                await self.send(msg)
                self.agent.messages += 1

    class send_make_child(OneShotBehaviour):
        async def run(self):
            for i in self.agent.neighbours:
                if i != self.agent.parent_jid:
                    msg = Message(to=i+"@"+XMPP_server)
                    msg.set_metadata("action", "make_child")
                    await self.send(msg)
                    self.agent.messages += 1
                    self.agent.counter += 1

    class send_value(OneShotBehaviour):
        async def run(self):
            s = self.agent.value
            n = 1
            for i in self.agent.childs_values:
                s += int(i[0])
                n += int(i[1])
            if self.agent.leader:
                print(f"Average sum is {s/n}")
                await self.agent.stop()

            else:
                print(self.agent.parent_jid, XMPP_server)
                msg = Message(to=self.agent.parent_jid + "@" + XMPP_server)
                msg.set_metadata("action", "send_value")
                msg.body = f"{s},{n}"
                await self.send(msg)
                self.agent.messages += 1
            self.kill()

    class on_send_value(CyclicBehaviour):
        async def run(self):
            msg = None
            if self.agent.childs:
                msg = await self.receive(timeout=40)
            if msg:
                s = msg.body.split(',')[0]
                n = msg.body.split(',')[1]
                self.agent.childs_values.append((s, n))
            if len(self.agent.childs) == len(self.agent.childs_values):
                self.agent.add_behaviour(self.agent.send_value())
                self.kill()

    class on_make_child_answer(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                answer = msg.body
                if answer:
                    self.agent.childs.append(str(msg.sender).split("@")[0])
                    b = self.agent.on_send_value()
                    if not self.agent.has_on_send_value_behaviour:
                        t = Template()
                        t.set_metadata("action", "send_value")
                        self.agent.add_behaviour(b, t)
                        self.agent.has_on_send_value_behaviour = True
                self.agent.counter -= 1
            if self.agent.counter == 0:
                if not self.agent.childs:
                    self.agent.add_behaviour(self.agent.send_value())
                self.kill()

    async def setup(self):
        b = self.on_make_child_reply()
        t = Template()
        t.set_metadata("action", "make_child")
        self.add_behaviour(b, t)
        if self.leader:
            self.add_behaviour(self.send_make_child())

        t = Template()
        t.set_metadata("action", "answer")
        self.add_behaviour(self.on_make_child_answer(), t)


graph = [
    [f"{Agent_prefix}{i}" for i in [1, 7, 15]],
    [f"{Agent_prefix}{i}" for i in [0, 2, 8]],
    [f"{Agent_prefix}{i}" for i in [1, 3]],
    [f"{Agent_prefix}{i}" for i in [2, 4]],
    [f"{Agent_prefix}{i}" for i in [3, 5, 13]],
    [f"{Agent_prefix}{i}" for i in [4, 6, 10]],
    [f"{Agent_prefix}{i}" for i in [5, 7, 14]],
    [f"{Agent_prefix}{i}" for i in [0, 6, 8]],
    [f"{Agent_prefix}{i}" for i in [1, 7, 9, 12]],
    [f"{Agent_prefix}{i}" for i in [8, 10]],
    [f"{Agent_prefix}{i}" for i in [5, 9, 11]],
    [f"{Agent_prefix}{i}" for i in [10, 12, 15]],
    [f"{Agent_prefix}{i}" for i in [8, 11, 13]],
    [f"{Agent_prefix}{i}" for i in [4, 12, 14]],
    [f"{Agent_prefix}{i}" for i in [6, 13, 15]],
    [f"{Agent_prefix}{i}" for i in [0, 14, 11]]
]

async def main():
    s = 0
    agents = []
    leader_num = randint(0, len(graph)-1)
    print(f'Leader num - {leader_num}')
    for i in range(len(graph)):
        val = randint(0, 100)
        s += val
        if i != leader_num:
            print(i)
            agent = MyAgent(graph[i], False, val, f"{Agent_prefix}{i}@{XMPP_server}", "mypass", verify_security=False)
            await agent.start(auto_register=False)
            agents.append(agent)
        else:
            leader_val = val
    print(f"True average value is {(s)/len(graph)}")
    time.sleep(5)
    leader = MyAgent(graph[leader_num], True, leader_val, f"{Agent_prefix}{leader_num}@{XMPP_server}", "mypass", verify_security=False)
    await leader.start(auto_register=False)

    await wait_until_finished(leader)

    for i in agents:
        await i.stop()
    print("Agents finished")

if __name__ == "__main__":
    run(main())
    print('Done')