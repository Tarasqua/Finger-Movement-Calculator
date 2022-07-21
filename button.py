import cv2


class Button:

    def __init__(self, position: tuple, width: int, height: int, value: int):
        self.position = position
        self.width = width
        self.height = height
        self.value = value

    def draw_button(self, img: None, rectangle_color: tuple = (0, 149, 255), text_color: tuple = (50, 50, 50),
                    font_scale: float = 2, thickness: int = 2):
        # Alignment
        text_size = cv2.getTextSize(text=self.value, fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=font_scale, thickness=thickness)
        text_x = int(self.position[0] + self.width / 2 - text_size[1])
        text_y = int(self.position[1] + self.height / 2 + text_size[1])
        # Drawing
        cv2.rectangle(img=img, pt1=self.position, pt2=(self.position[0] + self.width, self.position[1] + self.height),
                      color=rectangle_color, thickness=cv2.FILLED)
        cv2.rectangle(img=img, pt1=self.position, pt2=(self.position[0] + self.width, self.position[1] + self.height),
                      color=(50, 50, 50), thickness=3)
        cv2.putText(img=img, text=self.value, org=(text_x, text_y), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=font_scale, color=text_color, thickness=thickness)

    def check_click(self, x, y, img: None):
        if self.position[0] < x < self.position[0] + self.width and \
                self.position[1] < y < self.position[1] + self.height:
            self.draw_button(img=img, rectangle_color=(121, 188, 255),
                             text_color=(0, 0, 0), font_scale=2.5, thickness=2)
            return True
        else:
            return False
