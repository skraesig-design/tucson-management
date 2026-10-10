"""Builds the Tucson Management static site.

python3 build.py OUT_DIR [--preview]
--preview writes the home page without its <!doctype>/<head> wrapper (the Artifact host adds one).
"""
import os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
PREVIEW = '--preview' in sys.argv

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700&family=Public+Sans:wght@400;500;600&display=swap">')

NAV = [('rentals', 'Rentals'), ('tenants', 'Tenants'), ('owners', 'Owners'),
       ('communities', 'Communities'), ('philosophy', 'Philosophy')]

TENANT_TEL, TENANT_MAIL = '(520) 440-6342', 'dlkraesig@gmail.com'
OWNER_TEL, OWNER_MAIL = '(520) 331-1962', 'helpumanagerentals@gmail.com'


def tel(n):
    return 'tel:+1' + re.sub(r'\D', '', n)


def header(R, cur):
    links = ''.join(
        f'<a href="{R}{slug}/index.html"{" aria-current=\"page\"" if slug == cur else ""}>{label}</a>\n      '
        for slug, label in NAV)
    cta_cur = ' aria-current="page"' if cur == 'contact' else ''
    return f'''<header class="topbar">
  <div class="wrap">
    <a class="brand" href="{R}index.html" aria-label="Tucson Management home">
      <img class="brand-mark" src="{R}img/tmaz-logo.png" alt="" width="44" height="44">
      <span class="brand-name">Tucson Management</span>
    </a>
    <nav class="nav" aria-label="Main">
      {links}<a class="cta" href="{R}contact/index.html"{cta_cur}>Contact</a>
    </nav>
  </div>
</header>
'''


def footer(R):
    nav = ''.join(f'<li><a href="{R}{s}/index.html">{l}</a></li>' for s, l in NAV) + f'<li><a href="{R}contact/index.html">Contact</a></li>'
    return f'''<div class="logos" aria-label="Memberships and affiliations">
  <div class="wrap">
    <p>Members &amp; affiliations</p>
    <div class="logo-row">
    <img src="{R}img/realty-executives.png" alt="Realty Executives Arizona Territory" width="590" height="327">
    <img class="tar" src="{R}img/tucson-realtors.png" alt="Tucson Association of Realtors" width="320" height="115">
    <img src="{R}img/crpm.png" alt="CRPM, Certified Residential Property Manager" width="416" height="265">
    <img src="{R}img/narpm.png" alt="NARPM" width="431" height="211">
    <img src="{R}img/help-u-manage.png" alt="Help-U-Manage" width="674" height="389">
    <img class="sq" src="{R}img/equal-housing.png" alt="Equal Housing Opportunity" width="236" height="240">
    <img class="sq" src="{R}img/realtor.png" alt="Realtor" width="216" height="234">
    </div>
  </div>
</div>
<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>Tucson Management</h4>
        <p style="margin:0">Tucson, Arizona<br>Open Monday through Sunday, 8am to 7pm</p>
        <p class="lic" style="margin:12px 0 0">TAR Member #19071 · NRDS #148027079<br>License #SA566445000</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>{nav}</ul>
      </div>
      <div>
        <h4>Follow</h4>
        <ul><li><a href="https://www.facebook.com/">Facebook</a></li><li><a href="https://www.linkedin.com/">LinkedIn</a></li><li><a href="https://twitter.com/DKraesig">Twitter @DKraesig</a></li><li><a href="https://www.youtube.com/">YouTube</a></li></ul>
      </div>
    </div>
    <p class="disclaimer">Dennis Kraesig, National Help U Manage LLC and Help-U-Manage LLC do not provide property management to the general public and do not act as property managers for Realty Executives Arizona Territory. They provide private property management for Aina Investments LLC. Use of this website for Property Management outside of Aina Investments is not allowed.</p>
    <div class="copy"><span>© 2026 Tucson Management</span><a href="{R}contact/index.html#terms">Terms of Use</a></div>
  </div>
</footer>
'''


def page_hero(title_html, lede, crumb, seed, actions=''):
    return f'''<section class="hero sub" aria-labelledby="hero-title">
    <div class="wrap hero-copy" data-depth="0.28">
      <p class="crumbs"><a href="../index.html">Home</a> / {crumb}</p>
      <h1 id="hero-title">{title_html}</h1>
      <p class="hero-lede">{lede}</p>
      {actions}
    </div>
    <div class="hero-scene" data-seed="{seed}" aria-hidden="true"></div>
  </section>'''


def callout(R, heading, sub, number):
    return f'''<div class="callout">
        <div><h2>{heading}</h2><p>{sub}</p></div>
        <a class="tel" href="{tel(number)}">{number}</a>
      </div>'''


