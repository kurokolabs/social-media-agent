"""LinkedIn Carousel PDF Generator — Feature 3.

Generates a 10-slide 1080×1080px B&W PDF using reportlab.
Slide 1: Title + Hook
Slides 2–9: Key points (one per slide)
Slide 10: CTA

Output path: output/carousels/{slug}.pdf
"""
import os
import re
from pathlib import Path


_SLIDE_SIZE = (1080, 1080)   # points (≈ 15.1 × 15.1 inches at 72 dpi — PDF internal unit)
_OUTPUT_DIR = Path("output/carousels")


def _slugify(text: str) -> str:
    """Convert title to a filesystem-safe slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:60] or "carousel"


class CarouselGenerator:
    """Creates a 10-slide 1080×1080px PDF carousel for LinkedIn."""

    def generate(self, post_content: str, title: str) -> str:
        """Generate PDF and return the file path.

        Args:
            post_content: Full post text used to extract key points.
            title: Post title used for slide 1 and filename.

        Returns:
            Absolute path string to the generated PDF.
        """
        try:
            from reportlab.lib.pagesizes import landscape
            from reportlab.pdfgen import canvas
            from reportlab.lib import colors
        except ImportError as exc:
            raise RuntimeError(
                "reportlab is required for carousel generation. "
                "Install with: pip install reportlab>=4.0"
            ) from exc

        _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        slug = _slugify(title)
        pdf_path = _OUTPUT_DIR / f"{slug}.pdf"

        slides = self._build_slides(post_content, title)

        c = canvas.Canvas(str(pdf_path), pagesize=_SLIDE_SIZE)
        for slide in slides:
            self._draw_slide(c, slide)
            c.showPage()
        c.save()
        return str(pdf_path.resolve())

    # ------------------------------------------------------------------
    # Slide construction
    # ------------------------------------------------------------------

    def _build_slides(self, content: str, title: str) -> list[dict]:
        """Extract up to 8 key points and build slide data."""
        # Split content into lines; pick non-empty, non-hashtag lines as key points
        lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#")]
        # Remove lines that are mostly symbols or very short
        key_points = [l for l in lines if len(l) > 20][:8]

        # Pad with generic CTA points if fewer than 8
        while len(key_points) < 8:
            key_points.append("KI-Automatisierung als Hebel für operative Exzellenz.")

        slides = [
            {"type": "title", "title": title, "subtitle": key_points[0] if key_points else ""},
        ]
        for i, point in enumerate(key_points, start=1):
            slides.append({"type": "content", "number": i, "text": point})

        slides.append({
            "type": "cta",
            "text": "Mehr erfahren? Folgt Kuroko Labs auf LinkedIn.",
            "handle": "kuroko-labs",
        })
        return slides

    def _draw_slide(self, c, slide: dict) -> None:
        """Draw a single slide onto the canvas."""
        from reportlab.lib import colors

        w, h = _SLIDE_SIZE

        # Background: white
        c.setFillColor(colors.white)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Thin black border
        c.setStrokeColor(colors.black)
        c.setLineWidth(4)
        c.rect(20, 20, w - 40, h - 40, fill=0, stroke=1)

        if slide["type"] == "title":
            self._draw_title_slide(c, slide, w, h)
        elif slide["type"] == "content":
            self._draw_content_slide(c, slide, w, h)
        elif slide["type"] == "cta":
            self._draw_cta_slide(c, slide, w, h)

    def _draw_title_slide(self, c, slide: dict, w: int, h: int) -> None:
        from reportlab.lib import colors

        # Logo area — top-left small mark
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(60, h - 80, "KUROKO LABS")

        # Horizontal rule
        c.setLineWidth(2)
        c.line(60, h - 100, w - 60, h - 100)

        # Title
        c.setFont("Helvetica-Bold", 64)
        self._draw_wrapped_text(c, slide["title"], 60, h - 200, w - 120, 64, max_lines=4)

        # Subtitle / hook
        c.setFont("Helvetica", 32)
        self._draw_wrapped_text(c, slide["subtitle"], 60, 200, w - 120, 32, max_lines=3)

        # Bottom rule
        c.line(60, 80, w - 60, 80)
        c.setFont("Helvetica", 20)
        c.drawString(60, 50, "kuroko-labs.com")

    def _draw_content_slide(self, c, slide: dict, w: int, h: int) -> None:
        from reportlab.lib import colors

        # Slide number
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 180)
        c.setFillColorRGB(0.93, 0.93, 0.93)
        c.drawString(60, h - 340, str(slide["number"]))

        # Content text on top
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 40)
        self._draw_wrapped_text(c, slide["text"], 60, h - 180, w - 120, 40, max_lines=6)

        # Bottom logo
        c.setFont("Helvetica-Bold", 20)
        c.drawString(60, 50, "KUROKO LABS")

    def _draw_cta_slide(self, c, slide: dict, w: int, h: int) -> None:
        from reportlab.lib import colors

        c.setFillColor(colors.black)
        # Black background block
        c.rect(40, h // 2 - 80, w - 80, 160, fill=1, stroke=0)

        # CTA text in white
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 36)
        self._draw_wrapped_text(c, slide["text"], 80, h // 2 + 40, w - 160, 36, max_lines=2)

        # Handle below
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 28)
        c.drawString(60, h // 2 - 140, f"@{slide['handle']}")

        # Logo top
        c.setFont("Helvetica-Bold", 24)
        c.drawString(60, h - 80, "KUROKO LABS")

    def _draw_wrapped_text(
        self,
        c,
        text: str,
        x: float,
        y: float,
        max_width: float,
        font_size: float,
        max_lines: int = 4,
    ) -> None:
        """Simple word-wrapping text draw."""
        from reportlab.pdfbase.pdfmetrics import stringWidth

        words = text.split()
        line = ""
        lines_drawn = 0
        line_height = font_size * 1.3

        for word in words:
            test_line = f"{line} {word}".strip()
            if stringWidth(test_line, c._fontname, font_size) <= max_width:
                line = test_line
            else:
                if line:
                    c.drawString(x, y - lines_drawn * line_height, line)
                    lines_drawn += 1
                    if lines_drawn >= max_lines:
                        break
                line = word

        if line and lines_drawn < max_lines:
            c.drawString(x, y - lines_drawn * line_height, line)
