"""Pygame-based renderer for Sketching.

License:
    BSD
"""

import contextlib
import copy
import math
import typing

import PIL.Image
import PIL.ImageFont

with contextlib.redirect_stdout(None):
    import pygame
    import pygame.draw
    import pygame.image
    import pygame.key
    import pygame.locals
    import pygame.mouse

import sketching.abstracted
import sketching.const
import sketching.control_struct
import sketching.data_struct
import sketching.local_data_struct
import sketching.pillow_util
import sketching.sketch2d_keymap
import sketching.state_struct
import sketching.transform

DEFAULT_FPS = 20
MANUAL_OFFSET = False
OPTIONAL_SKETCH_CALLBACK = typing.Optional[typing.Callable[[sketching.abstracted.Sketch], None]]


class Sketch2DApp(sketching.abstracted.Sketch):
    """Create a new Pygame-based Sketch."""

    def __init__(self, width: int, height: int, title: typing.Optional[str] = None,
        loading_src: typing.Optional[str] = None):
        """Create a enw Pygame-based sketch.

        Args:
            width: The width of the sketch in pixels. This will be used for window width.
            height: The height of the sketch in pixels. This will be used for window height.
            title: Starting title for the application.
            loading_src: ID for loading screen. Ignored, reserved for future use.
        """
        super().__init__()

        # System params
        self._width = width
        self._height = height

        # Callbacks
        self._callback_step: OPTIONAL_SKETCH_CALLBACK = None
        self._callback_quit: OPTIONAL_SKETCH_CALLBACK = None

        # User configurable state
        self._state_frame_rate = DEFAULT_FPS

        # Internal state
        self._internal_pre_show_actions: typing.List[typing.Callable] = []
        self._internal_quit_requested = False
        self._internal_surface = None
        self._internal_clock = pygame.time.Clock()
        self._transformer = sketching.transform.Transformer()
        self._transformer_stack: typing.List[sketching.transform.Transformer] = []

        # Inputs
        self._mouse = PygameMouse()
        self._keyboard = PygameKeyboard()

        # Internal struct
        self._struct_event_handlers = {
            pygame.KEYDOWN: lambda x: self._process_key_down(x),
            pygame.KEYUP: lambda x: self._process_key_up(x),
            pygame.MOUSEBUTTONDOWN: lambda x: self._process_mouse_down(x),
            pygame.MOUSEBUTTONUP: lambda x: self._process_mouse_up(x),
            pygame.locals.QUIT: lambda x: self._process_quit(x)
        }

        # Default window properties
        self.set_title('Sketching.py Sketch' if title is None else title)

    ############
    # Controls #
    ############

    def get_keyboard(self) -> typing.Optional[sketching.control_struct.Keyboard]:
        return self._keyboard

    def get_mouse(self) -> typing.Optional[sketching.control_struct.Mouse]:
        return self._mouse

    ########
    # Data #
    ########

    def get_data_layer(self) -> typing.Optional[sketching.data_struct.DataLayer]:
        return sketching.local_data_struct.LocalDataLayer()

    ###########
    # Drawing #
    ###########

    def clear(self, color_hex: str):
        if self._internal_surface is None:
            self._internal_pre_show_actions.append(lambda: self.clear(color_hex))
            return

        self._internal_surface.fill(pygame.Color(color_hex))

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

        transformer = self._transformer.quick_copy()

        def execute_draw():
            pillow_util_image = sketching.pillow_util.make_arc_image(
                rect.x,
                rect.y,
                rect.w,
                rect.h,
                a1_rad,
                a2_rad,
                stroke_enabled,
                fill_enabled,
                self._to_pillow_rgba(stroke_native) if stroke_enabled else None,
                self._to_pillow_rgba(fill_native) if fill_enabled else None,
                stroke_weight
            )

            native_image = self._convert_pillow_image(pillow_util_image.get_image())

            self._blit_with_transform(
                native_image,
                rect.centerx,
                rect.centery,
                transformer
            )

        if self._internal_surface is None:
            self._internal_pre_show_actions.append(execute_draw)
        else:
            execute_draw()

    def draw_ellipse(self, x1: float, y1: float, x2: float, y2: float):
        current_machine = self._get_current_state_machine()
        mode_str = current_machine.get_ellipse_mode()
        native_mode = current_machine.get_ellipse_mode_native()
        draw_method = pygame.draw.ellipse
        self._draw_primitive(x1, y1, x2, y2, mode_str, native_mode, draw_method)

    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        state_machine = self._get_current_state_machine()
        if not state_machine.get_stroke_enabled():
            return

        stroke_color = state_machine.get_stroke_native()
        stroke_weight = state_machine.get_stroke_weight_native()

        transformer = self._transformer.quick_copy()

        def execute_draw():
            min_x = min([x1, x2])
            max_x = max([x1, x2])
            width = max_x - min_x + 2 * stroke_weight

            min_y = min([y1, y2])
            max_y = max([y1, y2])
            height = max_y - min_y + 2 * stroke_weight

            rect = pygame.Rect(0, 0, width, height)
            target_surface = self._make_shape_surface(rect)

            def adjust(target):
                return (
                    target[0] - min_x + stroke_weight,
                    target[1] - min_y + stroke_weight,
                )

            pygame.draw.line(
                target_surface,
                stroke_color,
                adjust((x1, y1)),
                adjust((x2, y2)),
                width=stroke_weight
            )

            center_x = (max_x + min_x) / 2
            center_y = (max_y + min_y) / 2
            self._blit_with_transform(target_surface, center_x, center_y, transformer)

        if self._internal_surface is None:
            self._internal_pre_show_actions.append(execute_draw)
        else:
            execute_draw()

    def draw_rect(self, x1: float, y1: float, x2: float, y2: float):
        state_machine = self._get_current_state_machine()
        mode_str = state_machine.get_rect_mode()
        native_mode = state_machine.get_rect_mode_native()
        draw_method = pygame.draw.rect
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

        transformer = self._transformer.quick_copy()

        def execute_draw():
            pillow_util_image = sketching.pillow_util.make_shape_image(
                shape,
                stroke_enabled,
                fill_enabled,
                self._to_pillow_rgba(stroke_native) if stroke_enabled else None,
                self._to_pillow_rgba(fill_native) if fill_enabled else None,
                stroke_weight
            )

            native_image = self._convert_pillow_image(pillow_util_image.get_image())

            min_x = shape.get_min_x()
            max_x = shape.get_max_x()
            center_x = (max_x + min_x) / 2

            min_y = shape.get_min_y()
            max_y = shape.get_max_y()
            center_y = (max_y + min_y) / 2

            self._blit_with_transform(
                native_image,
                center_x,
                center_y,
                transformer
            )

        if self._internal_surface is None:
            self._internal_pre_show_actions.append(execute_draw)
        else:
            execute_draw()

    def draw_text(self, x: float, y: float, content: str):
        state_machine = self._get_current_state_machine()

        stroke_enabled = state_machine.get_stroke_enabled()
        fill_enabled = state_machine.get_fill_enabled()
        stroke_native = state_machine.get_stroke_native()
        fill_native = state_machine.get_fill_native()
        stroke_weight = state_machine.get_stroke_weight()

        text_font = state_machine.get_text_font_native()
        fill_pillow = self._to_pillow_rgba(fill_native)
        stroke_pillow = self._to_pillow_rgba(stroke_native)

        align_info = state_machine.get_text_align_native()
        anchor_str = align_info.get_horizontal_align() + align_info.get_vertical_align()

        transformer = self._transformer.quick_copy()

        def execute_draw():
            pillow_util_image = sketching.pillow_util.make_text_image(
                x,
                y,
                content,
                text_font,
                stroke_enabled,
                fill_enabled,
                stroke_pillow,
                fill_pillow,
                stroke_weight,
                anchor_str
            )

            native_image = self._convert_pillow_image(pillow_util_image.get_image())

            self._blit_with_transform(
                native_image,
                pillow_util_image.get_x() + pillow_util_image.get_width() / 2,
                pillow_util_image.get_y() + pillow_util_image.get_height() / 2,
                transformer
            )

        if self._internal_surface is None:
            self._internal_pre_show_actions.append(execute_draw)
        else:
            execute_draw()

    ##########
    # Events #
    ##########

    def on_step(self, callback: sketching.abstracted.StepCallback):
        self._callback_step = callback

    def on_quit(self, callback: sketching.abstracted.QuitCallback):
        self._callback_quit = callback

    #########
    # Image #
    #########

    def load_image(self, src: str) -> sketching.abstracted.Image:
        return PygameImage(src)

    def draw_image(self, x: float, y: float, image: sketching.abstracted.Image):
        if not image.get_is_loaded():
            return

        transformer = self._transformer.quick_copy()

        image_mode_native = self._get_current_state_machine().get_image_mode_native()

        def execute_draw():
            rect = self._build_rect_with_mode(
                x,
                y,
                image.get_width(),
                image.get_height(),
                image_mode_native
            )

            surface = image.get_native()
            self._blit_with_transform(surface, rect.centerx, rect.centery, transformer)

        if self._internal_surface is None:
            self._internal_pre_show_actions.append(execute_draw)
        else:
            execute_draw()

    def save_image(self, path: str):
        def execute_save():
            pygame.image.save(self._internal_surface, path)

        if self._internal_surface is None:
            self._internal_pre_show_actions.append(execute_save)
            self.show_and_quit()
        else:
            execute_save()

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
        if self._internal_surface is None:
            raise RuntimeError('Need to show sketch first before surface is available.')

        return self._internal_surface

    def set_fps(self, rate: int):
        self._state_frame_rate = rate

    def set_title(self, title: str):
        def execute():
            pygame.display.set_caption(title)

        if self._internal_surface is None:
            self._internal_pre_show_actions.append(execute)
        else:
            execute()

    def quit(self):
        self._internal_quit_requested = True

    def show(self, ax=None):
        self._show_internal(ax=ax, quit_immediately=False)

    def show_and_quit(self, ax=None):
        self._show_internal(ax=ax, quit_immediately=True)

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

    def _show_internal(self, ax=None, quit_immediately=False):
        pygame.init()
        self._internal_surface = pygame.display.set_mode((self._width, self._height))

        for action in self._internal_pre_show_actions:
            action()

        self._inner_loop(quit_immediately=quit_immediately)

    def _inner_loop(self, quit_immediately=False):
        while not self._internal_quit_requested:

            for event in pygame.event.get():
                self._process_event(event)

            if self._callback_step is not None:
                self._callback_step(self)

            pygame.display.update()
            self._internal_clock.tick(self._state_frame_rate)

            if quit_immediately:
                self._internal_quit_requested = True

        if self._callback_quit is not None:
            self._callback_quit(self)

    def _process_event(self, event):
        if event.type not in self._struct_event_handlers:
            return

        self._struct_event_handlers[event.type](event)

    def _process_quit(self, event):
        self._internal_quit_requested = True

    def _process_mouse_down(self, event):
        self._mouse.report_mouse_down(event)

    def _process_mouse_up(self, event):
        self._mouse.report_mouse_down(event)

    def _process_key_down(self, event):
        self._keyboard.report_key_down(event)

    def _process_key_up(self, event):
        self._keyboard.report_key_up(event)

    def _create_state_machine(self) -> sketching.state_struct.SketchStateMachine:
        return PygameSketchStateMachine()

    def _make_shape_surface(self, rect: pygame.Rect) -> pygame.Surface:
        return pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)

    def _offset_stroke_weight(self, rect: pygame.Rect, stroke_weight: float) -> pygame.Rect:
        if not MANUAL_OFFSET:
            return rect

        half_weight = stroke_weight / 2
        return pygame.Rect(
            rect.x - half_weight,
            rect.y - half_weight,
            rect.w + half_weight * 2,
            rect.h + half_weight * 2
        )

    def _offset_fill_weight(self, rect: pygame.Rect, stroke_weight: float) -> pygame.Rect:
        if not MANUAL_OFFSET:
            return rect

        half_weight = stroke_weight / 2
        return pygame.Rect(
            rect.x + half_weight,
            rect.y + half_weight,
            rect.w - half_weight * 2,
            rect.h - half_weight * 2
        )

    def _zero_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(0, 0, rect.w, rect.h)

    def _build_rect_with_mode(self, x1: float, y1: float, x2: float, y2: float,
        native_mode: int) -> pygame.Rect:
        if native_mode == sketching.const.CENTER:
            start_x = x1 - math.floor(x2 / 2)
            start_y = y1 - math.floor(y2 / 2)
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
            width = x2 + 1
            height = y2
        elif native_mode == sketching.const.CORNERS:
            (x1, y1, x2, y2) = sketching.abstracted.reorder_coords(x1, y1, x2, y2)
            start_x = x1
            start_y = y1
            width = x2 - x1
            height = y2 - y1
        else:
            raise RuntimeError('Unknown mode: ' + str(native_mode))

        return pygame.Rect(start_x, start_y, width, height)

    def _draw_primitive(self, x1: float, y1: float, x2: float, y2: float,
        mode: str, native_mode, draw_method):
        state_machine = self._get_current_state_machine()
        has_fill = state_machine.get_fill_enabled()
        fill_color = state_machine.get_fill_native()
        has_stroke = state_machine.get_stroke_enabled()
        stroke_color = state_machine.get_stroke_native()
        rect = self._build_rect_with_mode(x1, y1, x2, y2, native_mode)
        stroke_weight = state_machine.get_stroke_weight_native()

        transformer = self._transformer.quick_copy()

        def execute_draw_piece(color, strategy):
            target_surface = self._make_shape_surface(rect)
            rect_adj = self._zero_rect(rect)

            strategy(target_surface, rect_adj)

            self._blit_with_transform(
                target_surface,
                rect.centerx,
                rect.centery,
                transformer
            )

        def execute_draw():
            if has_fill:
                execute_draw_piece(
                    fill_color,
                    lambda surface, rect: draw_method(
                        surface,
                        fill_color,
                        self._offset_fill_weight(rect, stroke_weight),
                        0
                    )
                )

            if has_stroke:
                execute_draw_piece(
                    stroke_color,
                    lambda surface, rect: draw_method(
                        surface,
                        stroke_color,
                        self._offset_stroke_weight(rect, stroke_weight),
                        stroke_weight
                    )
                )

        if self._internal_surface is None:
            self._internal_pre_show_actions.append(execute_draw)
            return
        else:
            execute_draw()

    def _to_pillow_rgba(self, target: pygame.Color):
        return (target.r, target.g, target.b, target.a)

    def _convert_pillow_image(self, target: PIL.Image.Image) -> pygame.Surface:
        return pygame.image.fromstring(
            target.tobytes(),
            target.size,
            target.mode  # type: ignore
        ).convert_alpha()

    def _blit_with_transform(self, surface: pygame.Surface, x: float, y: float,
        transformer: sketching.transform.Transformer):
        start_rect = surface.get_rect()
        start_rect.centerx = x  # type: ignore
        start_rect.centery = y  # type: ignore

        transformed_center = transformer.transform(
            start_rect.centerx,
            start_rect.centery
        )

        has_scale = transformed_center.get_scale() != 1
        has_rotation = transformed_center.get_rotation() != 0
        has_content_transform = has_scale or has_rotation
        if has_content_transform:
            angle = transformed_center.get_rotation()
            angle_transform = math.degrees(angle)
            scale = transformed_center.get_scale()
            surface = pygame.transform.rotozoom(surface, angle_transform, scale)
            end_rect = surface.get_rect()
        else:
            end_rect = start_rect

        end_rect.centerx = transformed_center.get_x()  # type: ignore
        end_rect.centery = transformed_center.get_y()  # type: ignore

        assert self._internal_surface is not None
        self._internal_surface.blit(surface, (end_rect.x, end_rect.y))


