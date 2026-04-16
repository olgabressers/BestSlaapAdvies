/*!
 * BesteSlaapAdvies — centralised affiliate-link wrapper
 *
 * PURPOSE
 *   Every retailer link on the site is a plain search/product URL. This helper
 *   scans all outbound links on page load and rewrites them to include affiliate
 *   tracking — but only if you've filled in a real ID below. Empty IDs = links
 *   are left unchanged (safe default, nothing breaks).
 *
 * HOW TO ACTIVATE
 *   1. Apply to each affiliate programme (Amazon NL Associates, Bol partner-
 *      programma OR Daisycon, Awin).
 *   2. Fill in the matching ID in the AFF object below.
 *   3. Push. Every existing and future retailer link is automatically wrapped.
 *
 * TO OPT A SPECIFIC LINK OUT OF WRAPPING
 *   Add data-aff="skip" to the <a> tag. Useful for links to affiliate.bol.com
 *   or the admin page where you don't want wrapping.
 *
 * AUDITING
 *   After activation, click a link and inspect the URL — it should now include
 *   your tag/ID. Also check DevTools → Network → the first request on the
 *   retailer site.
 */
(function () {
  'use strict';

  // ---------------------------------------------------------------------------
  // CONFIG — fill these in when your affiliate approvals come through
  // ---------------------------------------------------------------------------
  const AFF = {
    // Amazon Associates NL — append ?tag=XYZ-21 to every amazon.nl link
    // Example: 'besteslaap-21'
    amazon: 'besteslaapadvies21',

    // Bol.com partnerprogramma — direct partner ID (sometimes called "site ID")
    // Wraps every bol.com link via partnerprogramma.bol.com/click/click
    // Example: '1234567'
    bol: '1515810',

    // Daisycon — alternative way to monetise Bol.com + many NL shops
    // Fill in EITHER `bol` OR `daisycon.publisherId` — not both (bol takes
    // precedence). Daisycon gives you a single publisher ID and per-programme
    // IDs; the helper wraps the URL via Daisycon's click-tracker.
    daisycon: {
      publisherId: '',           // e.g. '123456'
      bolProgrammeId: ''         // e.g. '78910' — the ID Daisycon gives for Bol.com specifically
    },

    // Awin — one publisher ID covers every Awin merchant (Vitaminstore, Holland
    // & Barrett, iHerb, etc.). You still need the per-merchant `mid` (merchant
    // ID) that Awin supplies once you're accepted for each programme.
    awin: {
      publisherId: '',            // e.g. '987654'
      merchants: {
        // map a retailer hostname → Awin merchant ID ("mid")
        // 'www.vitaminstore.nl':     '12345',
        // 'www.hollandandbarrett.nl': '23456',
        // 'nl.iherb.com':             '34567'
      }
    }
  };

  // ---------------------------------------------------------------------------
  // URL WRAPPERS — pure functions, one per programme
  // ---------------------------------------------------------------------------
  function wrapAmazon(originalUrl) {
    if (!AFF.amazon) return originalUrl;
    try {
      const u = new URL(originalUrl);
      if (!/(^|\.)amazon\.nl$/i.test(u.hostname)) return originalUrl;
      u.searchParams.set('tag', AFF.amazon);
      return u.toString();
    } catch (e) { return originalUrl; }
  }

  function wrapBol(originalUrl) {
    // Prefer direct Bol partnerprogramma ID if set, else fall back to Daisycon
    if (AFF.bol) {
      return 'https://partnerprogramma.bol.com/click/click?p=1&t=url' +
             '&s=' + encodeURIComponent(AFF.bol) +
             '&url=' + encodeURIComponent(originalUrl) +
             '&f=TXL&name=affiliate';
    }
    if (AFF.daisycon.publisherId && AFF.daisycon.bolProgrammeId) {
      // Daisycon click URL format (v2): ds1.nl/c/?si=<pub>&li=<programme>&url=<encoded>
      return 'https://ds1.nl/c/?si=' + encodeURIComponent(AFF.daisycon.publisherId) +
             '&li=' + encodeURIComponent(AFF.daisycon.bolProgrammeId) +
             '&url=' + encodeURIComponent(originalUrl);
    }
    return originalUrl;
  }

  function wrapAwin(originalUrl, merchantId) {
    if (!AFF.awin.publisherId || !merchantId) return originalUrl;
    // Awin click URL: https://www.awin1.com/cread.php?awinmid=MID&awinaffid=PUB&ued=ENCODED
    return 'https://www.awin1.com/cread.php' +
           '?awinmid=' + encodeURIComponent(merchantId) +
           '&awinaffid=' + encodeURIComponent(AFF.awin.publisherId) +
           '&ued=' + encodeURIComponent(originalUrl);
  }

  // ---------------------------------------------------------------------------
  // ROUTING — pick the right wrapper based on hostname
  // ---------------------------------------------------------------------------
  function rewrite(href) {
    if (!href || !/^https?:\/\//i.test(href)) return href;
    let host;
    try { host = new URL(href).hostname.toLowerCase(); } catch (e) { return href; }

    if (/(^|\.)amazon\.nl$/.test(host))           return wrapAmazon(href);
    if (/(^|\.)bol\.com$/.test(host))             return wrapBol(href);

    const awinMid = AFF.awin.merchants[host];
    if (awinMid)                                   return wrapAwin(href, awinMid);

    return href;
  }

  // ---------------------------------------------------------------------------
  // PROCESS EVERY LINK ON THE PAGE
  // ---------------------------------------------------------------------------
  function processLinks() {
    const links = document.querySelectorAll('a[href^="http"]');
    links.forEach(function (a) {
      if (a.dataset.aff === 'skip') return;
      if (a.dataset.affProcessed) return;

      const original = a.href;
      const wrapped = rewrite(original);
      if (wrapped !== original) {
        a.href = wrapped;
        a.dataset.affProcessed = '1';
        a.dataset.affOriginal = original;
        // Best-practice attributes on monetised outbound links
        if (!a.rel || !/\bsponsored\b/.test(a.rel)) {
          a.rel = (a.rel ? a.rel + ' ' : '') + 'sponsored';
        }
        if (!a.rel.includes('nofollow')) a.rel += ' nofollow';
      }
    });
  }

  // Run now if DOM is already parsed, else wait
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', processLinks);
  } else {
    processLinks();
  }

  // Watch for dynamically-added links (compare modals, JS-rendered content)
  var observer = new MutationObserver(function (mutations) {
    var hasNewLinks = mutations.some(function (m) {
      return m.addedNodes.length > 0;
    });
    if (hasNewLinks) processLinks();
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });

  // Expose for debugging: window.__aff.status() prints whether any ID is active
  window.__aff = {
    status: function () {
      const on = [];
      if (AFF.amazon) on.push('Amazon NL');
      if (AFF.bol) on.push('Bol.com (direct)');
      if (AFF.daisycon.publisherId && AFF.daisycon.bolProgrammeId) on.push('Bol.com (via Daisycon)');
      if (AFF.awin.publisherId) on.push('Awin (' + Object.keys(AFF.awin.merchants).length + ' merchants)');
      console.log('[affiliate.js] Active programmes:', on.length ? on.join(', ') : 'NONE — links are unwrapped');
      return on;
    },
    rewrite: rewrite
  };
})();
