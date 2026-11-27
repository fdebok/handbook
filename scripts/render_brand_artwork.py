#!/usr/bin/env python3
"""Render FDEBOK social preview cards and the Apple touch icon with Cairo/Pango."""

from __future__ import annotations

import ctypes
import ctypes.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_ASSETS_DIR = ROOT / "src" / "site" / "assets"
WIDTH = 1200
HEIGHT = 630
PANGO_SCALE = 1024


def load_library(name: str) -> ctypes.CDLL:
    path = ctypes.util.find_library(name)
    if path is None:
        raise RuntimeError(f"Required native library {name!r} is unavailable")
    return ctypes.CDLL(path)


cairo = load_library("cairo")
pango_cairo = load_library("pangocairo-1.0")
pango = load_library("pango-1.0")
gobject = load_library("gobject-2.0")

cairo.cairo_image_surface_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
cairo.cairo_image_surface_create.restype = ctypes.c_void_p
cairo.cairo_image_surface_create_from_png.argtypes = [ctypes.c_char_p]
cairo.cairo_image_surface_create_from_png.restype = ctypes.c_void_p
cairo.cairo_surface_status.argtypes = [ctypes.c_void_p]
cairo.cairo_surface_status.restype = ctypes.c_int
cairo.cairo_status_to_string.argtypes = [ctypes.c_int]
cairo.cairo_status_to_string.restype = ctypes.c_char_p
cairo.cairo_create.argtypes = [ctypes.c_void_p]
cairo.cairo_create.restype = ctypes.c_void_p
cairo.cairo_surface_write_to_png.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
cairo.cairo_surface_write_to_png.restype = ctypes.c_int
cairo.cairo_set_source_surface.argtypes = [
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_double,
    ctypes.c_double,
]
cairo.cairo_surface_destroy.argtypes = [ctypes.c_void_p]
cairo.cairo_destroy.argtypes = [ctypes.c_void_p]
cairo.cairo_set_source_rgba.argtypes = [
    ctypes.c_void_p,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
cairo.cairo_fill_preserve.argtypes = [ctypes.c_void_p]
cairo.cairo_fill_preserve.restype = None
cairo.cairo_stroke_preserve.argtypes = [ctypes.c_void_p]
cairo.cairo_stroke_preserve.restype = None
cairo.cairo_paint.argtypes = [ctypes.c_void_p]
cairo.cairo_rectangle.argtypes = [
    ctypes.c_void_p,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
cairo.cairo_fill.argtypes = [ctypes.c_void_p]
cairo.cairo_stroke.argtypes = [ctypes.c_void_p]
cairo.cairo_set_line_width.argtypes = [ctypes.c_void_p, ctypes.c_double]
cairo.cairo_move_to.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
cairo.cairo_line_to.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
cairo.cairo_curve_to.argtypes = [
    ctypes.c_void_p,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
cairo.cairo_new_path.argtypes = [ctypes.c_void_p]
cairo.cairo_close_path.argtypes = [ctypes.c_void_p]
cairo.cairo_clip.argtypes = [ctypes.c_void_p]
cairo.cairo_save.argtypes = [ctypes.c_void_p]
cairo.cairo_restore.argtypes = [ctypes.c_void_p]
cairo.cairo_translate.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
cairo.cairo_scale.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
cairo.cairo_set_line_cap.argtypes = [ctypes.c_void_p, ctypes.c_int]
cairo.cairo_set_line_join.argtypes = [ctypes.c_void_p, ctypes.c_int]
cairo.cairo_set_dash.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int,
    ctypes.c_double,
]
cairo.cairo_arc.argtypes = [
    ctypes.c_void_p,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
cairo.cairo_pattern_create_linear.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
cairo.cairo_pattern_create_linear.restype = ctypes.c_void_p
cairo.cairo_pattern_add_color_stop_rgba.argtypes = [
    ctypes.c_void_p,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
cairo.cairo_set_source.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
cairo.cairo_pattern_destroy.argtypes = [ctypes.c_void_p]

pango_cairo.pango_cairo_create_layout.argtypes = [ctypes.c_void_p]
pango_cairo.pango_cairo_create_layout.restype = ctypes.c_void_p
pango_cairo.pango_cairo_show_layout.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
pango.pango_font_description_new.restype = ctypes.c_void_p
pango.pango_font_description_set_family.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
pango.pango_font_description_set_weight.argtypes = [ctypes.c_void_p, ctypes.c_int]
pango.pango_font_description_set_absolute_size.argtypes = [ctypes.c_void_p, ctypes.c_double]
pango.pango_layout_set_font_description.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
pango.pango_layout_set_text.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
pango.pango_layout_set_width.argtypes = [ctypes.c_void_p, ctypes.c_int]
pango.pango_layout_set_wrap.argtypes = [ctypes.c_void_p, ctypes.c_int]
pango.pango_layout_get_pixel_size.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
]
pango.pango_font_description_free.argtypes = [ctypes.c_void_p]
gobject.g_object_unref.argtypes = [ctypes.c_void_p]


def color(context: ctypes.c_void_p, value: str, alpha: float = 1.0) -> None:
    red = int(value[1:3], 16) / 255
    green = int(value[3:5], 16) / 255
    blue = int(value[5:7], 16) / 255
    cairo.cairo_set_source_rgba(context, red, green, blue, alpha)


def text(
    context: ctypes.c_void_p,
    value: str,
    x: float,
    y: float,
    size: float,
    fill: str,
    *,
    bold: bool = False,
    max_width: int = 0,
) -> None:
    layout = pango_cairo.pango_cairo_create_layout(context)
    description = pango.pango_font_description_new()
    pango.pango_font_description_set_family(description, b"DejaVu Sans")
    pango.pango_font_description_set_weight(description, 700 if bold else 400)
    pango.pango_font_description_set_absolute_size(description, size * PANGO_SCALE)
    pango.pango_layout_set_font_description(layout, description)
    encoded = value.encode("utf-8")
    pango.pango_layout_set_text(layout, encoded, len(encoded))
    if max_width:
        pango.pango_layout_set_width(layout, max_width * PANGO_SCALE)
        pango.pango_layout_set_wrap(layout, 2)
    color(context, fill)
    cairo.cairo_move_to(context, x, y)
    pango_cairo.pango_cairo_show_layout(context, layout)
    pango.pango_font_description_free(description)
    gobject.g_object_unref(layout)


def circle(
    context: ctypes.c_void_p,
    cx: float,
    cy: float,
    radius: float,
    fill: str,
    alpha: float = 1.0,
) -> None:
    cairo.cairo_new_path(context)
    cairo.cairo_arc(context, cx, cy, radius, 0, 6.283185307179586)
    color(context, fill, alpha)
    cairo.cairo_fill(context)


def gradient_circle(
    context: ctypes.c_void_p,
    cx: float,
    cy: float,
    radius: float,
    top: str,
    bottom: str,
    stroke: str | None = None,
    width: float = 1.0,
) -> None:
    cairo.cairo_new_path(context)
    cairo.cairo_arc(context, cx, cy, radius, 0, 6.283185307179586)
    gradient = cairo.cairo_pattern_create_linear(cx, cy - radius, cx, cy + radius)
    for offset, value in ((0, top), (1, bottom)):
        red, green, blue = (
            int(value[index : index + 2], 16) / 255 for index in (1, 3, 5)
        )
        cairo.cairo_pattern_add_color_stop_rgba(
            gradient, offset, red, green, blue, 1
        )
    cairo.cairo_set_source(context, gradient)
    if stroke:
        cairo.cairo_fill_preserve(context)
        cairo.cairo_set_line_width(context, width)
        color(context, stroke)
        cairo.cairo_stroke(context)
    else:
        cairo.cairo_fill(context)
    cairo.cairo_pattern_destroy(gradient)


def draw_logo_mark(context: ctypes.c_void_p, x: int, y: int, size: int) -> None:
    scale = size / 100
    cairo.cairo_save(context)
    cairo.cairo_translate(context, x, y)
    cairo.cairo_scale(context, scale, scale)

    circle(context, 51, 52, 48, "#705522", 0.16)
    gradient_circle(context, 50, 50, 48, "#f6e7b5", "#b98a35", "#c59b55", 1.3)
    gradient_circle(context, 50, 50, 45.7, "#fff3c9", "#d7bd75", "#f7e7b5", 0.7)
    gradient_circle(context, 50, 50, 43.2, "#ffffff", "#eaf1ec", "#cbd8cf", 0.65)

    cairo.cairo_save(context)
    cairo.cairo_new_path(context)
    cairo.cairo_arc(context, 50, 50, 42.6, 0, 6.283185307179586)
    cairo.cairo_clip(context)
    cairo.cairo_set_line_width(context, 0.8)
    color(context, "#79bda8", 0.16)
    for scale_x in (0.34, 0.68):
        cairo.cairo_save(context)
        cairo.cairo_translate(context, 50, 50)
        cairo.cairo_scale(context, scale_x, 1)
        cairo.cairo_new_path(context)
        cairo.cairo_arc(context, 0, 0, 41.5, 0, 6.283185307179586)
        cairo.cairo_restore(context)
        cairo.cairo_stroke(context)
    for scale_y in (0.38, 0.7):
        cairo.cairo_save(context)
        cairo.cairo_translate(context, 50, 50)
        cairo.cairo_scale(context, 1, scale_y)
        cairo.cairo_new_path(context)
        cairo.cairo_arc(context, 0, 0, 41.5, 0, 6.283185307179586)
        cairo.cairo_restore(context)
        cairo.cairo_stroke(context)
    cairo.cairo_new_path(context)
    cairo.cairo_move_to(context, 8.5, 50)
    cairo.cairo_line_to(context, 91.5, 50)
    cairo.cairo_stroke(context)
    cairo.cairo_restore(context)

    cairo.cairo_save(context)
    cairo.cairo_new_path(context)
    cairo.cairo_arc(context, 50, 50, 42.6, 0, 6.283185307179586)
    cairo.cairo_clip(context)

    letters = (
        (
            ((19, 30), (19, 50), (19, 70), (35, 30), (32, 50)),
            ((0, 1), (1, 2), (0, 3), (1, 4)),
        ),
        (
            ((43, 30), (43, 50), (43, 70), (51, 30), (60, 50), (51, 70)),
            ((0, 1), (1, 2), (0, 3), (3, 4), (4, 5), (5, 2)),
        ),
        (
            ((68, 30), (68, 50), (68, 70), (82, 30), (78, 50), (82, 70)),
            ((0, 1), (1, 2), (0, 3), (1, 4), (2, 5)),
        ),
    )
    letter_colors = ("#624719", "#806025", "#9a742c")
    dash_pattern = (ctypes.c_double * 2)(3, 1.8)
    cairo.cairo_set_line_cap(context, 1)
    cairo.cairo_set_line_join(context, 1)
    for letter_index, (nodes, links) in enumerate(letters):
        for link_index, (start, end) in enumerate(links):
            cairo.cairo_new_path(context)
            cairo.cairo_set_dash(context, dash_pattern, 2, 0)
            cairo.cairo_move_to(context, *nodes[start])
            if letter_index == 1 and (start, end) == (3, 4):
                cairo.cairo_curve_to(context, 57, 30, 60, 39, *nodes[end])
            elif letter_index == 1 and (start, end) == (4, 5):
                cairo.cairo_curve_to(context, 60, 61, 57, 70, *nodes[end])
            else:
                cairo.cairo_line_to(context, *nodes[end])
            cairo.cairo_set_line_width(context, 2.8)
            color(context, letter_colors[letter_index])
            cairo.cairo_stroke(context)
            cairo.cairo_set_dash(context, None, 0, 0)

    for letter_index, (nodes, _) in enumerate(letters):
        for node_index, (node_x, node_y) in enumerate(nodes):
            node_color = "#79bda8" if letter_index == 0 and node_index == 0 else letter_colors[letter_index]
            radius = 2.5 if (letter_index, node_index) in ((0, 1), (1, 4)) else 2.2
            circle(context, node_x + 0.5, node_y + 0.7, radius + 0.65, "#60461d", 0.14)
            circle(context, node_x, node_y, radius, "#fffdf3")
            cairo.cairo_new_path(context)
            cairo.cairo_arc(context, node_x, node_y, radius, 0, 6.283185307179586)
            cairo.cairo_set_line_width(context, 1)
            color(context, letter_colors[letter_index])
            cairo.cairo_stroke(context)
            circle(context, node_x, node_y, 0.8, node_color)
    cairo.cairo_restore(context)
    cairo.cairo_restore(context)


def draw_card(path: Path, english: bool) -> None:
    surface = cairo.cairo_image_surface_create(0, WIDTH, HEIGHT)
    context = cairo.cairo_create(surface)
    gradient = cairo.cairo_pattern_create_linear(0, 0, WIDTH, HEIGHT)
    cairo.cairo_pattern_add_color_stop_rgba(gradient, 0, 0.055, 0.102, 0.173, 1)
    cairo.cairo_pattern_add_color_stop_rgba(gradient, 1, 0.122, 0.247, 0.369, 1)
    cairo.cairo_set_source(context, gradient)
    cairo.cairo_paint(context)
    cairo.cairo_pattern_destroy(gradient)

    draw_logo_mark(context, 80, 60, 74)
    text(context, "FDE", 177, 68, 34, "#f3f6fb", bold=True)
    text(context, "BOK", 264, 68, 34, "#d8b46c", bold=True)
    text(context, "FIELD INSIGHT  ·  AI DELIVERY  ·  REAL IMPACT", 180, 111, 12, "#bdcbdc", bold=True)
    cairo.cairo_set_line_width(context, 1)
    color(context, "#d8b15d", 0.35)
    cairo.cairo_move_to(context, 82, 166)
    cairo.cairo_line_to(context, 1118, 166)
    cairo.cairo_stroke(context)

    cairo.cairo_set_line_width(context, 1)
    color(context, "#d8e2ed", 0.22)
    cairo.cairo_move_to(context, 82, 407)
    cairo.cairo_line_to(context, 1118, 407)
    cairo.cairo_stroke(context)
    draw_logo_mark(context, 885, 187, 190)

    if english:
        text(context, "From AI capability to", 88, 206, 43, "#f4f6fa", bold=True)
        text(context, "measurable delivery.", 88, 260, 43, "#edc66d", bold=True)
        text(context, "A field guide for Forward Deployed Engineers", 91, 331, 20, "#d1dce9")
        labels = (("22", "CHAPTERS"), ("10", "DOMAINS"), ("6", "DELIVERY STAGES"), ("9", "FIELD TEMPLATES"))
        footer = "A practical, open handbook for enterprise AI delivery."
    else:
        text(context, "让企业 AI 从场景", 88, 206, 43, "#f4f6fa", bold=True)
        text(context, "走向稳定交付", 88, 260, 43, "#edc66d", bold=True)
        text(context, "FDE GUIDE  ·  ENTERPRISE AI DELIVERY", 91, 331, 20, "#d1dce9")
        labels = (("22", "章节"), ("10", "知识域"), ("6", "交付阶段"), ("9", "现场模板"))
        footer = "FDEBOK · 开放、双语、可复用的企业 AI 交付实践指南"

    column_width = 258
    for index, (number, label) in enumerate(labels):
        x = 89 + index * column_width
        text(context, number, x, 423, 27, "#edc66d", bold=True)
        text(context, label, x + 2, 463, 13, "#d9e2ec", bold=True)
        if index < len(labels) - 1:
            cairo.cairo_set_line_width(context, 1)
            color(context, "#d8e2ed", 0.16)
            cairo.cairo_move_to(context, x + column_width - 20, 426)
            cairo.cairo_line_to(context, x + column_width - 20, 478)
            cairo.cairo_stroke(context)

    text(context, footer, 91, 548, 14, "#bdcbdc", bold=True)
    text(context, "www.fdebok.com", 91, 580, 13, "#f2cb72", bold=True)
    cairo.cairo_surface_write_to_png(surface, str(path).encode("utf-8"))
    cairo.cairo_destroy(context)
    cairo.cairo_surface_destroy(surface)


def draw_touch_icon(path: Path) -> None:
    surface = cairo.cairo_image_surface_create(0, 180, 180)
    context = cairo.cairo_create(surface)
    gradient = cairo.cairo_pattern_create_linear(0, 0, 180, 180)
    cairo.cairo_pattern_add_color_stop_rgba(gradient, 0, 0.12, 0.23, 0.36, 1)
    cairo.cairo_pattern_add_color_stop_rgba(gradient, 1, 0.055, 0.10, 0.17, 1)
    cairo.cairo_set_source(context, gradient)
    cairo.cairo_paint(context)
    cairo.cairo_pattern_destroy(gradient)
    draw_logo_mark(context, 18, 18, 144)
    cairo.cairo_surface_write_to_png(surface, str(path).encode("utf-8"))
    cairo.cairo_destroy(context)
    cairo.cairo_surface_destroy(surface)


def draw_chinese_card(path: Path) -> None:
    source_path = ROOT / "share-card-zh-v3.png"
    surface = cairo.cairo_image_surface_create_from_png(str(source_path).encode("utf-8"))
    if not surface:
        raise RuntimeError(f"Unable to load the Chinese artwork source: {source_path}")
    context = cairo.cairo_create(surface)

    gradient = cairo.cairo_pattern_create_linear(0, 0, WIDTH, HEIGHT)
    cairo.cairo_pattern_add_color_stop_rgba(gradient, 0, 0.055, 0.102, 0.173, 1)
    cairo.cairo_pattern_add_color_stop_rgba(gradient, 1, 0.122, 0.247, 0.369, 1)
    for x, y, width, height in (
        (80, 60, 74, 74),
        (885, 187, 190, 190),
        (80, 315, 760, 36),
    ):
        cairo.cairo_set_source(context, gradient)
        cairo.cairo_rectangle(context, x, y, width, height)
        cairo.cairo_fill(context)
    cairo.cairo_pattern_destroy(gradient)

    draw_logo_mark(context, 80, 60, 74)
    draw_logo_mark(context, 885, 187, 190)
    text(context, "FDE GUIDE  ·  ENTERPRISE AI DELIVERY", 91, 331, 20, "#d1dce9")
    cairo.cairo_surface_write_to_png(surface, str(path).encode("utf-8"))
    cairo.cairo_destroy(context)
    cairo.cairo_surface_destroy(surface)


def draw_badge_crops() -> None:
    source_path = ROOT / "assets" / "fdebok-badges-approved-v28-source.png"
    source = cairo.cairo_image_surface_create_from_png(str(source_path).encode("utf-8"))
    if not source:
        raise RuntimeError(f"Unable to load the approved badge artwork: {source_path}")
    status = cairo.cairo_surface_status(source)
    if status:
        message = cairo.cairo_status_to_string(status).decode("utf-8")
        cairo.cairo_surface_destroy(source)
        raise RuntimeError(f"Unable to load badge artwork {source_path}: {message}")

    for filename, left in (
        ("badge-a.png", 230),
        ("badge-p.png", 700),
        ("badge-m.png", 1170),
    ):
        surface = cairo.cairo_image_surface_create(0, 320, 390)
        context = cairo.cairo_create(surface)
        color(context, "#f4f5f2")
        cairo.cairo_paint(context)
        cairo.cairo_set_source_surface(context, source, -left, -455)
        cairo.cairo_paint(context)
        status = cairo.cairo_surface_write_to_png(
            surface, str(SITE_ASSETS_DIR / filename).encode("utf-8")
        )
        cairo.cairo_destroy(context)
        cairo.cairo_surface_destroy(surface)
        if status:
            message = cairo.cairo_status_to_string(status).decode("utf-8")
            cairo.cairo_surface_destroy(source)
            raise RuntimeError(f"Unable to write {filename}: {message}")
    cairo.cairo_surface_destroy(source)


def main() -> None:
    SITE_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    draw_chinese_card(SITE_ASSETS_DIR / "share-card-zh-v6.png")
    draw_card(SITE_ASSETS_DIR / "share-card-en-v6.png", english=True)
    draw_chinese_card(SITE_ASSETS_DIR / "og-image.png")
    draw_card(SITE_ASSETS_DIR / "og-image-en.png", english=True)
    draw_touch_icon(SITE_ASSETS_DIR / "apple-touch-icon.png")
    draw_badge_crops()
    print("Rendered v6 brand artwork, A/P/M badge assets, and the 180x180 Apple touch icon.")


if __name__ == "__main__":
    main()