class PygameSketchStateMachine(sketching.state_struct.SketchStateMachine):
    """Implementation of SketchStateMachine for Pygame types."""

    def __init__(self):
        """Create a new state machine for Pygame-based sketches."""
        super().__init__()
        self._fill_native = pygame.Color(super().get_fill())
        self._stroke_native = pygame.Color(super().get_stroke())
        self._font_cache = {}
        self._text_align_native = self._transform_text_align(super().get_text_align_native())

    def set_fill(self, fill: str):
        super().set_fill(fill)
        self._fill_native = pygame.Color(super().get_fill())

    def get_fill_native(self):
        return self._fill_native

    def set_stroke(self, stroke: str):
        super().set_stroke(stroke)
        self._stroke_native = pygame.Color(super().get_stroke())

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


class PygameImage(sketching.abstracted.Image):
    """Strategy implementation for Pygame images."""

    def __init__(self, src: str):
        """Create a new image.

        Args:
            src: Path to the image.
        """
        super().__init__(src)
        self._native = pygame.image.load(self.get_src())
        self._converted = False

    def get_width(self) -> float:
        return self._native.get_rect().width

    def get_height(self) -> float:
        return self._native.get_rect().height

    def resize(self, width: float, height: float):
        self._native = pygame.transform.scale(self._native, (width, height))

    def get_native(self):
        if not self._converted:
            self._native.convert_alpha()

        return self._native

    def get_is_loaded(self):
        return True


