#!/usr/bin/env python
import os

import rospy
from std_msgs.msg import String
from roboga_nlu.msg import Nlu
from rasa_nlu.model import Interpreter

if __name__ == "__main__":
    directory = os.path.dirname(os.path.realpath(__file__))
    rospy.init_node('rasa_nlu', anonymous=True)
    interpreter = Interpreter.load(directory+"/rasa/models/nlu")
    pub = rospy.Publisher("roboga/nlu/result", Nlu, queue_size=10)
    def callback(data):
        msg = Nlu()
        result = interpreter.parse(data.data)
        msg.message = str(result['text'])
        msg.intent = str(result["intent"].get("name"))
        msg.entities = ["{{entity:{0} , value:{1}}}".format(x.get("entity"), x.get("value")) for x in result.get("entities")]
        pub.publish(msg)

    rospy.Subscriber("roboga/stt/result", String, callback=callback)
    rospy.spin()
    