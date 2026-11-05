#!/usr/bin/env python3
"""Generate the Fink ecosystem badges.

This script is the single source of truth for the badges. It writes:

* ``endpoints/<key>.json``: one shields.io endpoint file per badge
  (https://shields.io/badges/endpoint-badge). A README displays a badge with
  ``https://img.shields.io/endpoint?url=<raw URL of the JSON file>``, so the
  URL stays short and every README picks up changes made here.
* ``README.md``: the gallery with copy-paste snippets.

Colors come from the official Fink palette
(https://fink-broker.org/visual-identity/branding/). The Fink badge embeds the
official secondary logo (``assets/fink_secondary_logo_48x64.png``). The other
icons are drawn below as small SVGs.

Usage (standard library only)::

    python generate_badges.py
"""

from __future__ import annotations

import base64
import json
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

BADGES_DIR = Path(__file__).resolve().parent
ENDPOINTS_DIR = BADGES_DIR / "endpoints"
FINK_LOGO_PNG = BADGES_DIR / "assets" / "fink_secondary_logo_48x64.png"

RAW_BASE_URL = "https://raw.githubusercontent.com/astrolabsoftware/fink-badges/main/endpoints"
SHIELDS_ENDPOINT_URL = "https://img.shields.io/endpoint?url="
SHIELDS_STATIC_URL = "https://img.shields.io/badge/"

# Official Fink palette.
NAVY = "#15284F"
BLUE = "#3C8DFF"
ORANGE = "#F5622E"
GREY = "#D5D5D3"
WHITE = "#FFFFFF"


@dataclass(frozen=True)
class Badge:
    """One badge of the Fink ecosystem.

    Attributes:
        key: File stem of the endpoint JSON and reference name in Markdown.
        label: Left-hand text.
        message: Right-hand text.
        label_color: Left-hand background (hex, palette color).
        color: Right-hand background (hex, palette color).
        logo_svg: Icon drawn on the left, as a complete SVG document.
        link: Target of the badge link.
        description: One-line description shown in the gallery.
    """

    key: str
    label: str
    message: str
    label_color: str
    color: str
    logo_svg: str
    link: str
    description: str


def svg_icon(body: str, view_box: str = "0 0 24 24") -> str:
    """Wrap SVG drawing elements into a standalone SVG document."""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}">{body}</svg>'


def png_as_svg(png_path: Path, width: int, height: int) -> str:
    """Embed a PNG into an SVG document.

    The shields.io endpoint schema only accepts SVG logos (``logoSvg``), so a
    raster logo must be wrapped.
    """
    data = base64.b64encode(png_path.read_bytes()).decode()
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {width} {height}">'
        f'<image width="{width}" height="{height}" xlink:href="data:image/png;base64,{data}"/>'
        "</svg>"
    )


