# CleoVoice — Marketing Site

Marketing website for [CleoVoice](https://www.cleovoice.com), a 24/7 AI voice receptionist built for HVAC, plumbing, and electrical contractors.

Built with Next.js 15, Tailwind v4, and Space Grotesk. Deployed on Vercel.

## Pages

- `/` — Homepage (hero, how it works, pricing, demo form)
- `/about` — Founder story and mission
- `/integrations` — CRM and calendar integrations

## Stack

- **Framework:** Next.js 15 (App Router)
- **Styling:** Tailwind v4 + inline styles
- **Font:** Space Grotesk (Google Fonts)
- **Animations:** IntersectionObserver + CSS transitions

## Running locally

```bash
npm install
npm run dev
```

Runs on `http://localhost:3001` (port 3000 is reserved for the Cleo backend dashboard).

## Project structure

```
app/
  page.tsx          # Homepage
  about/page.tsx    # About page
  integrations/page.tsx
  layout.tsx
  globals.css
components/
  Nav.tsx
  HowItWorks.tsx
  WhyCleo.tsx
  AudioDemoSection.tsx
  VerticalSwitcher.tsx
  PricingSection.tsx
  FAQSection.tsx
  DemoForm.tsx
  HeroBackground.tsx
public/
  founder.jpeg
  audio/
```
