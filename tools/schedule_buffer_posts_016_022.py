#!/usr/bin/env python3
"""Schedule Instagram posts 016-022 in Buffer.
Run after queue has capacity (1 slot opens per day as posts publish).
Queue currently has posts 006-015 (10/10 free plan limit).
Posts 016-022 are May 4-10 at 17:30 UTC.
"""
import json
import urllib.request
import sys
import os

TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN", "RwgbBNLcpOVbKDuqSKp2V4PxcC-M6FRAD0-rRBkN6gY")
CHANNEL_ID = "69e144d4031bfa423c0fe604"
BASE_URL = "https://raw.githubusercontent.com/olgabressers/BestSlaapAdvies/main/content/instagram"

POSTS = [
    {
        "num": "016", "date": "2026-05-04T17:30:00.000Z",
        "img": "016_04mei_to-do-lijst.jpg",
        "text": """Je hoofd wil niet stoppen. De gedachten aan morgen — wat je nog moet doen, wat je niet mag vergeten — blijven ronddraaien zodra je gaat liggen.

Er is iets simpels wat helpt.

Schrijf voor je naar bed gaat een to-do lijst voor morgen. Niet wat je vandaag gedaan hebt, maar wat je morgen wil doen. Specifiek. Op papier.

Onderzoekers van de Baylor University ontdekten dat mensen die dit deden gemiddeld negen minuten sneller in slaap vielen. Hoe concreter de lijst, hoe sneller.

De gedachten zijn er al. Ze hebben alleen een plek nodig buiten je hoofd. Als ze op papier staan, hoeft je brein ze niet meer vast te houden.

Vanavond vijf minuten. Pen en papier. Morgen begint al een beetje rustiger.

#piekeren #slaaptips #beterslapen #avondroutine #besteslaapadvies"""
    },
    {
        "num": "017", "date": "2026-05-05T17:30:00.000Z",
        "img": "017_05mei_magnesium.jpg",
        "text": """Veel mensen die slecht slapen, missen magnesium. Niet omdat ze ongezond eten — maar omdat stress magnesium verbruikt. En de meeste mensen hebben chronisch te weinig.

Magnesium helpt je zenuwstelsel tot rust te komen. Het reguleert GABA, de neurotransmitter die je brein afremt. Het ontspant je spieren. En het helpt bij het reguleren van melatonine, het hormoon dat je slaap-waakcyclus aanstuurt.

Niet elk magnesium is hetzelfde. Magnesiumglycinaat wordt het beste opgenomen en is het meest geschikt voor slaap. Magnesiumoxide is goedkoop maar werkt nauwelijks.

Wij vergeleken de beste magnesiumsupplementen voor slaap. Link in de eerste reactie.

#magnesium #supplementen #slaaptips #beterslapen #besteslaapadvies"""
    },
    {
        "num": "018", "date": "2026-05-06T17:30:00.000Z",
        "img": "018_06mei_niet-kunnen-slapen.jpg",
        "text": """We zijn nu een paar weken onderweg.

Je hebt gelezen over je slaapkamer, je avondroutine, je telefoon, cafeïne, ademhaling. Maar slapen is ook gewoon menselijk. En soms lukt het gewoon niet, ook al doe je alles goed.

Op die momenten doet iedereen iets anders. Sommigen staan op. Anderen lezen. Sommigen laten hun gedachten gaan. Weer anderen leggen gewoon hun ogen dicht en accepteren dat de slaap wel komt.

Wat doe jij op zo'n avond?

Deel het hieronder. We leren net zoveel van elkaar als van de wetenschap.

#slaapproblemen #beterslapen #slaaptips #community #besteslaapadvies"""
    },
    {
        "num": "019", "date": "2026-05-07T17:30:00.000Z",
        "img": "019_07mei_huberman-licht.jpg",
        "text": """Er is één ding dat meer invloed heeft op je slaap dan bijna alles wat je doet voor bedtijd. En de meeste mensen denken er nooit aan.

Ochtendlicht.

Andrew Huberman legt in zijn podcast uit hoe daglicht in de ochtend je biologische klok reset. Het is het startsignaal voor je lichaam: de dag begint nu. En dat signaal bepaalt precies wanneer je 's avonds moe wordt.

Geen ochtendlicht? Dan verschuift je ritme. Je wordt later moe, later wakker, en de cyclus raakt uit balans.

Tien minuten buiten in de ochtend — ook op bewolkte dagen — maakt een meetbaar verschil. Je hoeft er niks speciaals voor te doen. Gewoon naar buiten.

Huberman Lab is een van de beste podcasts over slaapwetenschap. Wij hebben de beste afleveringen voor je geselecteerd.

#hubermanlaboratory #slaapwetenschap #beterslapen #daglichtt #besteslaapadvies"""
    },
    {
        "num": "020", "date": "2026-05-08T17:30:00.000Z",
        "img": "020_08mei_4-7-8-ademhaling.jpg",
        "text": """Je ligt in bed. Je hoofd draait. Je probeert te ontspannen, maar dat lukt niet als je er bewust op let.

Dit is een techniek die rechtstreeks ingrijpt op je zenuwstelsel. Niet via je gedachten, maar via je adem.

Adem in door je neus: vier tellen.
Houd vast: zeven tellen.
Adem langzaam uit door je mond: acht tellen.

Herhaal dit vier keer.

De lange uitademing activeert je parasympathisch zenuwstelsel — het systeem dat je lichaam in rustmodus zet. Na een paar rondes merk je dat je hartslag daalt en je spieren losser worden.

Het voelt onwennig de eerste keer. Geef het een week. Vanavond kun je het meteen proberen.

#ademhaling #slaaptips #beterslapen #ontspanning #besteslaapadvies"""
    },
    {
        "num": "021", "date": "2026-05-09T17:30:00.000Z",
        "img": "021_09mei_cafeïne.jpg",
        "text": """Eén kop koffie om 14:00. Klinkt onschuldig.

Maar cafeïne heeft een halfwaardetijd van vijf tot zes uur. Dat betekent dat de helft van die koffie om 20:00 nog steeds actief in je bloed zit. En om 02:00 's nachts nog een kwart.

Je valt misschien prima in slaap. Cafeïne onderdrukt de vermoeidheid, maar verstoort ondertussen je diepe slaap. Je slaapt, maar je herstelt minder goed. Je wordt wakker en voelt je... niet uitgerust.

De eenvoudigste aanpassing: geen cafeïne na 13:00. Dat geldt ook voor thee met cafeïne, cola en energiedrankjes.

Morgen kijken we naar een andere gewoonte die je slaap ongemerkt verstoort.

#cafeine #koffie #slaaptips #beterslapen #besteslaapadvies"""
    },
    {
        "num": "022", "date": "2026-05-10T17:30:00.000Z",
        "img": "022_10mei_verzwaringsdeken.jpg",
        "text": """Er zijn nachten waarop je lichaam onrustig is. Alsof er te veel spanning in je spieren zit om echt los te laten.

Een verzwaringsdeken werkt anders dan een gewone deken. De extra zwaarte activeert je parasympathisch zenuwstelsel — het systeem dat je lichaam in rust en herstel zet. Je voelt je letterlijk neergedrukt in de matras.

Het is geen magisch hulpmiddel. Maar voor mensen die 's nachts liggen te draaien, piekeren of spanning vasthouden, kan het een groot verschil maken.

Wij vergeleken de beste verzwaringsdekens van dit moment. Welk gewicht past bij jou? Hoe kies je de juiste maat? Link in de eerste reactie.

#verzwaringsdeken #slaaptips #beterslapen #ontspanning #besteslaapadvies"""
    },
]

