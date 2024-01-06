ARC = "arc"
CENTRAL = "central"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"
CIRCULAR = "circular"


class Gradient:
    def __init__(self):
        from tkinter import _default_root, Tk
        self.tk: Tk = _default_root
        self.init()

    def demo(self):
        """
        示例
        """
        self.tk.call("gradient", "demo")

    from tkinter import Canvas

    def draw(self,
             canvas: Canvas, tags: str,
             x: int, y: int, width: int, height: int,
             orient, color1, color2, **kw):
        """
        绘制渐变图形

        Args:
            canvas (Canvas): 被绘制的画布
            tags (str): 渐变图形标签
            x (int): 渐变图形在画布上X轴坐标
            y (int): 渐变图形在画布上Y轴坐标
            width (int): 渐变图形的宽度
            height (int): 渐变图形的高度
            orient (str): 渐变图形的形状，有"arc" "central" "vertical" "horizontal" "circular"
            color1 (str): 渐变颜色1
            color2 (str): 渐变颜色2
        """
        kwargs = []
        for k in kw:
            kwargs.append("-" + k)
            kwargs.append(kw[k])
        return self.tk.call(
            "gradient", "draw", canvas._w,
            tags, x, y, width, height, orient, color1, color2, *kwargs
        )

    def init(self):
        """
        初始化渐变模块
        参见：https://wiki.tcl-lang.org/page/Drawing+Gradients+on+a+Canvas
        """
        self.tk.eval(
            """
            # Create color gradients of various shapes and sizes on a canvas.
            #   Usage:
            #       gradient draw    <canvas> <tags> <x> <y> <width> <height> <vertical|horizontal|circular|central|arc> <color1> <color2>  ?-animate? ?option? ...
            #       gradient redraw  <canvas> <tags> <x> <y> <width> <height> <vertical|horizontal|circular|central|arc> <color1> <color2>  ?-animate? ?option? ...
            #       gradient resize  <canvas> <tags> <x> <y> <width> <height>
            #       gradient recolor <canvas> <tags> <color1> <color2>
    
            namespace eval gradient {
                namespace ensemble create -subcommands {
                    draw
                    redraw
                    recolor
                    resize
                    demo
                }
    
                # Create a gradient on a canvas. The gradient will be placed at the top of the display list.
                proc draw {canvas tags x y width height orient color1 color2 args} {
                    # Ensure valid colors are provided while also converting to lists of 16-bit RGB values.
                    if { [catch {winfo rgb . $color1} rgb1] } {
                        error "invalid color: $color1"
                    }
                    if { [catch {winfo rgb . $color2} rgb2] } {
                        error "invalid color: $color2"
                    }
    
                    # Delete the gradient if it already exists.
                    $canvas delete [join $tags &&]
    
                    # Create a hidden canvas item to store meta data about this gradient.
                    set meta_data [list x $x  y $y  width $width  height $height  orient $orient  color1 $color1  color2 $color2  args $args]
                    $canvas create line $x $y $x $y  -state hidden  -tags [list {*}$tags meta [list gradient: {*}$meta_data]]
    
                    # Intercept the -animate option.
                    if { "-animate" in $args} {
                        set index [lsearch $args "-animate"]
                        set args  [lreplace $args $index $index]
                        set animate 1
                    } else {
                        set animate 0
                    }
    
                    # Draw the gradient.
                    if { $orient eq "central" } {
                        # Create the canvas rectangle items.
                        foreach {x1 y1 x2 y2 color} [get_rects $x $y $width $height $rgb1 $rgb2] {
                            $canvas create rectangle $x1 $y1 $x2 $y2  -outline $color  -width 2  -tags $tags  {*}$args
                            if {$animate} {update}
                        }
                    } elseif { $orient eq "circular" } {
                        # Create the canvas oval items.
                        foreach {x1 y1 x2 y2 color} [get_rects $x $y $width $height $rgb1 $rgb2] {
                            $canvas create oval $x1 $y1 $x2 $y2  -outline $color  -width 2  -tags $tags  {*}$args
                            if {$animate} {update}
                        }
                    } elseif { $orient eq "arc" } {
                        # Create the canvas arc items.
                        foreach {x1 y1 x2 y2 color} [get_rects $x $y $width $height $rgb1 $rgb2] {
                            $canvas create arc $x1 $y1 $x2 $y2  -outline $color  -width 2  -tags $tags  -style arc  {*}$args
                            if {$animate} {update}
                        }
                    } elseif { $orient in [list "vertical" "horizontal"] } {        
                        # Create the canvas line items.
                        foreach {x1 y1 x2 y2 color} [get_lines $x $y $width $height $orient $rgb1 $rgb2] {
                            $canvas create line $x1 $y1 $x2 $y2  -fill $color  -tags $tags  -capstyle projecting  {*}$args
                            if {$animate} {update}
                        }
                    } else {
                        # Delete the meta data and throw an error.
                        $canvas delete [join $tags &&]
                        error "invalid orientation: $orient; must be: vertical, horizontal, circular, central, or arc"
                    }
    
                    return
                }
    
                # Same as draw, but if the gradient already exists then it will retain its position in the canvas's display list after being redrawn.
                proc redraw {canvas tags x y width height orient color1 color2 args} {
                    # If the gradient already exists, remember its location in the display list.
                    set item_above [$canvas find above [join $tags &&]]
    
                    # Draw the gradient.
                    draw $canvas $tags $x $y $width $height $orient $color1 $color2 {*}$args
    
                    # Move the gradient to its previous location in the display list, if any.
                    if { $item_above ne "" } {
                        $canvas lower [join $tags &&] $item_above
                    }
    
                    return
                }
    
                # Shortcut procedure to change the colors of the gradient. Same as redraw but introspectively determines some meta data. 
                # This will use the gradient's x/y location when it was last drawn.
                proc recolor {canvas tags color1 color2} {
                    # Retrieve the gradient's meta data.
                    set meta [get_meta_data $canvas $tags]
                    set meta [dict remove $meta color1 color2]
                    dict with meta {}
    
                    # Redraw the gradient with the new colors.
                    redraw $canvas $tags $x $y $width $height $orient $color1 $color2 {*}$args
                    return     
                }
    
                # Shortcut procedure to resize and reposition a gradient. Same as redraw but introspectively determines some meta data. 
                proc resize {canvas tags x y width height} {
                    # Retrieve the gradient's meta data.
                    set meta [get_meta_data $canvas $tags]
                    set meta [dict remove $meta x y width height]
                    dict with meta {}
    
                    # Recreate the canvas lines with the new dimensions.
                    redraw $canvas $tags $x $y $width $height $orient $color1 $color2 {*}$args
                    return
                }
    
                # Retrieve meta information on a gradient.
                proc get_meta_data {canvas tags} {
                    if { [string is integer -strict $tags] } {
                        # This is supposedly a canvas item ID instead of a list of tags describing a gradient. Avoid introducing subtle logic errors.
                        error "cannot provide canvas item ID in lieu of gradient tags: $tags"
                    }
                    # This is a list of tags for a gradient. Find the hidden meta item for this gradient.
                    set all_tags [$canvas gettags "meta&&[join $tags &&]"]
                    set meta_data [lrange [lsearch -inline -index 0 $all_tags "gradient:"] 1 end]
                    if { [llength $meta_data] == 0 } {
                        error "cannot find meta data for gradient with tags: $tags"
                    }
                    return $meta_data
                }
    
                # For a canvas item ID, return all tags that are not gradient meta tags.
                proc get_non_meta_tags {canvas id} {
                    set tags [$canvas gettags $id]
                    set index [lsearch $tags "meta"]
                    set tags [lreplace $tags $index $index]
                    set index [lsearch -index 0 $tags "gradient:"]
                    set tags [lreplace $tags $index $index]
                    return $tags
                }
    
                # Calculate a list of center-to-outward colored rectangles suitable for [canvas create rectangle] or [canvas create oval].
                proc get_rects {x y width height rgb1 rgb2} {
                    set rects [list]
                    set x1 [expr {int($x)+1}]
                    set y1 [expr {int($y)+1}]
                    set x2 [expr {$x1+$width-1}]
                    set y2 [expr {$y1+$height-1}]
    
                    # Calculate each rectangle.
                    if { $width > $height } {
                        # Decrement X by one pixel in both directions. Decrement Y by a fraction in both directions.
                        # The Y axis will be more heavily concentrated.
                        set ratio  [expr { 1.0*$height/$width }]
                        set length [expr { $width/2 }]
                        while { $x2 > $x1 } {
                            lappend rects $x1 $y1 $x2 $y2 [get_color $rgb1 $rgb2 $length [expr { ($x2-$x1)/2 }]]
                            set x1 [expr { $x1+1 }]
                            set x2 [expr { $x2-1 }]
                            set y1 [expr { $y1+$ratio }]
                            set y2 [expr { $y2-$ratio }]
                        }
                    } else {
                        # Decrement Y by one pixel in both directions. Decrement X by a fraction in both directions.
                        # The X axis will be more heavily concentrated (unless width==height).
                        set ratio  [expr { 1.0*$width/$height }]
                        set length [expr { $height/2 }]
                        while { $y2 > $y1 } {
                            lappend rects $x1 $y1 $x2 $y2 [get_color $rgb1 $rgb2 $length [expr { ($y2-$y1)/2 }]]
                            set x1 [expr { $x1+$ratio }]
                            set x2 [expr { $x2-$ratio }]
                            set y1 [expr { $y1+1 }]
                            set y2 [expr { $y2-1 }]
                        }
                    }
                    return $rects
                }
    
                # Calculate a list of left-to-right or top-to-bottom colored lines suitable for [canvas create line].
                proc get_lines {x1 y1 width height orient rgb1 rgb2} {
                    set lines [list]
                    set x1 [expr {int($x1)}]
                    set y1 [expr {int($y1)}]
                    set x2 [expr {$x1+$width}]
                    set y2 [expr {$y1+$height}]
                    if { $orient eq "vertical" } {
                        # Calculate the color for each horizontal line.
                        for {set y $y1} {$y < $y2} {incr y} {
                            lappend lines $x1 $y $x2 $y [get_color $rgb1 $rgb2 $height [expr {$y-$y1}]]
                        }
                    } elseif { $orient eq "horizontal" } {
                        # Calculate the color for each vertical column.
                        for {set x $x1} {$x < $x2} {incr x} {
                            lappend lines $x $y1 $x $y2 [get_color $rgb1 $rgb2 $width [expr {$x-$x1}]]
                        }
                    } else {
                        error "invalid orientation: $orient; must be: vertical or horizontal"
                    }
    
                    return $lines
                }
    
                # Calculates the color at the specified index between rgb1 and rgb2 where rgb1 and rgb2 are the specified length apart.
                proc get_color {rgb1 rgb2 length index} {
                    # Throw an error if the index is out of bounds.
                    if { $index < 0  ||  $index >= $length } {
                        error "index $index is out of bounds for length $length"
                    }
    
                    lassign $rgb1 r1 g1 b1
                    lassign $rgb2 r2 g2 b2
    
                    # Determine the ratio between each starting component color and ending component color.
                    set r_ratio [expr { 1.00*($r2-$r1+1)/$length }]
                    set g_ratio [expr { 1.00*($g2-$g1+1)/$length }]
                    set b_ratio [expr { 1.00*($b2-$b1+1)/$length }]
    
                    # Calculate the new component colors at the given index. 
                    set r [expr { int($r_ratio*$index+$r1) }]
                    set g [expr { int($g_ratio*$index+$g1) }]
                    set b [expr { int($b_ratio*$index+$b1) }]
    
                    # A hacky workaround to make up for a lack of precision (or faulty math?).
                    # The final pixel of the gradient should exactly match the color of rgb2
                    if { $index == [expr {$length-1}] } {
                        lassign $rgb2 r g b
                    }
    
                    # Convert the integer RGB values to a hex color.
                    return [rgb_to_hex [list $r $g $b]]
                }
    
                # Convert a list of 16-bit RGB values to an 8-bit hex color. Using 8-bit hex colors instead of 16-bit
                # speeds up drawing of images two-fold (I haven't benchmarked this for canvases).
                proc rgb_to_hex {rgb} {
                    lassign $rgb r g b
                    set r [format %02x [expr {$r/256}]]
                    set g [format %02x [expr {$g/256}]]
                    set b [format %02x [expr {$b/256}]]
                    return #$r$g$b
                }
    
                # Converts 8-bit RGB values to 16-bit RGB values.
                proc rgb_8_to_16_bit {rgb} {
                    lassign $rgb r g b
                    return [list [expr {$r*256}] [expr {$g*256}] [expr {$b*256}]]
                }
    
                # Returns a random 8-bit hex color.
                proc random_color {} {
                    return [rgb_to_hex "[expr {int(rand()*65536)}] [expr {int(rand()*65536)}] [expr {int(rand()*65536)}]"]
                }
    
                # Redraw all gradients with random colors
                proc randomize_all_gradient_colors {canvas} {
                    foreach id [$canvas find withtag meta] {
                        set tags [get_non_meta_tags $canvas $id]
                        recolor $canvas $tags [random_color] [random_color]
                    }
                  return
                }
    
                # Randomize colors for all canvas items.
                proc randomize_all_canvas_item_colors {canvas} {
                    foreach id [$canvas find withtag all] {
                        if { [$canvas type $id] in {window} } {
                            continue
                        }
                        $canvas itemconfigure $id -fill [random_color]
                        if { [$canvas type $id] in {rectangle arc oval} } {
                             $canvas itemconfigure $id -outline [random_color]
                        }
                    }
                    return
                }
    
                # Run a demonstration.
                proc demo {} {
                    # Create a toplevel window with a canvas filling the contents.
                    set win .gradients
                    if { [winfo exists $win] } {
                        destroy $win
                    }
                    toplevel $win
                    set cvs [canvas $win.cvs -highlightthickness 0]
                    pack $cvs -fill both -expand yes
                    wm geometry $win 800x600
                    raise $win
    
                    # Fill the bottom of the screen with a striped green fade.
                    gradient draw $cvs footer 0 0 10 10 vertical white darkgreen -dash {3 1}
                    bind $cvs <Configure> {
                        gradient resize %W footer 0 [expr {%h-300}] %w 300
                    }
    
                    # Draw a strip of rainbow.
                    set width  100
                    set colors {white red orange yellow green blue purple violet white}
                    for {set i 1} {$i < [llength $colors]} {incr i} {
                        set c1 [lindex $colors $i-1]
                        set c2 [lindex $colors $i]
                        gradient draw $cvs "wave $i" [expr {$width*($i-1)}] 0 $width 50 horizontal $c1 $c2
                    }
    
                    # Draw some balls with diameters of 100.
                    set colors {green red yellow blue orange white}
                    for {set i 0} {$i < 6} {incr i} {
                        gradient draw $cvs "beachball $i" 0 55 100 100 arc [lindex $colors $i] #333 -start [expr {$i*60}] -extent 60
                    }
                    set colors {cyan pink orange firebrick}
                    for {set i 0} {$i < [llength $colors]} {incr i} {
                        gradient draw $cvs "quadball $i" 110 55 100 100 arc [lindex $colors $i] #eee -start [expr {$i*90}] -extent 90
                    }
                    gradient draw $cvs ball1    220 55 100 100 circular #bbbbbb white
                    gradient draw $cvs ball2    330 55 100 100 circular #888 #eee
                    gradient draw $cvs ball3    440 55 100 100 circular black grey
                    gradient draw $cvs ball4    550 55 100 100 circular black #555
                    gradient draw $cvs ball5    660 55 100 100 circular cyan black
    
                    # Draw some boxes.
                    gradient draw $cvs box1   0 160 150 100 horizontal white firebrick
                    gradient draw $cvs box2 150 160 200 100 central    black firebrick
                    gradient draw $cvs box3 350 160 100 100 horizontal firebrick black
                    gradient draw $cvs box4 450 160 200 100 central    firebrick black
                    gradient draw $cvs box5 650 160 150 100 horizontal black white
    
                    # Display some control buttons.
                    frame $cvs.f
                    button $cvs.f.b1 -text "Redraw with random gradient colors" -command [list [namespace current]::randomize_all_gradient_colors $cvs]
                    button $cvs.f.b2 -text "Relaunch demo with default colors" -command [list [namespace current]::demo]
                    button $cvs.f.b3 -text "Chaos" -command [list [namespace current]::randomize_all_canvas_item_colors $cvs]
                    pack $cvs.f.b1 $cvs.f.b2 $cvs.f.b3 -fill x
                    $cvs create window 400 400 -window $cvs.f
    
                    return
                }
            }
                    """
        )

    def recolor(self, canvas: Canvas, tags: str, color1, color2):
        """
        修改渐变图形颜色

        Args:
            canvas (Canvas): 被绘制的画布
            tags (str): 渐变图形标签
            color1 (str): 渐变颜色1
            color2 (str): 渐变颜色2
        """
        return self.tk.call(
            "gradient", "recolor", canvas._w,
            tags, color1, color2
        )

    def redraw(self,
               canvas: Canvas, tags: str,
               x: int, y: int, width: int, height: int,
               orient, color1, color2, **kw
               ):
        """
        绘制渐变图形，与draw相同

        Args:
            canvas (Canvas): 被绘制的画布
            tags (str): 渐变图形标签
            x (int): 渐变图形在画布上X轴坐标
            y (int): 渐变图形在画布上Y轴坐标
            width (int): 渐变图形的宽度
            height (int): 渐变图形的高度
            orient (str): 渐变图形的形状，有"arc" "central" "vertical" "horizontal" "circular"
            color1 (str): 渐变颜色1
            color2 (str): 渐变颜色2
        """
        kwargs = []
        for k in kw:
            kwargs.append("-" + k)
            kwargs.append(kw[k])
        return self.tk.call(
            "gradient", "redraw", canvas._w,
            tags, x, y, width, height, orient, color1, color2, *kwargs
        )

    def resize(self, canvas: Canvas, tags: str, x: int, y: int, width: int, height: int):
        """
        修改渐变图形位置

        Args:
            canvas (Canvas): 被绘制的画布
            tags (str): 渐变图形标签
            x (int): 渐变图形在画布上X轴坐标
            y (int): 渐变图形在画布上Y轴坐标
            width (int): 渐变图形的宽度
            height (int): 渐变图形的高度
        """
        return self.tk.call(
            "gradient", "recolor", canvas._w,
            tags, x, y, width, height
        )


