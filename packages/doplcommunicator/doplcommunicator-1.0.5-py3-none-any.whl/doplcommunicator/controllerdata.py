import json

class ControllerData():
    def __init__(self, enabled: bool, x: float, y: float, z: float, rx: float, ry: float, rz: float, rw: float):
        self.enabled = enabled
        self.position = Position(x, y, z)
        self.rotation = Quaternion(rx, ry, rz, rw)

    @classmethod
    def fromDict(self, controller_data):
        print(controller_data)
        return ControllerData(controller_data["enabled"], controller_data["position"]["x"], controller_data["position"]["y"], controller_data["position"]["z"],
            controller_data["rotation"]["x"], controller_data["rotation"]["y"], controller_data["rotation"]["z"], controller_data["rotation"]["w"])

    def toDict(self):
        return {
            "enabled": self.enabled,
            "position": self.position.toDict(),
            "rotation": self.rotation.toDict(),
        }

    def __eq__(self, other): 
        if not isinstance(other, ControllerData):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        return self.enabled == other.enabled and \
            self.position == other.position and \
            self.rotation == other.rotation

class Position:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def toDict(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }

    def __eq__(self, other): 
        if not isinstance(other, Position):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and \
            self.y == other.y and \
            self.z == other.z
    
class Quaternion:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def toDict(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "w": self.w,
        }

    def __eq__(self, other): 
        if not isinstance(other, Quaternion):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and \
            self.y == other.y and \
            self.z == other.z and \
            self.w == other.w