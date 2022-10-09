#!/usr/bin/env python3
import os

import rospy
from std_msgs.msg import String
from roboga_nlu.srv import Nlu, NluResponse
from rasa_nlu.model import Interpreter

if __name__ == "__main__":
    directory = os.path.dirname(os.path.realpath(__file__))
    rospy.init_node('rasa_nlu', anonymous=True)
    interpreter = Interpreter.load(directory+"/rasa/models/nlu")
    
    def handler(req):
        result = interpreter.parse(req.data)
        message = str(result['text'])
        intent = str(result["intent"].get("name"))
        entities = ["{{\"entity\":\"{0}\", \"value\":\"{1}\"}}".format(x.get("entity"), x.get("value")) for x in result.get("entities")]
        return NluResponse(
            message=message,
            intent=intent,
            entities=entities
        )

    pub = rospy.Service("zordon/nlu", Nlu, handler)
    rospy.spin()
    