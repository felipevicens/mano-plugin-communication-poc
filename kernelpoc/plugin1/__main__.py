import logging
import json
import time
from ..sonbase.manoplugin import ManoPlugin


class DemoPlugin1(ManoPlugin):

    def __init__(self):
        # call super class to do all the messaging and registration overhead
        super(self.__class__, self).__init__(blocking=False)

    def declare_subscriptions(self):
        """
        Declare topics to which we want to listen and define callback methods.
        """
        self.subscribe("platform.management.plugins.list", self.on_list_result)

    def on_list_result(self, ch, method, properties, body):
        sender = properties.app_id
        message = json.loads(body)
        if message.get("type") == "REP":
            # we have a reply, lets print it
            print "-" * 20 + " Plugins " + "-" * 20
            for k, v in message.get("plugins").iteritems():
                print "%s, %s, %s" % (k, v.get("version"), v.get("state"))
            print "-" * 49

    def run(self):
        """
        Overwrites. Put your Plugin code here.
        """
        # lets have some fun and query the plugin manager for a list of plugins
        self.publish("platform.management.plugins.list", json.dumps({"type": "REQ"}))
        # trigger deployment workflow of example B
        self.publish("service.management.placement.compute", json.dumps(
            {"service": "Service A", "service_chain_graph": "I am a complex service chain."}))
        # give us some time to react
        time.sleep(5)
        # lets stop this plugin
        self.deregister()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    p = DemoPlugin1()
