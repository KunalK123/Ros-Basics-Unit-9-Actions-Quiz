#! /usr/bin/env python
import rospy
import time
import actionlib

from actions_quiz.msg import CustomActionMsgFeedback, CustomActionMsgResult, CustomActionMsgAction
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

class CustomActionMsgClass(object):

  _feedback = CustomActionMsgFeedback()
  _result   = CustomActionMsgResult()

  def __init__(self):
    self._as = actionlib.SimpleActionServer("action_custom_msg_as", CustomActionMsgAction, self.goal_callback, False)
    self._as.start()
    
  def goal_callback(self, goal):

    success = True
    r = rospy.Rate(1)

    self._pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
    self._takeoff_msg = Empty()
    self._pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
    self._land_msg = Empty()

    takeoff_or_land = goal.goal

    i = 0
    for i in xrange(0, 4):

      if self._as.is_preempt_requested():
        rospy.loginfo('The goal has been cancelled/preempted')
        self._as.set_preempted()
        success = False
        break

      if takeoff_or_land == 'TAKEOFF':

        self._pub_takeoff.publish(self._takeoff_msg)
        self._feedback.feedback = 'Taking Off...'
        self._as.publish_feedback(self._feedback)

      if takeoff_or_land == 'LAND':

        self._pub_land.publish(self._land_msg)
        self._feedback.feedback = 'Landing...'
        self._as.publish_feedback(self._feedback)

      r.sleep()
      
    if success:
      self._result = Empty()
      self._as.set_succeeded(self._result)


if __name__ == '__main__':
  rospy.init_node('action_custom_msg')
  CustomActionMsgClass()
  rospy.spin()
