import matplotlib.pyplot as plt
import matplotlib.patches as pltp
import matplotlib.lines as pltl

import basicplot

# Create an instance of SimpleDraw
bp = basicplot.SimpleDraw()

# Test fill and no_fill methods
bp.fill("r")
assert bp._SimpleDraw__do_fill == True
assert bp._SimpleDraw__current_fill_color == "r"

bp.no_fill()
assert bp._SimpleDraw__do_fill == False

# Test stroke and no_stroke methods
bp.stroke("b")
assert bp._SimpleDraw__do_stroke == True
assert bp._SimpleDraw__current_stroke_color == "b"

bp.no_stroke()
assert bp._SimpleDraw__do_stroke == False

# Test line_style method
bp.line_style("--")
assert bp._SimpleDraw__current_line_style == "--"

# Test line_width method
bp.line_width(2.5)
assert bp._SimpleDraw__current_line_width == 2.5

# Test text_size method
bp.text_size(16)
assert bp._SimpleDraw__current_text_size == 16

# Test text_color method
bp.text_color("g")
assert bp._SimpleDraw__current_text_color == "g"

# Test ellipse method
bp.ellipse(0, 0, 5, 3)
# Assert that an Ellipse object is added to the plot
assert isinstance(plt.gca().patches[-1], pltp.Ellipse)

# Test circle method
bp.circle(2, 2, 4)
# Assert that an Ellipse object is added to the plot
assert isinstance(plt.gca().patches[-1], pltp.Ellipse)

# Test rect method
bp.rect(1, 1, 6, 4)
# Assert that a Rectangle object is added to the plot
assert isinstance(plt.gca().patches[-1], pltp.Rectangle)

# Test line method
bp.line(0, 0, 5, 5)
# Assert that a Line2D object is added to the plot
assert isinstance(plt.gca().lines[-1], pltl.Line2D)

# Test text method
bp.text(3, 3, "Hello")
# Assert that a Text object is added to the plot
assert isinstance(plt.gca().texts[-1], plt.Text)

# Test show method
bp.show()
# Assert that the plot is displayed
assert plt.fignum_exists(plt.gcf().number) == True

print("All tests passed!")