MUTATION = """
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess {
      post {
        id
        status
        dueAt
      }
    }
    ... on MutationError {
      userFriendlyMessage
    }
  }
}
"""

def schedule_post(post):
    img_url = f"{BASE_URL}/{post['img']}"
    variables = {
        "input": {
            "channelId": CHANNEL_ID,
            "text": post["text"],
            "mediaUrls": [img_url],
            "scheduledAt": post["date"],
            "status": "scheduled"
        }
    }
    payload = json.dumps({"query": MUTATION, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.buffer.com/graphql",
        data=payload,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def get_queue_count():
    query = '{ posts(input: { organizationId: "69c7e43022df31cc73ef2e21" }) { edges { node { id status } } } }'
    payload = json.dumps({"query": query}).encode()
    req = urllib.request.Request(
        "https://api.buffer.com/graphql",
        data=payload,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    edges = data.get("data", {}).get("posts", {}).get("edges", [])
    scheduled = [e for e in edges if e["node"]["status"] == "scheduled"]
    return len(scheduled)

# Check how many are already scheduled
try:
    count = get_queue_count()
    print(f"Current queue: {count}/10 scheduled posts")
    available_slots = 10 - count
    print(f"Available slots: {available_slots}")
except Exception as e:
    print(f"Could not check queue: {e}")
    available_slots = 10

scheduled_count = 0
skipped = []
for post in POSTS:
    if scheduled_count >= available_slots:
        skipped.append(post['num'])
        print(f"SKIP post {post['num']} — queue full ({10 - available_slots + scheduled_count}/10)")
        continue
    print(f"Scheduling post {post['num']} for {post['date']}...")
    try:
        result = schedule_post(post)
        if result.get("data", {}).get("createPost", {}).get("post"):
            post_id = result["data"]["createPost"]["post"]["id"]
            print(f"  ✓ Scheduled — ID: {post_id}")
            scheduled_count += 1
        elif result.get("data", {}).get("createPost", {}).get("userFriendlyMessage"):
            msg = result["data"]["createPost"]["userFriendlyMessage"]
            print(f"  ✗ Error: {msg}")
            skipped.append(post['num'])
        else:
            print(f"  ✗ Unexpected response: {json.dumps(result)}")
            skipped.append(post['num'])
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        skipped.append(post['num'])

print(f"\nScheduled {scheduled_count} posts.")
if skipped:
    print(f"Still pending (run again when slots open): {', '.join(skipped)}")