def doc(title, desc, R, cur, main, wrap=True):
    head = f'<title>{title}</title>\n{FONTS}\n<link rel="stylesheet" href="{R}site.css">\n'
    body = f'{header(R, cur)}\n{main}\n{footer(R)}<script src="{R}site.js"></script>\n'
    if not wrap:
        return head + '\n' + body
    return (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<meta name="description" content="{desc}">\n{head}</head>\n<body>\n{body}</body>\n</html>\n')


def ph(scene, seed, label, src=None, R='../'):
    s = f' data-src="{R}img/photos/{src}.jpg"' if src else ''
    return f'<div class="ph" role="img" aria-label="{label}" data-scene="{scene}" data-seed="{seed}"{s}></div>'


# ---------------- Home ----------------
home = open(os.path.join(HERE, 'home_main.html')).read()
R = ''
for a, b in [
    ('<a class="btn" href="#contact">Let\'s talk</a>\n          <a class="textlink" href="#communities">View all rentals</a>',
     '<a class="btn" href="contact/index.html">Let\'s talk</a>\n          <a class="textlink" href="rentals/index.html">View all rentals</a>'),
    ('<form id="search-form" role="search">', '<form id="search-form" role="search" data-target="rentals/index.html">'),
    ('<a class="textlink" href="#contact">View all rentals</a>\n', '<div class="head-actions"><a class="textlink" href="communities/index.html">All communities</a>\n'),
    ('aria-label="Next communities">→</button></div>', 'aria-label="Next communities">→</button></div></div>'),
    ('<a class="btn" href="#contact">Let\'s talk</a>\n      </div>\n    </div>\n  </section>',
     '<a class="btn" href="contact/index.html">Let\'s talk</a>\n      </div>\n    </div>\n  </section>'),
]:
    assert a in home, a[:70]
    home = home.replace(a, b, 1)
home = re.sub(r'\s*<div class="affil".*?</div>\n  </div>\n', '\n', home, flags=re.S)
home = home.replace('</ul>\n    </div>\n  </section>\n\n  <section class="meet"',
                    '</ul>\n      <p style="margin:32px 0 0"><a class="textlink" href="philosophy/index.html">Read our philosophy</a></p>\n    </div>\n  </section>\n\n  <section class="meet"', 1)
for slug, name in [('sabino', 'Sabino Canyon'), ('university', 'University &amp; Central'), ('oro-valley', 'Oro Valley'), ('foothills', 'Catalina Foothills')]:
    home = home.replace(f'<h3>{name}</h3>', f'<h3><a href="communities/index.html#{slug}" style="text-decoration:none">{name}</a></h3>', 1)
assert 'affil' not in home

pages = {'index.html': doc('Tucson Management',
                           'Tucson Management: rentals and landlord support across Tucson with Dennis Kraesig.',
                           '', 'home', home, wrap=not PREVIEW)}

# ---------------- Rentals ----------------
R = '../'
LISTINGS = [
    ('Casas Adobes', 'Tile-roof home with a desert garden', 2350, 3, 2, 'golden:adobe', 61, 'casas-adobes'),
    ('University &amp; Central', 'Bright apartment near campus', 1450, 2, 1, 'morning:adobe', 62, 'university'),
    ('Oro Valley', 'Home with a covered patio and pool', 2950, 4, 3, 'day:modern', 63, 'oro-valley'),
    ('Sabino Canyon', 'Loft-style home near the canyon trails', 2650, 3, 2, 'dusk:modern', 64, 'sabino-canyon'),
    ('Drexel Heights', 'Adobe home with a walled courtyard', 2150, 3, 2, 'golden:modern', 65, 'drexel-heights'),
    ('Catalina Foothills', 'Foothills home with a mountain view', 3400, 4, 3, 'morning:adobe', 66, 'catalina-foothills'),
]
cards = ''.join(f'''
        <article class="listing" data-price="{p}" data-beds="{bd}" data-baths="{ba}">
          {ph(sc, sd, 'Example rental home', src)}
          <div class="body">
            <span class="loc place-loc" style="font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600">{area}</span>
            <div class="price">${p:,}<small> / month</small></div>
            <h3>{title}</h3>
            <div class="specs"><span>{bd} beds</span><span>{ba} baths</span></div>
            <div class="tagrow"><span class="pill">For rent</span><span class="pill alt">Example</span></div>
          </div>
        </article>''' for area, title, p, bd, ba, sc, sd, src in LISTINGS)
rentals = f'''<main id="top">
  {page_hero('Rentals', 'Homes for rent across Tucson, from the university to the foothills.', 'Rentals', 21)}
  <section class="search" aria-label="Search rentals">
    <div class="wrap">
      <form id="rent-filter" role="search">
        <label for="q"><span>Where</span><input id="q" name="q" type="text" placeholder="City, neighborhood, or listing ID"></label>
        <label for="price"><span>Price max</span>
          <select id="price" name="price"><option value="">Any</option><option value="1500">$1,500</option><option value="2000">$2,000</option><option value="2500">$2,500</option><option value="3000">$3,000</option></select></label>
        <label for="beds"><span>Beds</span>
          <select id="beds" name="beds"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option></select></label>
        <label for="baths"><span>Baths</span>
          <select id="baths" name="baths"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option></select></label>
        <button class="btn" type="submit">Search</button>
      </form>
    </div>
  </section>
  <section class="places" style="padding-top:clamp(8px,2vw,24px)" aria-labelledby="list-title">
    <div class="wrap">
      <div class="rent-bar">
        <strong id="list-title">Available now · <span id="rent-count">6 homes</span></strong>
        <span class="note">These are example listings. Current homes will appear here once listings are connected.</span>
      </div>
      <div class="listings">{cards}
      </div>
      <p id="rent-empty" class="note" hidden style="margin-top:20px">No homes match those filters. Try a higher price or fewer beds, or call us and we'll tell you what's coming up.</p>
    </div>
  </section>
  <section aria-label="Applying">
    <div class="wrap">
      {callout(R, 'Found one you like?', 'Call the tenant line to set up a showing or start an application.', TENANT_TEL)}
      <p style="margin:24px 0 0"><a class="textlink" href="../tenants/index.html">How applying works</a></p>
    </div>
  </section>
</main>'''
pages['rentals/index.html'] = doc('Rentals · Tucson Management', 'Homes for rent across Tucson.', R, 'rentals', rentals)

# ---------------- Tenants ----------------
tenants = f'''<main id="top">
  {page_hero('Tenants &amp; <span>applicants</span>', 'Looking for a home, applying, or already renting with us? Here is how it works.', 'Tenants', 22,
             '<div class="hero-actions"><a class="btn" href="../rentals/index.html">Browse rentals</a><a class="textlink" href="#renting">Already renting</a></div>')}
  <section class="places" aria-labelledby="apply-title">
    <div class="wrap">
      <div class="head"><div><p class="eyebrow">Applying</p><h2 id="apply-title">From first look to move-in</h2></div></div>
      <ol class="steps">
        <li><h3>Find a home</h3><p>Browse the current rentals or tell us what you need and where.</p></li>
        <li><h3>Call or email</h3><p>Reach the tenant line to ask questions and set up a showing.</p></li>
        <li><h3>Apply</h3><p>We'll walk you through the application and what you'll need to bring.</p></li>
        <li><h3>Move in</h3><p>Sign your lease, get your keys and settle in.</p></li>
      </ol>
    </div>
  </section>
  <section id="renting" aria-labelledby="renting-title">
    <div class="wrap">
      <div class="split">
        <div>
          <p class="eyebrow">Already renting</p>
          <h2 id="renting-title">We're a phone call away</h2>
          <div class="prose">
            <p>Questions about your lease, rent, or something that needs fixing at home? Call or email the tenant line and we'll help you sort it out.</p>
            <p>We answer seven days a week, Monday through Sunday, 8am to 7pm.</p>
          </div>
          <ul class="facts"><li>{TENANT_TEL}</li><li>{TENANT_MAIL}</li></ul>
          <a class="btn" href="../contact/index.html">Contact us</a>
        </div>
        {ph('morning:adobe', 31, 'Bright living room in a rental home', 'sabino-canyon')}
      </div>
    </div>
  </section>
  <section class="places" aria-label="Fair housing">
    <div class="wrap" style="display:grid;gap:28px">
      {callout(R, 'Tenant &amp; applicant line', 'Open Monday through Sunday, 8am to 7pm.', TENANT_TEL)}
      <div class="ehl"><img src="../img/equal-housing.png" alt="Equal Housing Opportunity"><p>We are committed to fair housing and equal opportunity for every applicant.</p></div>
    </div>
  </section>
</main>'''
pages['tenants/index.html'] = doc('Tenants · Tucson Management', 'Applying for and renting a home with Tucson Management.', R, 'tenants', tenants)

# ---------------- Owners ----------------
SERVICES = [
    ('Self-management help', 'Run your own rentals with an experienced hand to call on when you need one.'),
    ('Pricing your rental', 'Set a rent that fits the Tucson market and your neighborhood.'),
    ('Finding tenants', 'Get your property in front of the right renters.'),
    ('Screening applicants', 'Know what to look for before you hand over the keys.'),
    ('Leases &amp; paperwork', 'Keep your agreements clear and your records in order.'),
    ('Portfolio consulting', 'Plan the next step for your properties, whether you are buying, holding or selling.'),
]
svc = ''.join(f'<div class="service"><h3>{h}</h3><p>{p}</p></div>' for h, p in SERVICES)
owners = f'''<main id="top">
  {page_hero('Owners &amp; <span>landlords</span>', 'We help you manage your own rental properties.', 'Owners', 23,
             '<div class="hero-actions"><a class="btn" href="../contact/index.html">Let\'s talk</a><a class="textlink" href="#brokers">Brokers &amp; agents</a></div>')}
  <section class="places" aria-labelledby="svc-title">
    <div class="wrap">
      <div class="head"><div><p class="eyebrow">For landlords</p><h2 id="svc-title">Keep control. Get help where it counts.</h2></div></div>
      <div class="services">{svc}</div>
    </div>
  </section>
  <section aria-labelledby="why-title">
    <div class="wrap">
      <div class="split flip">
        <div>
          <p class="eyebrow">Why it matters</p>
          <h2 id="why-title">Your portfolio is more than an asset</h2>
          <div class="prose">
            <p>Your rentals are your security, your livelihood and your future. Dennis brings a lifetime of real estate knowledge to helping you protect them.</p>
            <p>He is a Certified Residential Property Manager and a member of NARPM and National Help-U-Manage.</p>
          </div>
          <a class="btn" href="../philosophy/index.html">Meet Dennis</a>
        </div>
        {ph('dusk:portfolio', 32, 'A row of rental homes with a Rented sign')}
      </div>
      <div class="split" id="brokers">
        <div>
          <p class="eyebrow">Brokers &amp; agents</p>
          <h2>Resources for real estate pros</h2>
          <div class="prose"><p>Consulting for brokers and agents who have clients with rental properties, or rental questions of their own. Let's work together.</p></div>
          <a class="btn" href="../contact/index.html">Let's talk</a>
        </div>
        {ph('golden:openhouse', 33, 'Open house sign in front of a modern home')}
      </div>
    </div>
  </section>
  <section class="places" aria-label="Landlord line">
    <div class="wrap">{callout(R, 'Landlord line', 'Call or email ' + OWNER_MAIL + '. Open daily, 8am to 7pm.', OWNER_TEL)}</div>
  </section>
</main>'''
pages['owners/index.html'] = doc('Owners · Tucson Management', 'Help for Tucson landlords who self-manage their rentals.', R, 'owners', owners)

# ---------------- Communities ----------------
COMM = [
    ('sabino', 'Sabino Canyon', 'Northeast Tucson', 'golden:adobe', 41, 'sabino-canyon',
     'Homes close to Sabino Canyon Recreation Area, with trails, desert washes and the Santa Catalinas right outside the door.', ['Hiking trails', 'Mountain views', 'Quiet streets']),
    ('university', 'University &amp; Central', 'Central Tucson', 'morning:adobe', 42, 'university',
     'Rentals near the University of Arizona, downtown and the streetcar line. Great for students, faculty and anyone who wants to walk to dinner.', ['Near campus', 'Streetcar', 'Downtown']),
    ('oro-valley', 'Oro Valley', 'North of Tucson', 'dusk:modern', 43, 'oro-valley',
     'A quieter town just north of the city, with big views of Pusch Ridge, parks and golf.', ['Pusch Ridge views', 'Parks', 'Golf']),
    ('foothills', 'Catalina Foothills', 'North Tucson', 'day:modern', 44, 'catalina-foothills',
     'Desert homes in the foothills above the city, with sweeping views of the valley and the city lights at night.', ['City-light views', 'Desert lots', 'Foothills trails']),
    ('casas-adobes', 'Casas Adobes', 'Northwest Tucson', 'golden:adobe', 46, 'casas-adobes',
     'Established neighborhoods on the northwest side, close to shopping, schools and the Tortolita and Catalina mountain views.', ['Mountain views', 'Established streets', 'Close to shopping']),
    ('drexel-heights', 'Drexel Heights', 'Southwest Tucson', 'day:adobe', 47, 'drexel-heights',
     'Room to spread out on the southwest side, with desert lots and Tucson Mountain Park nearby.', ['Bigger lots', 'Tucson Mountain Park', 'Desert living']),
]
rows = ''
for i, (slug, name, loc, sc, sd, src, text, facts) in enumerate(COMM):
    fl = ' flip' if i % 2 else ''
    rows += f'''
      <div class="split{fl}" id="{slug}">
        <div>
          <p class="eyebrow">{loc}</p>
          <h2>{name}</h2>
          <div class="prose"><p>{text}</p></div>
          <ul class="facts">{''.join(f'<li>{f}</li>' for f in facts)}</ul>
          <a class="textlink" href="../rentals/index.html">See rentals</a>
        </div>
        {ph(sc, sd, name + ' home', src)}
      </div>'''
communities = f'''<main id="top">
  {page_hero('Where can you <span>go?</span>', 'Tucson neighborhoods where we help people find homes.', 'Communities', 24)}
  <section aria-label="Communities">
    <div class="wrap">{rows}
    </div>
  </section>
  <section class="band" aria-labelledby="band-title">
    <div class="band-bg" role="img" aria-label="Modern desert home at golden hour" data-scene="golden:band" data-seed="45" data-band></div>
    <div class="wrap">
      <div class="band-card">
        <p class="eyebrow">Not sure where to start?</p>
        <h2 id="band-title">Tell us what you need</h2>
        <p>Share your budget and how you want to live, and we'll point you to the right part of town.</p>
        <a class="btn" href="../contact/index.html">Let's talk</a>
      </div>
    </div>
  </section>
</main>'''
pages['communities/index.html'] = doc('Communities · Tucson Management', 'Tucson neighborhoods we serve.', R, 'communities', communities)

# ---------------- Philosophy ----------------
meet = home[home.index('<section class="meet"'):home.index('</section>', home.index('<section class="meet"')) + 10]
meet = meet.replace('href="contact/index.html"', 'href="../contact/index.html"').replace('src="img/', 'src="../img/')
phil_list = home[home.index('<ul class="principles">'):home.index('</ul>', home.index('<ul class="principles">')) + 5]
philosophy = f'''<main id="top">
  {page_hero('Our <span>philosophy</span>', 'Our pride comes from making your life easier.', 'Philosophy', 25)}
  <section class="philosophy" aria-label="Principles">
    <div class="wrap">
      <p class="eyebrow">What we believe</p>
      {phil_list}
    </div>
  </section>
  {meet}
  <section class="places" aria-labelledby="cred-title">
    <div class="wrap">
      <div class="head"><div><p class="eyebrow">Credentials</p><h2 id="cred-title">Licensed and certified</h2></div></div>
      <div class="services">
        <div class="service"><h3>CRPM</h3><p>Certified Residential Property Manager.</p></div>
        <div class="service"><h3>NARPM</h3><p>Member, National Association of Residential Property Managers.</p></div>
        <div class="service"><h3>Realtor</h3><p>TAR Member #19071 · NRDS #148027079 · License #SA566445000.</p></div>
      </div>
    </div>
  </section>
</main>'''
pages['philosophy/index.html'] = doc('Philosophy · Tucson Management', 'What Tucson Management believes, and who Dennis Kraesig is.', R, 'philosophy', philosophy)

# ---------------- Contact ----------------
contact_sec = home[home.index('<section class="contact"'):home.index('</section>', home.index('<section class="contact"')) + 10]
contact_sec = contact_sec.replace('<p class="eyebrow">Contact</p>\n        <h2 id="contact-title">Let\'s talk</h2>',
                                  '<p class="eyebrow">Two lines, seven days</p>\n        <h2 id="contact-title">Call, email or write</h2>')
contact = f'''<main id="top">
  {page_hero('Let\'s <span>talk</span>', 'So let\'s talk about how we can protect your portfolio, or find your next home.', 'Contact', 26)}
  {contact_sec}
  <section id="terms" aria-labelledby="terms-title">
    <div class="wrap">
      <p class="eyebrow">Terms of use</p>
      <h2 id="terms-title" style="font-size:clamp(24px,3vw,36px);font-weight:400;text-transform:uppercase;margin:10px 0 16px">Please note</h2>
      <div class="prose"><p>Dennis Kraesig, National Help U Manage LLC and Help-U-Manage LLC do not provide property management to the general public and do not act as property managers for Realty Executives Arizona Territory. They provide private property management for Aina Investments LLC. Use of this website for Property Management outside of Aina Investments is not allowed.</p></div>
    </div>
  </section>
</main>'''
pages['contact/index.html'] = doc('Contact · Tucson Management', 'Phone, email and hours for Tucson Management.', R, 'contact', contact)

# ---------------- Write ----------------
for path, html in pages.items():
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    open(full, 'w').write(html)
for f in ['site.css', 'site.js']:
    shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
print('built', len(pages), 'pages into', OUT)
