# Source Onboarding Analysis

## Source Classification & Configuration Proposal

### Overview
This document analyzes 9 new sources for onboarding into the Medietat job scraping system.

---

## 1. https://etermed.pl/praca/

**Classification:** Direct medical facility career page  
**Type:** Single facility (eTermed - medical facility)  
**Difficulty:** Medium  
**City:** To be determined from page content

**Analysis:**
- Standard career page structure expected
- Likely has repeating job listing blocks
- May require Playwright if JavaScript-rendered

**Proposed Config:**
```json
{
  "sourceId": "etermed",
  "sourceName": "eTermed",
  "baseUrl": "https://etermed.pl/praca/",
  "city": "TBD",  // Extract from page
  "facilityName": "eTermed",
  "selectors": {
    "jobListContainer": "TBD",  // Auto-detect
    "jobItem": "TBD",
    "title": "TBD",
    "link": "TBD"
  },
  "metadata": {
    "confidence": "MEDIUM",
    "notes": "Standard facility page - auto-detect structure"
  }
}
```

**Edge Cases:**
- May have pagination
- City needs extraction from content

**Maintenance Cost:** Low

---

## 2. https://www.szpitalpolanki.pl/oferty_pracy

**Classification:** Direct medical facility career page  
**Type:** Single facility (Szpital Polanki)  
**Difficulty:** Low-Medium  
**City:** Gdańsk (inferred from facility name)

**Analysis:**
- Standard facility career page
- URL pattern suggests simple structure
- Likely straightforward HTML

**Proposed Config:**
```json
{
  "sourceId": "szpitalpolanki",
  "sourceName": "Szpital Polanki",
  "baseUrl": "https://www.szpitalpolanki.pl/oferty_pracy",
  "city": "Gdańsk",
  "facilityName": "Szpital Polanki",
  "selectors": {
    "jobListContainer": "TBD",
    "jobItem": "TBD",
    "title": "TBD",
    "link": "TBD"
  },
  "metadata": {
    "confidence": "MEDIUM",
    "notes": "Standard facility page"
  }
}
```

**Edge Cases:**
- May use different URL structure
- Check for pagination

**Maintenance Cost:** Low

---

## 3. https://przychodniawitomino.pl/praca/

**Classification:** Direct medical facility career page  
**Type:** Single facility (Przychodnia Witomino)  
**Difficulty:** Low-Medium  
**City:** Gdańsk (Witomino is a district of Gdańsk)

**Analysis:**
- Small facility, likely simple page
- May have limited job postings
- Standard structure expected

**Proposed Config:**
```json
{
  "sourceId": "przychodniawitomino",
  "sourceName": "Przychodnia Witomino",
  "baseUrl": "https://przychodniawitomino.pl/praca/",
  "city": "Gdańsk",
  "facilityName": "Przychodnia Witomino",
  "selectors": {
    "jobListContainer": "TBD",
    "jobItem": "TBD",
    "title": "TBD",
    "link": "TBD"
  },
  "metadata": {
    "confidence": "MEDIUM",
    "notes": "Small facility - may have few postings"
  }
}
```

**Edge Cases:**
- May have empty state when no jobs
- Low volume expected

**Maintenance Cost:** Low

---

## 4. https://www.medicover.pl/praca/pielegniarki-i-polozne/gdynia,tc,s

**Classification:** Medical network / corporate careers  
**Type:** Large corporate (Medicover - private healthcare network)  
**Difficulty:** High  
**City:** Gdynia (from URL), but may have multiple locations

**Analysis:**
- Corporate career portal
- URL suggests filtered view (nurses/midwives in Gdynia)
- May have complex filtering/pagination
- Likely JavaScript-heavy
- May require Playwright

**Proposed Config:**
```json
{
  "sourceId": "medicover_gdynia",
  "sourceName": "Medicover",
  "baseUrl": "https://www.medicover.pl/praca/pielegniarki-i-polozne/gdynia,tc,s",
  "city": "Gdynia",
  "facilityName": "Medicover",
  "selectors": {
    "jobListContainer": "TBD",
    "jobItem": "TBD",
    "title": "TBD",
    "link": "TBD"
  },
  "metadata": {
    "confidence": "LOW",
    "notes": "Corporate portal - complex structure, may need manual tuning. URL is pre-filtered for nurses/midwives in Gdynia.",
    "requiresPlaywright": true,
    "needsReview": true
  }
}
```

**Edge Cases:**
- Complex filtering system
- May have AJAX pagination
- Multiple locations per job possible
- Role filtering already in URL (nurses/midwives only)

**Risks:**
- Structure may change frequently
- May need multiple configs for different roles/locations
- High maintenance

**Maintenance Cost:** High

---

## 5. https://pcrsopot.pl/category/ogloszenia/oferty-pracy/