X = "x"
Y = "y"


class Gradient2:
    def __init__(self):
        from tkinter import _default_root, Tk
        self.tk: Tk = _default_root
        self.init1()

    from tkinter import Canvas

    def demo1(self):
        self.tk.eval(
            """
  canvas .grad1
  bind .grad1 <Configure> [list drawGradient .grad1 x red royalblue]
  
  canvas .grad2
  bind .grad2 <Configure> [list drawGradient .grad2 y yellow red]
  
  pack .grad1 .grad2 -fill both -expand 1
            """
        )

    def draw1(self, win: Canvas, type, col1Str, col2Str):
        """
        用渐变颜色填充画布

        Args:
            win (Canvas): 被绘制的画布
            type (str): 渐变的方向，有"x" "y"
            col1Str (str): 渐变颜色1
            col2Str (str): 渐变颜色2

        """
        return self.tk.call("drawGradient", win._w, type, col1Str, col2Str)

    def init1(self):
        """
        初始化渐变模块
        参见：https://wiki.tcl-lang.org/page/Drawing+Gradients+on+a+Canvas
        """
        self.tk.eval(
            """
  proc + {n1 n2} {
    expr {$n1 + $n2}
  }
  proc - {n1 n2} {
    expr {$n1 - $n2}
  }
  proc * {n1 n2} {
    expr {$n1 * $n2}
  }
  proc / {n1 n2} {
    expr {$n1 / $n2}
  }
  proc toInt {n} {
    expr int($n)
  }
  
  proc drawGradient {win type col1Str col2Str} {
    $win delete gradient
    
    set width [winfo width $win]
    set height [winfo height $win]
    
    lassign [winfo rgb $win $col1Str] r1 g1 b1
    lassign  [winfo rgb $win $col2Str] r2 g2 b2
    set rRange [- $r2.0 $r1]
    set gRange [- $g2.0 $g1]
    set bRange [- $b2.0 $b1]
  
    if {$type == "x"} {
      set rRatio [/ $rRange $width]
      set gRatio [/ $gRange $width]
      set bRatio [/ $bRange $width]
    
      for {set x 0} {$x < $width} {incr x} {
        set nR [toInt [+ $r1 [* $rRatio $x]]]
        set nG [toInt [+ $g1 [* $gRatio $x]]]
        set nB [toInt [+ $b1 [* $bRatio $x]]]
  
        set col [format {%4.4x} $nR]
        append col [format {%4.4x} $nG]
        append col [format {%4.4x} $nB]
        $win create line $x 0 $x $height -tags gradient -fill #${col}
      }
    } else {
      set rRatio [/ $rRange $height]
      set gRatio [/ $gRange $height]
      set bRatio [/ $bRange $height]
  
      for {set y 0} {$y < $height} {incr y} {
        set nR [toInt [+ $r1 [* $rRatio $y]]]
        set nG [toInt [+ $g1 [* $gRatio $y]]]
        set nB [toInt [+ $b1 [* $bRatio $y]]]
  
        set col [format {%4.4x} $nR]
        append col [format {%4.4x} $nG]
        append col [format {%4.4x} $nB]
        $win create line 0 $y $width $y -tags gradient -fill #${col}
      }
    }
    return $win
  }
            """
        )


if __name__ == '__main__':
    from tkinter import Tk, Canvas

    root = Tk()

    canvas = Canvas()

    gradient = Gradient()
    gradient.draw(canvas, "gradient-rect-v",
                  5, 5, 50, 50, VERTICAL,
                  "blue", "red")
    gradient.draw(canvas, "gradient-rect-h",
                  60, 5, 50, 50, HORIZONTAL,
                  "blue", "red")
    gradient.draw(canvas, "gradient-rect-c",
                  115, 5, 50, 50, CENTRAL,
                  "blue", "red")
    gradient.draw(canvas, "gradient-arc",
                  170, 5, 50, 50, ARC,
                  "blue", "red", start=45, extent=135)
    gradient.draw(canvas, "gradient-circular",
                  225, 5, 50, 50, CIRCULAR,
                  "blue", "red")
    gradient.recolor(canvas, "gradient-rect-h", "blue", "black")

    canvas.pack(fill="both", expand="yes")

    canvas2 = Canvas()

    gradient2 = Gradient2()
    gradient2.draw1(canvas2, X, "blue", "red")

    canvas2.pack(fill="both", expand="yes")

    root.mainloop()
