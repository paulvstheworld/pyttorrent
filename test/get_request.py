from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import Agent, readBody


def test():
    def handle_request(result):
        print result
    
    def handle_request_err(err):
        print err
        reactor.stop()
    
    agent = Agent(reactor)
    d = agent.request('GET', 'http://xyz.google.com')
    d.addCallbacks(handle_request, handle_request_err)

if __name__ == '__main__':
    test()
    reactor.run()