**Classification:** Direct medical facility career page  
**Type:** Single facility (PCR Sopot - Pomorskie Centrum Reumatologiczne)  
**Difficulty:** Low-Medium  
**City:** Sopot

**Analysis:**
- WordPress-style category page (based on URL pattern)
- Likely standard blog post structure
- Should be straightforward

**Proposed Config:**
```json
{
  "sourceId": "pcrsopot",
  "sourceName": "Pomorskie Centrum Reumatologiczne Sopot",
  "baseUrl": "https://pcrsopot.pl/category/ogloszenia/oferty-pracy/",
  "city": "Sopot",
  "facilityName": "Pomorskie Centrum Reumatologiczne",
  "selectors": {
    "jobListContainer": "TBD",  // Likely article or post container
    "jobItem": "article, .post, .entry",
    "title": "h2, h3, .entry-title",
    "link": "a"
  },
  "metadata": {
    "confidence": "MEDIUM",
    "notes": "WordPress-style category page"
  }
}
```

**Edge Cases:**
- Standard WordPress pagination
- May have date-based filtering

**Maintenance Cost:** Low

---

## 6. https://szpital-gdansk.luxmed.pl/kariera/

**Classification:** Medical network / corporate careers  
**Type:** Corporate (LUX MED - already exists!)  
**Difficulty:** N/A - Already configured  
**Status:** ✅ Already onboarded as `lux_med_szpital_gdask`

**Note:** This source is already in the system. No action needed.

---

## 7. https://www.luxmed.pl/kariera/oferty-pracy

**Classification:** Medical network / corporate careers  
**Type:** Corporate (LUX MED - main corporate portal)  
**Difficulty:** High  
**City:** Multiple (national portal)

**Analysis:**
- Main corporate career portal (different from facility-specific)
- Likely has location filtering
- May show jobs from multiple cities
- Complex structure expected
- May require Playwright

**Proposed Config:**
```json
{
  "sourceId": "luxmed_corporate",
  "sourceName": "LUX MED",
  "baseUrl": "https://www.luxmed.pl/kariera/oferty-pracy",
  "city": "Multiple",  // Extract from each job
  "facilityName": "LUX MED",
  "selectors": {
    "jobListContainer": "TBD",
    "jobItem": "TBD",
    "title": "TBD",
    "link": "TBD"
  },
  "metadata": {
    "confidence": "LOW",
    "notes": "Corporate portal - may have jobs from multiple cities. City extraction critical. May need location filtering.",
    "requiresPlaywright": true,
    "needsReview": true
  }
}
```

**Edge Cases:**
- Multiple cities per page
- Location filtering may be needed
- May need to filter to Gdańsk/Gdynia/Sopot only
- Complex pagination

**Risks:**
- May scrape jobs from outside target area
- High maintenance
- May conflict with facility-specific LUX MED source

**Maintenance Cost:** High

**Recommendation:** Consider if we want national jobs or only local. May need location filtering in config.

---

## 8. https://polmed.pl/kariera/

**Classification:** Medical network / corporate careers  
**Type:** Corporate (Polmed - private healthcare network)  
**Difficulty:** High  
**City:** Multiple (national portal)

**Analysis:**
- Large corporate career portal
- Likely JavaScript-heavy
- Multiple locations
- Complex structure

**Proposed Config:**
```json
{
  "sourceId": "polmed",
  "sourceName": "Polmed",
  "baseUrl": "https://polmed.pl/kariera/",
  "city": "Multiple",  // Extract from each job
  "facilityName": "Polmed",
  "selectors": {
    "jobListContainer": "TBD",
    "jobItem": "TBD",
    "title": "TBD",
    "link": "TBD"
  },
  "metadata": {
    "confidence": "LOW",
    "notes": "Corporate portal - multiple cities. May need location filtering to focus on Gdańsk area.",
    "requiresPlaywright": true,
    "needsReview": true
  }
}
```

**Edge Cases:**
- Multiple cities
- May need location filtering
- Complex pagination
- AJAX loading

**Risks:**
- May scrape irrelevant locations
- High maintenance

**Maintenance Cost:** High

---

## 9. https://ogloszenia.trojmiasto.pl/praca-zatrudnie/sluzba-zdrowia/

**Classification:** ⚠️ External job aggregator (CRITICAL DIFFERENCE)  
**Type:** Third-party job board (Trojmiasto.pl - regional portal)  
**Difficulty:** Very High  
**City:** Multiple (Trojmiasto = Gdańsk/Gdynia/Sopot region)

**Analysis:**
- This is NOT a medical facility website
- It's a regional job aggregator/classifieds site
- Shows jobs from MULTIPLE employers
- Jobs may be posted by various facilities/clinics
- Structure likely complex and dynamic
- May have rate limiting
- May have terms of service restrictions

