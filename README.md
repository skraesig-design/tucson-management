# Tucson Management website

Static site, no build step needed to host it. Pages: home, rentals, tenants, owners, communities, philosophy, contact.
Open `index.html` in a browser to view it locally.

## Files
- `index.html` and `*/index.html`: the pages (so tucsonmgmt.com/tenants/ works on GitHub Pages)
- `site.css`, `site.js`: shared styles, painted placeholder scenes, parallax, rental filter
- `img/`: TM AZ logo and the member/affiliation logos (cropped from the uploaded screenshot)
- `_build/`: the generator. Edit `_build/build.py` (and `home_main.html`, `site.css`, `site.js`) then run `python3 _build/build.py .` from this folder to regenerate every page with the shared header and footer.

## Host on GitHub Pages
1. Put everything in this folder at the root of a GitHub repo.
2. Repo Settings > Pages > Deploy from branch > `main` / root.
3. To keep tucsonmgmt.com, add a `CNAME` file containing `tucsonmgmt.com` and point the domain's DNS at GitHub Pages.

## Still to do
- Dennis's headshot is in place (`img/dennis-kraesig.jpg`). Real home photos: add `data-src="img/your-photo.jpg"` to any `.ph` or `.band-bg` element and the photo replaces the illustration (parallax keeps working).
- Rentals page shows six example listings; connect real listings.
- Owners/tenants service and step copy is draft wording; have Dennis review it.
- Wire the contact form to a form service (e.g. Formspree).
- Fill in the real Facebook, LinkedIn and YouTube profile links.
