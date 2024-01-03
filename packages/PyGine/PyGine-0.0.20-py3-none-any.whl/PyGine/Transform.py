from PyGine.Vector3 import Vector3


class Transform :
    def __init__(self):

        self.position = Vector3(0,0,0)
        self.rotation = Vector3()
        self.scale = Vector3(1,1,1)

    def __str__(self):
        return "Transform(%s, %s, %s)" % (self.position, self.rotation, self.scale)

    def isPointInside(self, point):
        return self.position.x <= point.x <= self.position.x + self.scale.x and self.position.y <= point.y <= self.position.y + self.scale.y