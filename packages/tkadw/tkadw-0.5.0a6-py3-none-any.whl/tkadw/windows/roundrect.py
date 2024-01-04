class RoundRect:
    def __init__(self):
        from tkinter import _default_root, Tk
        self.tk: Tk = _default_root
        self.init1()

    def init1(self):
        """
        初始化圆角矩形模块
        参见：https://wiki.tcl-lang.org/page/Drawing+rounded+rectangles
        """
        self.tk.eval(
            """
proc roundRect2 {w L T Rad width height fill outline tag} {

  $w create oval $L $T [expr $L + $Rad] [expr $T + $Rad] -fill $fill -outline $outline -tag $tag
  $w create oval [expr $width-$Rad] $T $width [expr $T + $Rad] -fill $fill -outline $outline -tag $tag
  $w create oval $L [expr $height-$Rad] [expr $L+$Rad] $height -fill $fill -outline $outline -tag $tag
  $w create oval [expr $width-$Rad] [expr $height-$Rad] [expr $width] $height -fill $fill -outline $outline -tag $tag
  $w create rectangle [expr $L + ($Rad/2.0)] $T [expr $width-($Rad/2.0)] $height -fill $fill -outline $outline -tag $tag
  $w create rectangle $L [expr $T + ($Rad/2.0)] $width [expr $height-($Rad/2.0)] -fill $fill -outline $outline -tag $tag
}
            """
        )

    from tkinter import Canvas

    def draw(self, canvas, x, y, width, height, fill, outline, tag, radius):
        """
        绘制圆角矩形（方式1）

        Args:
            canvas (Canvas): 被绘制的画布
            x (int): 圆角矩形在画布上X轴坐标
            y (int): 圆角矩形在画布上Y轴坐标
            width (int): 圆角矩形的宽度
            height (int): 圆角矩形的高度
            fill (str): 圆角矩形填充颜色
            outline (str): 圆角矩形边框颜色
            tag (str): 圆角矩形标签
            radius (int): 圆角矩形圆角大小
        """
        _rect = self.tk.call("roundRect2", canvas._w, x, y, radius, width, height, fill, outline, tag)
        return _rect

    def draw2(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """
        绘制圆角矩形（方式2）

        Args:
            canvas (Canvas): 被绘制的画布
            x1 (int): 圆角矩形在画布上X轴开始坐标
            y1 (int): 圆角矩形在画布上Y轴开始坐标
            x2 (int): 圆角矩形在画布上X轴结束坐标
            y2 (int): 圆角矩形在画布上Y轴结束坐标
            radius (int): 圆角矩形圆角大小
        """
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        return canvas.create_polygon(points, **kwargs, smooth=True)
