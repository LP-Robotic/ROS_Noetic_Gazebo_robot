#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

def initNode():
    rospy.init_node('adapterJoint', anonymous=True)
	
def send(publisher, position):
    """
    Publishes the given position to the joint controller.
    """
    try:
        rospy.loginfo(f"Publishing position: {position}") # Лучше использовать f-строки
        publisher.publish(Float64(position)) # Явное создание объекта Float64
    except rospy.ROSException as e:
        rospy.logerr(f"Error publishing to topic: {e}") # Используйте rospy.logerr

if __name__=='__main__':
    try:
        initNode()
        # Правильное определение имени топика (ВАЖНО!)
        topic_name = '/manip/joint1_position_controller/command'  # Пример
        publisher = rospy.Publisher(topic_name, Float64, queue_size=10)  # Больший queue_size
        rospy.sleep(1) # Дать время publisher'у зарегистрироваться

        position = 0.0 # Инициализация position ВНУТРИ main (решает проблему с областью видимости)
        pos_mode = 1
        
        
        while not rospy.is_shutdown():
            send(publisher, position) # Передаем publisher и position в функцию
            if (pos_mode == 1):
                position += 0.5
                if (position == 3.5):
                		pos_mode = 0
            if (pos_mode == 0):
                position -= 0.5
                if (position == -3.5):
                		position += 0.5
                		pos_mode = 1
            
            rospy.sleep(1) # Sleep после публикации


    except rospy.ROSInterruptException:
        pass # Нормальное завершение при Ctrl+C
    except Exception as e:
        rospy.logerr(f"Unexpected error: {e}") # Обработка других ошибок
        
