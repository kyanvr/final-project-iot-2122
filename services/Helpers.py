import cv2 as cv

class Helpers:
    def putTextRect(img, text, pos, scale=3, thickness=3, colorT=(255, 255, 255),
                    colorR=(109, 67, 126), font=cv.FONT_HERSHEY_PLAIN,
                    offset=10, border=None, colorB=(0, 255, 0)):
        """
        Creates Text with Rectangle Background
        :param img: Image to put text rect on
        :param text: Text inside the rect
        :param pos: Starting position of the rect x1,y1
        :param scale: Scale of the text
        :param thickness: Thickness of the text
        :param colorT: Color of the Text
        :param colorR: Color of the Rectangle
        :param font: Font used. Must be cv.FONT....
        :param offset: Clearance around the text
        :param border: Outline around the rect
        :param colorB: Color of the outline
        :return: image, rect (x1,y1,x2,y2)
        """
        ox, oy = pos
        (w, h), _ = cv.getTextSize(text, font, scale, thickness)
 
        x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset
        cv.rectangle(img, (x1, y1), (x2, y2), colorR, cv.FILLED)
        if border is not None:
            cv.rectangle(img, (x1, y1), (x2, y2), colorB, border)
        cv.putText(img, text, (ox, oy), font, scale, colorT, thickness)
 
        return img, [x1, y2, x2, y1]