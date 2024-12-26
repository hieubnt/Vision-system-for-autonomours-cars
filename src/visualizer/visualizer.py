from abc import ABC, abstractmethod
from pydantic import BaseModel
import numpy as np
import sys
sys.path.append('../utilities')

from pub_sub import Publisher

class Visualizer(Subscriber):
    subscribed_topics = ['pipeline_output']
    subscriber_name = 'visualizer'

    def update(self, topic_name, data):
        pass

    def check_update(self):
        pass