def build_badges() -> list[Badge]:
    """Return the badge definitions, in display order."""
    return [
        Badge(
            key="fink",
            label="Fink",
            message="astronomy broker",
            label_color=WHITE,
            color=ORANGE,
            logo_svg=png_as_svg(FINK_LOGO_PNG, 48, 64),
            link="https://fink-broker.org",
            description="The Fink broker, with its official secondary logo.",
        ),
        Badge(
            key="fink-broker",
            label="fink-broker",
            message="alert processing",
            label_color=ORANGE,
            color=NAVY,
            # One stream in, three streams out.
            logo_svg=svg_icon(
                f'<circle cx="7" cy="12" r="3" fill="{WHITE}"/>'
                f'<path d="M1 12h3M10 12h4M10 10.5 L14 5h8M10 13.5 L14 19h8M14 12h8" '
                f'stroke="{WHITE}" stroke-width="2" fill="none" stroke-linecap="round"/>'
                f'<circle cx="21" cy="5" r="1.8" fill="{NAVY}"/>'
                f'<circle cx="21" cy="12" r="1.8" fill="{NAVY}"/>'
                f'<circle cx="21" cy="19" r="1.8" fill="{NAVY}"/>'
            ),
            link="https://github.com/astrolabsoftware/fink-broker",
            description="Core broker: ingests and processes the alert streams.",
        ),
        Badge(
            key="fink-client",
            label="fink-client",
            message="alert client",
            label_color=NAVY,
            color=BLUE,
            # Dish antenna receiving alerts.
            logo_svg=svg_icon(
                f'<path d="M4 6 a10 10 0 0 0 14 14 z" fill="{WHITE}"/>'
                f'<path d="M11 13 L17 7" stroke="{WHITE}" stroke-width="2" stroke-linecap="round"/>'
                f'<circle cx="18" cy="6" r="2" fill="{BLUE}"/>'
                f'<path d="M8 20h8" stroke="{WHITE}" stroke-width="2" stroke-linecap="round"/>'
            ),
            link="https://github.com/astrolabsoftware/fink-client",
            description="Client to receive and explore Fink alerts.",
        ),
        Badge(
            key="fink-science",
            label="fink-science",
            message="science modules",
            label_color=BLUE,
            color=NAVY,
            # Flask.
            logo_svg=svg_icon(
                f'<path d="M9 2h6M10 2v7L4 20a1.5 1.5 0 0 0 1.3 2h13.4A1.5 1.5 0 0 0 20 20L14 9V2" '
                f'fill="none" stroke="{WHITE}" stroke-width="2" stroke-linejoin="round"/>'
                f'<path d="M7 15h10l2.6 5H4.4z" fill="{WHITE}"/>'
                f'<circle cx="11" cy="11.5" r="1" fill="{WHITE}"/>'
            ),
            link="https://github.com/astrolabsoftware/fink-science",
            description="Science modules that add value to the alerts (classification, cross-matches).",
        ),
        Badge(
            key="fink-filters",
            label="fink-filters",
            message="alert filters",
            label_color=GREY,
            color=NAVY,
            # Funnel letting one orange alert through.
            logo_svg=svg_icon(
                f'<path d="M2 3h20l-8 9v7l-4 3v-10z" fill="{NAVY}"/>'
                f'<circle cx="12" cy="7" r="2" fill="{ORANGE}"/>'
            ),
            link="https://github.com/astrolabsoftware/fink-filters",
            description="Filters that select the alerts sent to each topic.",
        ),
        Badge(
            key="fink-fat",
            label="fink-fat",
            message="asteroid tracker",
            label_color=ORANGE,
            color=BLUE,
            # Elliptical orbit, Sun and an orange asteroid.
            logo_svg=svg_icon(
                f'<ellipse cx="12" cy="12" rx="11" ry="6" transform="rotate(-20 12 12)" '
                f'fill="none" stroke="{WHITE}" stroke-width="1.6"/>'
                f'<circle cx="12" cy="12" r="2.6" fill="{WHITE}"/>'
                f'<circle cx="20.3" cy="7.6" r="2.4" fill="{ORANGE}" stroke="{WHITE}" stroke-width="1"/>'
            ),
            link="https://github.com/FusRoman/fink-fat",
            description="Fink Asteroid Tracker: finds new Solar System objects.",
        ),
    ]


def endpoint_payload(badge: Badge) -> dict:
    """shields.io endpoint JSON for one badge."""
    return {
        "schemaVersion": 1,
        "label": badge.label,
        "message": badge.message,
        "labelColor": badge.label_color,
        "color": badge.color,
        "logoSvg": badge.logo_svg,
        "style": "flat",
        "cacheSeconds": 86400,
    }


def endpoint_image_url(badge: Badge) -> str:
    """Short image URL that renders the badge from its endpoint JSON."""
    return SHIELDS_ENDPOINT_URL + urllib.parse.quote(f"{RAW_BASE_URL}/{badge.key}.json", safe="")


