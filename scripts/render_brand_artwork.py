#!/usr/bin/env python3
"""Render FDEBOK social preview cards and the Apple touch icon with Cairo/Pango."""

from __future__ import annotations

import ctypes
import ctypes.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
cairo.cairo_create.argtypes = [ctypes.c_void_p]
cairo.cairo_create.restype = ctypes.c_void_p
cairo.cairo_surface_write_to_png.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
cairo.cairo_surface_write_to_png.restype = ctypes.c_int
cairo.cairo_surface_destroy.argtypes = [ctypes.c_void_p]
cairo.cairo_destroy.argtypes = [ctypes.c_void_p]
cairo.cairo_set_source_rgba.argtypes = [
    ctypes.c_void_p,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
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
cairo.cairo_new_path.argtypes = [ctypes.c_void_p]
cairo.cairo_close_path.argtypes = [ctypes.c_void_p]
cairo.cairo_save.argtypes = [ctypes.c_void_p]
cairo.cairo_restore.argtypes = [ctypes.c_void_p]
cairo.cairo_translate.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
cairo.cairo_scale.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
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


def rounded_card(context: ctypes.c_void_p, x: int, y: int, width: int, height: int) -> None:
    radius = 12
    cairo.cairo_new_path(context)
    cairo.cairo_arc(context, x + width - radius, y + radius, radius, -1.5708, 0)
    cairo.cairo_arc(context, x + width - radius, y + height - radius, radius, 0, 1.5708)
    cairo.cairo_arc(context, x + radius, y + height - radius, radius, 1.5708, 3.1416)
    cairo.cairo_arc(context, x + radius, y + radius, radius, 3.1416, 4.7124)
    cairo.cairo_close_path(context)
    color(context, "#0b1728", 0.6)
    cairo.cairo_fill(context)


def draw_logo_mark(context: ctypes.c_void_p, x: int, y: int, size: int) -> None:
    scale = size / 96
    cairo.cairo_save(context)
    cairo.cairo_translate(context, x, y)
    cairo.cairo_scale(context, scale, scale)
    cairo.cairo_rectangle(context, 3, 3, 90, 90)
    color(context, "#172b45")
    cairo.cairo_fill(context)
    cairo.cairo_set_line_width(context, 1)
    color(context, "#d7e5f3", 0.08)
    for offset in (24, 48, 72):
        cairo.cairo_move_to(context, offset, 18)
        cairo.cairo_line_to(context, offset, 78)
        cairo.cairo_move_to(context, 18, offset)
        cairo.cairo_line_to(context, 78, offset)
    cairo.cairo_stroke(context)
    cairo.cairo_set_line_width(context, 8)
    color(context, "#edc66d")
    cairo.cairo_move_to(context, 33, 70)
    cairo.cairo_line_to(context, 33, 27)
    cairo.cairo_line_to(context, 64, 27)
    cairo.cairo_move_to(context, 33, 46)
    cairo.cairo_line_to(context, 56, 46)
    cairo.cairo_stroke(context)
    cairo.cairo_set_line_width(context, 5)
    color(context, "#6fc5aa")
    cairo.cairo_move_to(context, 56, 46)
    cairo.cairo_line_to(context, 66, 46)
    cairo.cairo_arc(context, 66, 57, 11, -1.5708, 0)
    cairo.cairo_line_to(context, 77, 61)
    cairo.cairo_stroke(context)
    cairo.cairo_arc(context, 77, 67, 6, 0, 6.2832)
    cairo.cairo_fill(context)
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

    cairo.cairo_set_line_width(context, 1)
    color(context, "#d7e5f3", 0.07)
    for x in range(32, WIDTH, 48):
        cairo.cairo_move_to(context, x, 0)
        cairo.cairo_line_to(context, x, HEIGHT)
    for y in range(30, HEIGHT, 48):
        cairo.cairo_move_to(context, 0, y)
        cairo.cairo_line_to(context, WIDTH, y)
    cairo.cairo_stroke(context)

    draw_logo_mark(context, 80, 60, 74)
    text(context, "FDEBOK", 177, 68, 34, "#f3f6fb", bold=True)
    text(context, "FIELD DELIVERY  ·  KNOWLEDGE", 180, 111, 12, "#bdcbdc", bold=True)
    cairo.cairo_set_line_width(context, 2)
    color(context, "#d8b15d")
    cairo.cairo_move_to(context, 82, 166)
    cairo.cairo_line_to(context, 1118, 166)
    cairo.cairo_stroke(context)

    if english:
        text(context, "From AI capability to", 88, 206, 43, "#f4f6fa", bold=True)
        text(context, "measurable delivery.", 88, 260, 43, "#edc66d", bold=True)
        text(context, "A field guide for Forward Deployed Engineers", 91, 331, 20, "#d1dce9")
        labels = (("22", "CHAPTERS"), ("10", "DOMAINS"), ("6", "DELIVERY STAGES"), ("9", "FIELD TEMPLATES"))
        footer = "A practical, open handbook for enterprise AI delivery."
    else:
        text(context, "让企业 AI 从场景", 88, 206, 43, "#f4f6fa", bold=True)
        text(context, "走向稳定交付", 88, 260, 43, "#edc66d", bold=True)
        text(context, "前线部署工程师知识体系手册 · 面向真实业务与生产现场", 91, 331, 20, "#d1dce9")
        labels = (("22", "章  CHAPTERS"), ("10", "大知识域"), ("6", "交付阶段"), ("9", "现场模板"))
        footer = "FDEBOK · 开放、双语、可复用的企业 AI 交付实践指南"

    card_width = 244
    for index, (number, label) in enumerate(labels):
        x = 89 + index * 258
        rounded_card(context, x, 397, card_width, 98)
        text(context, number, x + 17, 410, 27, "#edc66d", bold=True)
        text(context, label, x + 18, 455, 13, "#d9e2ec", bold=True)

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
    draw_logo_mark(context, 23, 23, 134)
    cairo.cairo_surface_write_to_png(surface, str(path).encode("utf-8"))
    cairo.cairo_destroy(context)
    cairo.cairo_surface_destroy(surface)


def main() -> None:
    draw_card(ROOT / "share-card-zh.png", english=False)
    draw_card(ROOT / "share-card-en.png", english=True)
    draw_touch_icon(ROOT / "apple-touch-icon.png")
    print("Rendered zh/en 1200x630 social cards and the 180x180 Apple touch icon.")


if __name__ == "__main__":
    main()
