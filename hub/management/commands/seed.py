from datetime import timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from hub.models import Club, Event, JoinRequest


CLUBS = [
    {
        "name": "Strathmore Robotics Club",
        "tagline": "Build, break, repeat.",
        "category": "tech",
        "color": (27, 63, 42),
        "description": (
            "We design, build, and programme robots — from line-followers to "
            "small autonomous rovers. Whether you've never touched an Arduino "
            "or you've been soldering since high school, there's a bench for you."
        ),
        "events": [
            {"title": "Intro to Arduino Workshop", "days": 3, "hours": 17,
             "location": "Engineering Lab B2", "color": (36, 82, 56),
             "description": "Hands-on session: wire up your first LED circuit and blink it. Kits provided."},
            {"title": "Robotics Demo Day", "days": 14, "hours": 14,
             "location": "Main Quad", "color": (52, 110, 75),
             "description": "Members showcase their semester projects. Come watch the bots race."},
        ],
    },
    {
        "name": "Debate Society",
        "tagline": "Sharpen your voice.",
        "category": "academic",
        "color": (36, 82, 56),
        "description": (
            "Weekly British Parliamentary debates, public-speaking drills, and "
            "prep for inter-university tournaments. No experience needed — "
            "we'll teach you the format in one session."
        ),
        "events": [
            {"title": "Weekly Debate: AI & Ethics", "days": 2, "hours": 18,
             "location": "Auditorium 1", "color": (20, 48, 31),
             "description": "Motion released 15 minutes before. Spectators welcome."},
        ],
    },
    {
        "name": "Eco Warriors",
        "tagline": "Greener campus, greener future.",
        "category": "community",
        "color": (52, 110, 75),
        "description": (
            "A sustainability-focused club running campus cleanups, tree-planting "
            "drives, and waste-audit projects. We partner with the university "
            "facilities team on real changes to how the campus runs."
        ),
        "events": [
            {"title": "Campus Cleanup Drive", "days": 5, "hours": 9,
             "location": "Main Gate", "color": (27, 63, 42),
             "description": "Gloves and bags provided. Two hours, then breakfast on us."},
        ],
    },
    {
        "name": "Music & Arts Collective",
        "tagline": "Where sound meets colour.",
        "category": "arts",
        "color": (20, 48, 31),
        "description": (
            "An open collective for musicians, poets, visual artists, and anyone "
            "who makes things. We run open mics, jam sessions, and a small "
            "exhibition every semester."
        ),
        "events": [
            {"title": "Open Mic Night", "days": 7, "hours": 19,
             "location": "Student Centre Lounge", "color": (36, 82, 56),
             "description": "Sign up on the night. Five minutes per act. All genres welcome."},
        ],
    },
    {
        "name": "Entrepreneurship Hub",
        "tagline": "From idea to impact.",
        "category": "business",
        "color": (14, 31, 22),
        "description": (
            "For students building something — a side project, a startup, or just "
            "a curiosity. We host pitch nights, founder talks, and peer feedback "
            "sessions. No business plan required to show up."
        ),
        "events": [
            {"title": "Startup Pitch Night", "days": 10, "hours": 18,
             "location": "Innovation Space", "color": (52, 110, 75),
             "description": "Three-minute pitches to a panel of alumni founders. Feedback, not funding — yet."},
        ],
    },
]

JOIN_REQUESTS = [
    {"club": "Strathmore Robotics Club", "name": "Amina W.", "email": "amina.w@strathmore.edu",
     "message": "I've been tinkering with Arduino at home — would love to join."},
    {"club": "Debate Society", "name": "Brian O.", "email": "brian.o@strathmore.edu",
     "message": "First-time debater, a bit nervous, but keen."},
    {"club": "Eco Warriors", "name": "Cynthia M.", "email": "cynthia.m@strathmore.edu",
     "message": "Interested in the tree-planting drive especially."},
]


def make_image(label, color, size=(600, 400)):
    """Solid green cover with a big initial. Returns PNG bytes."""
    from PIL import Image, ImageDraw, ImageFont

    W, H = size
    img = Image.new("RGB", (W, H), color)
    draw = ImageDraw.Draw(img)
    letter = (label or "?")[0].upper()

    font = None
    for name in ("arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            font = ImageFont.truetype(name, int(H * 0.55))
            break
        except Exception:
            continue
    if font is None:
        try:
            font = ImageFont.load_default(size=int(H * 0.55))
        except TypeError:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), letter, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((W - tw) / 2 - bbox[0], (H - th) / 2 - bbox[1]),
        letter, fill=(223, 241, 229), font=font,
    )
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class Command(BaseCommand):
    help = "Create or update all sample clubs, events, and join requests. Safe to re-run."

    def handle(self, *args, **options):
        clubs_n, events_n, jr_n = 0, 0, 0

        for data in CLUBS:
            club, _ = Club.objects.update_or_create(
                name=data["name"],
                defaults={
                    "tagline": data["tagline"],
                    "description": data["description"],
                    "category": data["category"],
                },
            )
            # Always (re)generate a cover so images never go missing
            if not club.image:
                club.image.save(
                    f"club-{club.pk}.png",
                    ContentFile(make_image(club.name, data["color"])),
                    save=True,
                )
            clubs_n += 1

            for ev in data["events"]:
                event, _ = Event.objects.update_or_create(
                    club=club, title=ev["title"],
                    defaults={
                        "description": ev["description"],
                        "date": timezone.now() + timedelta(days=ev["days"], hours=ev["hours"]),
                        "location": ev["location"],
                    },
                )
                if not event.image:
                    event.image.save(
                        f"event-{event.pk}.png",
                        ContentFile(make_image(event.title, ev["color"], size=(800, 450))),
                        save=True,
                    )
                events_n += 1

        for jr in JOIN_REQUESTS:
            club = Club.objects.filter(name=jr["club"]).first()
            if not club:
                continue
            JoinRequest.objects.update_or_create(
                email=jr["email"],
                defaults={"club": club, "name": jr["name"], "message": jr["message"]},
            )
            jr_n += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded: {clubs_n} clubs, {events_n} events, {jr_n} join requests "
            f"(created or updated — nothing deleted)."
        ))