**Proposed Config:**
```json
{
  "sourceId": "trojmiasto_sluzba_zdrowia",
  "sourceName": "Trojmiasto.pl - Służba Zdrowia",
  "baseUrl": "https://ogloszenia.trojmiasto.pl/praca-zatrudnie/sluzba-zdrowia/",
  "city": "Multiple",  // Gdańsk/Gdynia/Sopot region
  "facilityName": "Various",  // Multiple employers
  "selectors": {
    "jobListContainer": "TBD",
    "jobItem": "TBD",
    "title": "TBD",
    "link": "TBD"
  },
  "metadata": {
    "confidence": "LOW",
    "notes": "EXTERNAL AGGREGATOR - Not a medical facility. Jobs from multiple employers. May have ToS restrictions. Complex structure. High maintenance risk.",
    "requiresPlaywright": true,
    "needsReview": true,
    "isAggregator": true,
    "warning": "This source differs fundamentally from others - it's a job board, not a facility site"
  }
}
```

### ⚠️ Special Considerations for Trojmiasto.pl:

**How it differs:**
1. **Multiple employers:** Each job is from a different facility/clinic
2. **External links:** Jobs may link to external employer sites
3. **Temporary listings:** Jobs may expire or be removed by employers
4. **Rate limiting:** Aggregators often have anti-scraping measures
5. **Terms of Service:** May prohibit automated scraping
6. **Pagination:** Likely complex (infinite scroll or AJAX)

**How to safely scrape:**
1. **Respect robots.txt:** Check before scraping
2. **Rate limiting:** Add delays between requests
3. **User-Agent:** Use proper identification
4. **Error handling:** Expect more failures
5. **Deduplication:** Jobs may appear on multiple sources
6. **Facility name extraction:** Must extract from job content, not config

**Limitations:**
- Cannot reliably detect "removed" jobs (employer may remove, not site)
- Facility names vary per job
- May have duplicate jobs from other sources
- Higher false positive rate for "removed" offers
- May need manual review of scraped jobs

**Refresh compatibility concerns:**
- ❌ Removal detection unreliable (employer removes, not site)
- ⚠️ Facility name varies per job (cannot use static config)
- ⚠️ May conflict with direct facility sources (duplicates)
- ⚠️ Higher maintenance burden

**Recommendation:** 
- Consider marking as "experimental"
- May want to exclude from automatic refresh or use different refresh logic
- Consider manual review of jobs from this source

**Maintenance Cost:** Very High

---

## Summary Table

| Source | Type | Difficulty | Confidence | Plug & Play? | Maintenance |
|--------|------|------------|------------|--------------|-------------|
| etermed.pl | Facility | Medium | Medium | ✅ Yes | Low |
| szpitalpolanki.pl | Facility | Low-Medium | Medium | ✅ Yes | Low |
| przychodniawitomino.pl | Facility | Low-Medium | Medium | ✅ Yes | Low |
| medicover.pl | Corporate | High | Low | ❌ No | High |
| pcrsopot.pl | Facility | Low-Medium | Medium | ✅ Yes | Low |
| szpital-gdansk.luxmed.pl | Corporate | N/A | N/A | ✅ Already exists | - |
| luxmed.pl | Corporate | High | Low | ❌ No | High |
| polmed.pl | Corporate | High | Low | ❌ No | High |
| trojmiasto.pl | **Aggregator** | **Very High** | **Low** | ❌ **No** | **Very High** |

---

## Recommendations

### Immediate Onboarding (Plug & Play):
1. ✅ **etermed.pl** - Standard facility page
2. ✅ **szpitalpolanki.pl** - Standard facility page  
3. ✅ **przychodniawitomino.pl** - Standard facility page
4. ✅ **pcrsopot.pl** - WordPress-style, straightforward

### Requires Manual Tuning:
5. ⚠️ **medicover.pl** - Complex corporate portal, may need multiple configs
6. ⚠️ **luxmed.pl** - Corporate portal, location filtering needed
7. ⚠️ **polmed.pl** - Corporate portal, location filtering needed

### Special Case (Requires Discussion):
8. ⚠️⚠️ **trojmiasto.pl** - External aggregator, fundamentally different
   - **Recommendation:** Discuss if we want aggregator sources
   - If yes, may need special handling in refresh logic
   - Consider marking jobs with `isAggregator: true` flag

---

## Next Steps

1. **Confirm approach for aggregator** (trojmiasto.pl)
2. **Run auto-detection** on plug & play sources
3. **Manual review** of corporate portals
4. **Test refresh compatibility** for each source
5. **Document any special cases** in config metadata

---

## Questions for Review

1. Should we include aggregator sources (trojmiasto.pl)?
2. For corporate portals (medicover, luxmed, polmed), should we:
   - Filter to Gdańsk/Gdynia/Sopot only?
   - Accept all locations?
   - Create separate configs per location?
3. Should aggregator sources use different refresh logic (less aggressive removal detection)?

