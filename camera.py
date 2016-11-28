
class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0

        self.width = width 
        self.height = height

    def update(self, target, track):
	# Limits the camera to the track perimeter
	if((target.pose.x-self.width/2)<track.rect.left):
            self.x = track.rect.left
	elif((target.pose.x+self.width/2)>track.rect.right):
		self.x = self.width-track.rect.right
	else:
		self.x = -target.pose.x + self.width/2

	if((target.pose.y-self.height/2)<track.rect.top):
            self.y = track.rect.top
	elif((target.pose.y+self.height/2)>track.rect.bottom):
		self.y = self.height-track.rect.bottom
	else:
            self.y = -target.pose.y + self.height/2

    def apply(self, target):
        return target.rect.move(self.x, self.y)

