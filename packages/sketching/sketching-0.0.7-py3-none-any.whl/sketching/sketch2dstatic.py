"""Pillow-based renderer for Sketching.

License:
    BSD
"""

import copy
import math
import typing
import PIL.Image
import PIL.ImageColor
import PIL.ImageFont

has_matplot_lib = False
try:
    import matplotlib.pyplot
    has_matplot_lib = True
except:
    pass


has_numpy_lib = False
try:
    import numpy
    has_numpy_lib = True
except:
    pass

import sketching.abstracted
import sketching.const
import sketching.control_struct
import sketching.data_struct
import sketching.local_data_struct
import sketching.pillow_util
import sketching.state_struct
import sketching.transform

COLOR_TUPLE = typing.Union[typing.Tuple[int, int, int], typing.Tuple[int, int, int, int]]
DEFAULT_FPS = 20
MANUAL_OFFSET = False


class Rect:
    """Simple structure describing a region in a sketch."""

    def __init__(self, x: float, y: float, width: float, height: float):
        """Create a new region.

        Args:
            x: The x coordinate for the left side of the rectangle.
            y: The y coordinate for the top of the rectangle.
            width: Horizontal size of the rectangle in pixels.
            height: Vertical size of the rectangle in pixels.
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def get_x(self) -> float:
        """Get the starting x coordinate of this region.

        Returns:
            The x coordinate for the left side of the rectangle.
        """
        return self._x

    def get_y(self) -> float:
        """Get the starting y coordinate of this region.

        Returns:
            The y coordinate for the top of the rectangle.
        """
        return self._y

    def set_x(self, x: float):
        """"Set the starting x coordinate of this region.

        Args:
            x: The x coordinate for the left side of the rectangle.
        """
        self._x = x

    def set_y(self, y: float):
        """Set the starting y coordinate of this region.

        Args:
            y: The y coordinate for the top of the rectangle.
        """
        self._y = y

    def get_width(self) -> float:
        """Get the width of this region.

        Returns:
            Horizontal size of the rectangle in pixels.
        """
        return self._width

    def get_height(self) -> float:
        """Get the height of this region.

        Returns;
            Vertical size of the rectangle in pixels.
        """
        return self._height

    def get_center_x(self) -> float:
        """Get the middle x coordinate of this region.

        Returns:
            Center horizontal coordinate of this region.
        """
        return self.get_x() + self.get_width() / 2

    def get_center_y(self) -> float:
        """Get the middle y coordinate of this region.

        Returns:
            Center vertical coordinate of this region.
        """
        return self.get_y() + self.get_height() / 2

    def set_center_x(self, x: float):
        """Move this region by setting its center horizontal coordinate.

        Args:
            x: The x coordinate that should be the new center of the region.
        """
        new_x = x - self.get_width() / 2
        self.set_x(new_x)

    def set_center_y(self, y: float):
        """Move this region by setting its center vertical coordinate.

        Args:
            y: The y coordinate that should be the new center of the region.
        """
        new_y = y - self.get_height() / 2
        self.set_y(new_y)


class WritableImage:
    """Decorator around a Pillow image which can be written to."""

    def __init__(self, image: PIL.Image.Image, drawable: PIL.ImageDraw.ImageDraw):
        """Create a new writable image record.

        Args:
            image: The Pillow image that isn't writable.
            drawable: The version of image which can be written to.
        """
        self._image = image
        self._drawable = drawable

    def get_image(self) -> PIL.Image.Image:
        """Get the Pillow image.

        Returns:
            The Pillow image that isn't writable.
        """
        return self._image

    def get_drawable(self) -> PIL.ImageDraw.ImageDraw:
        """Get the version of the image which can be written to.

        Returns:
            The version of image which can be written to.
        """
        return self._drawable


class Sketch2DStatic(sketching.abstracted.Sketch):
    """Pillow-based Sketch renderer."""

    def __init__(self, width: int, height: int, title: typing.Optional[str] = None,
        loading_src: typing.Optional[str] = None):
        """Create a new Pillow-based sketch.

        Args:
            width: The width of the sketch in pixels. This will be used as the horizontal image
                size.
            height: The height of the sketch in pixels. This will be used as the vertical image
                size.
            title: Title for the sketch. Ignored, reserved for future use.
            loading_src: ID for loading screen. Ignored, reserved for future use.
        """
        super().__init__()

        # System params
        self._width = width
        self._height = height

        # Internal image
        native_size = (self._width, self._height)
        target_image = PIL.Image.new('RGB', native_size)
        target_draw = PIL.ImageDraw.Draw(target_image, 'RGBA')
        self._target_writable = WritableImage(target_image, target_draw)

        # Other internals
        self._transformer = sketching.transform.Transformer()
        self._transformer_stack: typing.List[sketching.transform.Transformer] = []

    ############
    # Controls #
    ############

    def get_keyboard(self) -> typing.Optional[sketching.control_struct.Keyboard]:
        return None

    def get_mouse(self) -> typing.Optional[sketching.control_struct.Mouse]:
        return None

    ########
    # Data #
    ########

    def get_data_layer(self) -> typing.Optional[sketching.data_struct.DataLayer]:
        return sketching.local_data_struct.LocalDataLayer()

    ###########
    # Drawing #
    ###########

    def clear(self, color_hex: str):
        rect = (0, 0, self._width, self._height)
        self._target_writable.get_drawable().rectangle(rect, fill=color_hex, width=0)

    def draw_arc(self, x1: float, y1: float, x2: float, y2: float, a1: float,
        a2: float):
        state_machine = self._get_current_state_machine()

        stroke_enabled = state_machine.get_stroke_enabled()
        fill_enabled = state_machine.get_fill_enabled()
        stroke_native = state_machine.get_stroke_native()
        fill_native = state_machine.get_fill_native()
        stroke_weight = state_machine.get_stroke_weight()

        mode_native = state_machine.get_arc_mode_native()
        rect = self._build_rect_with_mode(x1, y1, x2, y2, mode_native)

        a1_rad = self._convert_to_radians(a1)
        a2_rad = self._convert_to_radians(a2)

        pillow_util_image = sketching.pillow_util.make_arc_image(
            rect.get_x(),
            rect.get_y(),
            rect.get_width(),
            rect.get_height(),
            a1_rad,
            a2_rad,
            stroke_enabled,
            fill_enabled,
            stroke_native if stroke_enabled else None,
            fill_native if fill_enabled else None,
            stroke_weight
        )

        self._draw_with_transform(
            pillow_util_image.get_image(),
            pillow_util_image.get_x(),
            pillow_util_image.get_y()
        )

    def draw_ellipse(self, x1: float, y1: float, x2: float, y2: float):
        current_machine = self._get_current_state_machine()
        mode_str = current_machine.get_ellipse_mode()
        native_mode = current_machine.get_ellipse_mode_native()

        def draw_method(target_surface, rect, fill, stroke, width):
            bounds = (
                rect.get_x(),
                rect.get_y(),
                rect.get_x() + rect.get_width(),
                rect.get_y() + rect.get_height()
            )
            target_surface.ellipse(bounds, fill=fill, outline=stroke, width=width)

        self._draw_primitive(x1, y1, x2, y2, mode_str, native_mode, draw_method)

    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        state_machine = self._get_current_state_machine()
        if not state_machine.get_stroke_enabled():
            return

        stroke_color = state_machine.get_stroke_native()
        stroke_weight = state_machine.get_stroke_weight_native()

        point_1 = self._transformer.transform(x1, y1)
        point_2 = self._transformer.transform(x2, y2)

        self._target_writable.get_drawable().line(
            (
                (point_1.get_x(), point_1.get_y()),
                (point_2.get_x(), point_2.get_y())
            ),
            fill=stroke_color,
            width=stroke_weight
        )

    def draw_rect(self, x1: float, y1: float, x2: float, y2: float):
        state_machine = self._get_current_state_machine()
        mode_str = state_machine.get_rect_mode()
        native_mode = state_machine.get_rect_mode_native()

        def draw_method(target_surface, rect, fill, stroke, width):
            bounds = (
                rect.get_x(),
                rect.get_y(),
                rect.get_x() + rect.get_width(),
                rect.get_y() + rect.get_height()
            )
            target_surface.rectangle(bounds, fill=fill, outline=stroke, width=width)

        self._draw_primitive(x1, y1, x2, y2, mode_str, native_mode, draw_method)

    def draw_shape(self, shape: sketching.shape_struct.Shape):
        if not shape.get_is_finished():
            raise RuntimeError('Finish your shape before drawing.')

        state_machine = self._get_current_state_machine()

        stroke_enabled = state_machine.get_stroke_enabled()
        fill_enabled = state_machine.get_fill_enabled()
        stroke_native = state_machine.get_stroke_native()
        fill_native = state_machine.get_fill_native()
        stroke_weight = state_machine.get_stroke_weight()

        pillow_util_image = sketching.pillow_util.make_shape_image(
            shape,
            stroke_enabled,
            fill_enabled,
            stroke_native if stroke_enabled else None,
            fill_native if fill_enabled else None,
            stroke_weight
        )

        self._draw_with_transform(
            pillow_util_image.get_image(),
            pillow_util_image.get_x(),
            pillow_util_image.get_y()
        )

    def draw_text(self, x: float, y: float, content: str):
        state_machine = self._get_current_state_machine()

        stroke_enabled = state_machine.get_stroke_enabled()
        fill_enabled = state_machine.get_fill_enabled()
        stroke_native = state_machine.get_stroke_native()
        fill_native = state_machine.get_fill_native()
        stroke_weight = state_machine.get_stroke_weight()

        text_font = state_machine.get_text_font_native()

        align_info = state_machine.get_text_align_native()
        anchor_str = align_info.get_horizontal_align() + align_info.get_vertical_align()

        pillow_util_image = sketching.pillow_util.make_text_image(
            x,
            y,
            content,
            text_font,
            stroke_enabled,
            fill_enabled,
            stroke_native,
            fill_native,
            stroke_weight,
            anchor_str
        )

        self._draw_with_transform(
            pillow_util_image.get_image(),
            pillow_util_image.get_x(),
            pillow_util_image.get_y()
        )

    ##########
    # Events #
    ##########

    def on_step(self, callback: sketching.abstracted.StepCallback):
        raise NotImplementedError('Events not available for static renderer.')

    def on_quit(self, callback: sketching.abstracted.QuitCallback):
        raise NotImplementedError('Events not available for static renderer.')

    #########
    # Image #
    #########

    def load_image(self, src: str) -> sketching.abstracted.Image:
        return PillowImage(src)

    def draw_image(self, x: float, y: float, image: sketching.abstracted.Image):
        if not image.get_is_loaded():
            return

        image_mode_native = self._get_current_state_machine().get_image_mode_native()

        rect = self._build_rect_with_mode(
            x,
            y,
            image.get_width(),
            image.get_height(),
            image_mode_native
        )

        surface = image.get_native()
        self._draw_with_transform(surface, rect.get_x(), rect.get_y())

    def save_image(self, path: str):
        self._target_writable.get_image().save(path)

    #########
    # State #
    #########

    def push_transform(self):
        self._transformer_stack.append(copy.deepcopy(self._transformer))

    def pop_transform(self):
        if len(self._transformer_stack) == 0:
            raise RuntimeError('Transformation stack empty.')

        self._transformer = self._transformer_stack.pop()

    ##########
    # System #
    ##########

    def get_native(self):
        return self._target_writable

    def set_fps(self, rate: int):
        raise NotImplementedError('Cannot set static renderer FPS as it cannot loop.')

    def set_title(self, title: str):
        raise NotImplementedError('Cannot set title for static renderer.')

    def quit(self):
        raise NotImplementedError('Cannot quit static renderer as it cannot loop.')

    def show(self, ax=None):
        if has_matplot_lib and has_numpy_lib:
            if ax is None:
                ax = matplotlib.pyplot.subplot(111)
                ax.axis('off')

            ax.imshow(numpy.asarray(self._target_writable.get_image()))
        else:
            raise RuntimeError('Install matplotlib and numpy or use save instead.')

    def show_and_quit(self, ax=None):
        pass

    #############
    # Transform #
    #############

    def translate(self, x: float, y: float):
        self._transformer.translate(x, y)

    def rotate(self, angle_mirror: float):
        angle = -1 * angle_mirror
        angle_rad = self._convert_to_radians(angle)
        self._transformer.rotate(angle_rad)

    def scale(self, scale: float):
        self._transformer.scale(scale)

    ###########
    # Support #
    ###########

    def _create_state_machine(self) -> sketching.state_struct.SketchStateMachine:
        return PillowSketchStateMachine()

    def _make_shape_surface(self, rect: Rect) -> WritableImage:
        native_size = (round(rect.get_width()), round(rect.get_height()))
        target_image = PIL.Image.new('RGBA', native_size, (255, 255, 255, 0))
        target_draw = PIL.ImageDraw.Draw(target_image, 'RGBA')
        return WritableImage(target_image, target_draw)

    def _offset_stroke_weight(self, rect: Rect, stroke_weight: float) -> Rect:
        if not MANUAL_OFFSET:
            return rect

        half_weight = stroke_weight / 2
        return Rect(
            rect.get_x() - half_weight,
            rect.get_y() - half_weight,
            rect.get_width() + half_weight * 2,
            rect.get_height() + half_weight * 2
        )

    def _offset_fill_weight(self, rect: Rect, stroke_weight: float) -> Rect:
        if not MANUAL_OFFSET:
            return rect

        half_weight = stroke_weight / 2
        return Rect(
            rect.get_x() + half_weight,
            rect.get_y() + half_weight,
            rect.get_width() - half_weight * 2,
            rect.get_height() - half_weight * 2
        )

    def _zero_rect(self, rect: Rect) -> Rect:
        return Rect(0, 0, rect.get_width(), rect.get_height())

    def _build_rect_with_mode(self, x1: float, y1: float, x2: float, y2: float,
        native_mode: int) -> Rect:
        if native_mode == sketching.const.CENTER:
            start_x = x1 - x2 / 2
            start_y = y1 - y2 / 2
            width = x2
            height = y2
        elif native_mode == sketching.const.RADIUS:
            start_x = x1 - x2
            start_y = y1 - y2
            width = x2 * 2
            height = y2 * 2
        elif native_mode == sketching.const.CORNER:
            start_x = x1
            start_y = y1
            width = x2
            height = y2
        elif native_mode == sketching.const.CORNERS:
            (x1, y1, x2, y2) = sketching.abstracted.reorder_coords(x1, y1, x2, y2)
            start_x = x1
            start_y = y1
            width = x2 - x1
            height = y2 - y1
        else:
            raise RuntimeError('Unknown mode: ' + str(native_mode))

        return Rect(start_x, start_y, width, height)

    def _draw_primitive(self, x1: float, y1: float, x2: float, y2: float,
        mode: str, native_mode, draw_method):
        state_machine = self._get_current_state_machine()
        has_fill = state_machine.get_fill_enabled()
        fill_color = state_machine.get_fill_native()
        has_stroke = state_machine.get_stroke_enabled()
        stroke_color = state_machine.get_stroke_native()
        rect = self._build_rect_with_mode(x1, y1, x2, y2, native_mode)
        stroke_weight = state_machine.get_stroke_weight_native()

        transformed_point = self._transformer.transform(
            rect.get_center_x(),
            rect.get_center_y()
        )

        rect = Rect(
            0,
            0,
            rect.get_width() * transformed_point.get_scale(),
            rect.get_height() * transformed_point.get_scale()
        )
        rect.set_center_x(transformed_point.get_x())
        rect.set_center_y(transformed_point.get_y())

        draw_method(
            self._target_writable.get_drawable(),
            rect,
            fill_color if has_fill else None,
            stroke_color if has_stroke else None,
            stroke_weight if has_stroke else 0
        )

    def _draw_with_transform(self, surface: PIL.Image.Image, x: float, y: float):
        start_rect = Rect(x, y, surface.width, surface.height)

        transformed_center = self._transformer.transform(
            start_rect.get_center_x(),
            start_rect.get_center_y()
        )

        has_scale = transformed_center.get_scale() != 1
        has_rotation = transformed_center.get_rotation() != 0
        has_content_transform = has_scale or has_rotation
        if has_content_transform:
            angle = transformed_center.get_rotation()
            angle_transform = math.degrees(angle)
            scale = transformed_center.get_scale()
            surface = surface.rotate(angle_transform, expand=True)
            surface = surface.resize((
                int(surface.width * scale),
                int(surface.height * scale)
            ))

        end_rect = Rect(x, y, surface.width, surface.height)
        end_rect.set_center_x(transformed_center.get_x())
        end_rect.set_center_y(transformed_center.get_y())

        native_pos = (int(end_rect.get_x()), int(end_rect.get_y()))
        self._target_writable.get_image().paste(surface, native_pos, surface)


class PillowSketchStateMachine(sketching.state_struct.SketchStateMachine):

    def __init__(self):
        super().__init__()
        self._fill_native = self._convert_color(super().get_fill())
        self._stroke_native = self._convert_color(super().get_stroke())
        self._font_cache = {}
        self._text_align_native = self._transform_text_align(super().get_text_align_native())

    def set_fill(self, fill: str):
        super().set_fill(fill)
        self._fill_native = self._convert_color(super().get_fill())

    def get_fill_native(self):
        return self._fill_native

    def set_stroke(self, stroke: str):
        super().set_stroke(stroke)
        self._stroke_native = self._convert_color(super().get_stroke())

    def get_stroke_native(self):
        return self._stroke_native

    def get_text_font_native(self):
        font = self.get_text_font()
        key = '%s.%d' % (font.get_identifier(), font.get_size())

        if key not in self._font_cache:
            new_font = PIL.ImageFont.truetype(font.get_identifier(), font.get_size())
            self._font_cache[key] = new_font

        return self._font_cache[key]

    def set_text_align(self, text_align: sketching.state_struct.TextAlign):
        super().set_text_align(text_align)
        self._text_align_native = self._transform_text_align(super().get_text_align_native())

    def get_text_align_native(self):
        return self._text_align_native

    def _transform_text_align(self,
        text_align: sketching.state_struct.TextAlign) -> sketching.state_struct.TextAlign:

        HORIZONTAL_ALIGNS = {
            sketching.const.LEFT: 'l',
            sketching.const.CENTER: 'm',
            sketching.const.RIGHT: 'r'
        }

        VERTICAL_ALIGNS = {
            sketching.const.TOP: 't',
            sketching.const.CENTER: 'm',
            sketching.const.BASELINE: 's',
            sketching.const.BOTTOM: 'b'
        }

        return sketching.state_struct.TextAlign(
            HORIZONTAL_ALIGNS[text_align.get_horizontal_align()],
            VERTICAL_ALIGNS[text_align.get_vertical_align()]
        )

    def _convert_color(self, target: str) -> COLOR_TUPLE:
        return PIL.ImageColor.getrgb(target)


class PillowImage(sketching.abstracted.Image):

    def __init__(self, src: str):
        super().__init__(src)
        self._native = PIL.Image.open(src)

    def get_width(self) -> float:
        return self._native.width

    def get_height(self) -> float:
        return self._native.height

    def resize(self, width: float, height: float):
        self._native = self._native.resize((int(width), int(height)))

    def get_native(self):
        return self._native

    def get_is_loaded(self):
        return True