class PygameMouse(sketching.control_struct.Mouse):
    """Strategy implementation for Pygame-based mouse access."""

    def __init__(self):
        """Create a new mouse strategy using Pygame."""
        super().__init__()
        self._press_callback = None
        self._release_callback = None

    def get_pointer_x(self):
        return pygame.mouse.get_pos()[0]

    def get_pointer_y(self):
        return pygame.mouse.get_pos()[1]

    def get_buttons_pressed(self) -> sketching.control_struct.Buttons:
        is_left_pressed = pygame.mouse.get_pressed()[0]
        is_right_pressed = pygame.mouse.get_pressed()[2]
        buttons_clicked = []

        if is_left_pressed:
            buttons_clicked.append(sketching.const.MOUSE_LEFT_BUTTON)

        if is_right_pressed:
            buttons_clicked.append(sketching.const.MOUSE_RIGHT_BUTTON)

        return map(lambda x: sketching.control_struct.Button(x), buttons_clicked)

    def on_button_press(self, callback: sketching.control_struct.MouseCallback):
        self._press_callback = callback

    def on_button_release(self, callback: sketching.control_struct.MouseCallback):
        self._release_callback = callback

    def report_mouse_down(self, event):
        if self._press_callback is None:
            return

        if event.button == 1:
            button = sketching.control_struct.Button(sketching.const.MOUSE_LEFT_BUTTON)
            self._press_callback(button)
        elif event.button == 3:
            button = sketching.control_struct.Button(sketching.const.MOUSE_RIGHT_BUTTON)
            self._press_callback(button)

    def report_mouse_up(self, event):
        if self._release_callback is None:
            return

        if event.button == 1:
            button = sketching.control_struct.Button(sketching.const.MOUSE_LEFT_BUTTON)
            self._release_callback(button)
        elif event.button == 3:
            button = sketching.control_struct.Button(sketching.const.MOUSE_RIGHT_BUTTON)
            self._release_callback(button)


class PygameKeyboard(sketching.control_struct.Keyboard):
    """Strategy implementation for Pygame-based keyboard access."""

    def __init__(self):
        """Create a new keyboard strategy using Pygame."""
        super().__init__()
        self._pressed = set()
        self._press_callback = None
        self._release_callback = None

    def get_keys_pressed(self) -> sketching.control_struct.Buttons:
        return map(lambda x: sketching.control_struct.Button(x), self._pressed)

    def on_key_press(self, callback: sketching.control_struct.KeyboardCallback):
        self._press_callback = callback

    def on_key_release(self, callback: sketching.control_struct.KeyboardCallback):
        self._release_callback = callback

    def report_key_down(self, event):
        mapped = sketching.sketch2d_keymap.KEY_MAP.get(event.key, None)

        if mapped is None:
            return

        self._pressed.add(mapped)

        if self._press_callback is not None:
            button = sketching.control_struct.Button(mapped)
            self._press_callback(button)

    def report_key_up(self, event):
        mapped = sketching.sketch2d_keymap.KEY_MAP.get(event.key, None)

        if mapped is None:
            return

        self._pressed.remove(mapped)

        if self._release_callback is not None:
            button = sketching.control_struct.Button(mapped)
            self._release_callback(button)
