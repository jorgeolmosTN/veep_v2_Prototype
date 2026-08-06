from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FRAME_DIR = ROOT / "frames"
OUT_DIR = ROOT / "videos"
OUT_DIR.mkdir(exist_ok=True)

WIDTH, HEIGHT = 960, 600
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def font(size, bold=False):
    return ImageFont.truetype(BOLD_PATH if bold else FONT_PATH, size)

def scene(name, caption=None):
    im = Image.open(FRAME_DIR / f"{name}.png").convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    if caption:
        draw = ImageDraw.Draw(im, "RGBA")
        draw.rounded_rectangle((32, HEIGHT - 70, WIDTH - 32, HEIGHT - 20), radius=10, fill=(4, 39, 77, 232))
        draw.text((52, HEIGHT - 56), caption, font=font(22, True), fill=(255, 255, 255, 255))
    return im

def title_card(title, subtitle):
    im = Image.new("RGB", (WIDTH, HEIGHT), (4, 39, 77))
    draw = ImageDraw.Draw(im)
    draw.text((58, 210), title, font=font(40, True), fill=(255, 255, 255))
    draw.text((60, 275), subtitle, font=font(23), fill=(190, 220, 242))
    draw.rounded_rectangle((60, 345, 250, 351), radius=3, fill=(30, 152, 91))
    draw.text((60, 385), "AltaOne concept", font=font(18), fill=(255, 255, 255))
    return im

def build(name, title, subtitle, steps, title_ms=2000):
    images = [title_card(title, subtitle)]
    durations = [title_ms]
    previous = images[0]
    for frame_name, caption, hold_ms in steps:
        current = scene(frame_name, caption)
        for mix in (0.25, 0.5, 0.75):
            images.append(Image.blend(previous, current, mix))
            durations.append(90)
        images.append(current)
        durations.append(hold_ms)
        previous = current
    palette = [im.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for im in images]
    output = OUT_DIR / f"{name}.gif"
    palette[0].save(output, save_all=True, append_images=palette[1:], duration=durations, loop=0, optimize=True, disposal=2)
    return output

packages = [
    (
        "01-anytimepay-overview",
        "AnyTimePay in Q2",
        "Native account experience — executive walkthrough",
        [
            ("home-first", "AnyTimePay appears alongside the member's other accounts", 4500),
            ("welcome", "First use begins with a clear invitation to access eligible earnings", 4500),
            ("progress-1", "Step 1 of 4 — updating account activity", 2500),
            ("progress-2", "Step 2 of 4 — confirming earnings information", 2500),
            ("progress-3", "Step 3 of 4 — calculating available earnings", 2500),
            ("progress-4", "Step 4 of 4 — preparing the AnyTimePay account", 2800),
            ("details", "The native account view brings availability, repayment and outlook together", 6500),
            ("transfer", "Members use Q2's native transfer experience", 5000),
            ("review", "The $4.99 fee, total repayment and T&Cs are reviewed before every transfer", 6000),
            ("success", "Submission returns directly to Transactions with a brief success message", 5000),
            ("transactions", "The transfer posts immediately; the $4.99 fee waits until repayment", 5000),
            ("home-post-transfer", "Checking increases by $60 while available earnings decrease by $60", 4000),
            ("nudge-after", "Explore Nudge opens broader Financial Wellness from AnyTimePay details", 6500),
        ],
        4000,
    ),
    (
        "02-first-time-check",
        "First-time earnings check",
        "Member-facing progress with behind-the-scenes decisioning",
        [
            ("welcome", "The member chooses to check available earnings", 2500),
            ("progress-1", "Updating account activity", 1300),
            ("progress-2", "Confirming earnings information", 1300),
            ("progress-3", "Calculating available earnings", 1300),
            ("progress-4", "Preparing the AnyTimePay account", 1600),
            ("details", "A successful check opens the native account experience", 3000),
        ],
    ),
    (
        "03-halted-check",
        "Halted earnings check",
        "A clear support reference without exposing internal risk signals",
        [
            ("home-active", "The member begins an availability refresh", 2200),
            ("returning-1", "Completed steps remain visible", 1600),
            ("halted", "The exact halted step, timestamp and reference support the call center", 5000),
        ],
    ),
    (
        "04-returning-refresh",
        "Returning-member refresh",
        "Availability is revalidated during each pay cycle",
        [
            ("home-active", "The last known balance is visible before refresh", 2200),
            ("returning-1", "Updating account activity", 1100),
            ("returning-2", "Confirming earnings information", 1100),
            ("returning-3", "Calculating available earnings", 1100),
            ("returning-4", "Refreshing AnyTimePay", 1400),
            ("details", "The confirmed balance and pay-cycle status are ready", 3000),
        ],
    ),
    (
        "05-nudge-access",
        "Nudge Financial Wellness",
        "In-context access from the AnyTimePay account",
        [
            ("details", "Financial Wellness sits beside the Cash-to-Payday Outlook", 5000),
            ("nudge-after", "Explore Nudge opens a separate, broader wellness experience", 5000),
        ],
    ),
]

for args in packages:
    print(build(*args))