def static_image_url(badge: Badge) -> str:
    """Self-contained image URL that does not depend on this repository."""

    def escape(text: str) -> str:
        return urllib.parse.quote(text.replace("-", "--").replace("_", "__"), safe="")

    logo = "data:image/svg+xml;base64," + base64.b64encode(badge.logo_svg.encode()).decode()
    query = urllib.parse.urlencode(
        {"style": "flat", "labelColor": badge.label_color.lstrip("#"), "logo": logo}
    )
    return f"{SHIELDS_STATIC_URL}{escape(badge.label)}-{escape(badge.message)}-{badge.color.lstrip('#')}?{query}"


def markdown_snippet(badge: Badge) -> str:
    """Markdown that displays the badge and links to its project."""
    return f"[![{badge.label}]({endpoint_image_url(badge)})]({badge.link})"


def render_gallery(badges: list[Badge]) -> str:
    """Content of ``badges/README.md``."""
    all_snippets = "\n".join(markdown_snippet(b) for b in badges)
    sections = []
    for b in badges:
        sections.append(
            f"### {b.label}\n\n"
            f"{markdown_snippet(b)}\n\n"
            f"{b.description}\n\n"
            f"```markdown\n{markdown_snippet(b)}\n```\n\n"
            "<details><summary>Self-contained URL (no dependency on this repository)</summary>\n\n"
            f"```markdown\n[![{b.label}]({static_image_url(b)})]({b.link})\n```\n\n"
            "</details>\n"
        )
    return (
        "<!-- Generated by generate_badges.py. Do not edit by hand. -->\n"
        "# Fink ecosystem badges\n\n"
        "Badges for the projects of the [Fink](https://fink-broker.org) ecosystem, in the\n"
        "[official Fink colors](https://fink-broker.org/visual-identity/branding/).\n"
        "Anyone can use them in their own README: copy a snippet below.\n\n"
        "| Color | Hex |\n| --- | --- |\n"
        f"| Navy | `{NAVY}` |\n| Blue | `{BLUE}` |\n| Orange | `{ORANGE}` |\n| Grey | `{GREY}` |\n\n"
        "## All badges\n\n"
        f"{all_snippets}\n\n"
        f"```markdown\n{all_snippets}\n```\n\n"
        "## One by one\n\n"
        + "\n".join(sections)
        + "\n## How it works\n\n"
        "Each badge is a [shields.io endpoint badge](https://shields.io/badges/endpoint-badge):\n"
        "shields.io reads its text, colors and icon from a JSON file in\n"
        "[`endpoints/`](endpoints/). Changes to these files reach every README that uses\n"
        "the badge (shields.io caches them for up to a day).\n\n"
        "If you would rather not depend on this repository, use the self-contained URL\n"
        "of each badge: everything, icon included, is encoded in the URL.\n\n"
        "To change a badge, edit `generate_badges.py` and run it (Python 3, standard\n"
        "library only):\n\n"
        "```sh\npython generate_badges.py\n```\n\n"
        "## Logo license\n\n"
        "The Fink badge embeds the official Fink secondary logo (by Justin Burks). The Fink\n"
        "project grants a non-exclusive license to use its logos for non-commercial\n"
        "purposes; such use does not imply endorsement by, partnership with, or official\n"
        "representation of the Fink project. See the\n"
        "[visual identity page](https://fink-broker.org/visual-identity/branding/).\n"
    )


def main() -> None:
    """Write the endpoint files and the gallery."""
    badges = build_badges()
    ENDPOINTS_DIR.mkdir(exist_ok=True)
    for badge in badges:
        path = ENDPOINTS_DIR / f"{badge.key}.json"
        path.write_text(json.dumps(endpoint_payload(badge), indent=2) + "\n")
    (BADGES_DIR / "README.md").write_text(render_gallery(badges))
    print(f"Wrote {len(badges)} endpoint files and README.md in {BADGES_DIR}")


if __name__ == "__main__":
    main()
