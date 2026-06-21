# Lead Demo Sites

**290+ responsive business demo websites deployed to GitHub Pages through automated CI/CD.**

A scaled website deployment pipeline: take a base template, customize it per business (name, phone, content, branding), verify the output, and deploy — all automated. Built as part of a larger lead generation system with scraper, auditor, and writer agents.

---

### What it is

A pipeline that produces production-ready business demo sites at scale. Each site is a responsive, single-page HTML/CSS/JS template customized for a specific business — dental clinics, local services, and small businesses.

### Scale

- **290+** sites deployed and live
- **Template-based** — one base design, per-business customization
- **Automated verification** — every deployment checked for HTTP 200, correct business name, and content integrity
- **GitHub Pages** hosting — zero infrastructure cost, global CDN

### Architecture

```
[Template] → [Customize per business] → [Audit] → [Deploy to GitHub Pages]
                                                           ↓
                                                    Live site live
```

The audit step catches template rot (leftover references from previous businesses), broken links, and content mismatches before anything goes live.

---

### Related

This project is one component of a larger multi-agent automation system. See [agentic-workflows](https://github.com/KevinPratap/agentic-workflows) for the full architecture.

### Tech

HTML5 · CSS3 · JavaScript · GitHub Pages · GitHub Actions · Python
