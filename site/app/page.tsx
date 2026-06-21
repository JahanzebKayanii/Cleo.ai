import Nav from "@/components/Nav";
import Reveal from "@/components/Reveal";
import AudioDemoSection from "@/components/AudioDemoSection";
import VerticalSwitcher from "@/components/VerticalSwitcher";
import PricingSection from "@/components/PricingSection";
import FAQSection from "@/components/FAQSection";
import HeroBackground from "@/components/HeroBackground";
import WhyCleo from "@/components/WhyCleo";

function CleoLogo() {
  return (
    <svg viewBox="0 0 40 40" width="30" height="30" fill="none">
      <rect width="40" height="40" rx="10" fill="#0d0f14" />
      <rect x="11" y="14" width="4.5" height="12" rx="2.25" fill="#10b981" />
      <rect x="17.75" y="9" width="4.5" height="22" rx="2.25" fill="#10b981" />
      <rect x="24.5" y="14" width="4.5" height="12" rx="2.25" fill="#10b981" />
    </svg>
  );
}


export default function Home() {
  return (
    <>
      <Nav />

      {/* ── HERO ────────────────────────────────────────────── */}
      <section className="r-hero" style={{
        margin: "68px 12px 12px",
        borderRadius: 24,
        background: "#f7f6f2",
        minHeight: "calc(90vh - 80px)",
        position: "relative",
        overflow: "hidden",
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 0,
        alignItems: "center",
        padding: "80px 64px",
      }}>
        {/* Animated canvas background */}
        <HeroBackground />

        {/* Left-edge fade so text stays legible */}
        <div style={{
          position: "absolute", inset: 0, pointerEvents: "none",
          background: "linear-gradient(to right, #f7f6f2 18%, transparent 52%)",
        }} />

        {/* Left — copy */}
        <div style={{ position: "relative", zIndex: 1, maxWidth: 560 }}>
          <h1 style={{
            fontSize: "clamp(42px, 4.8vw, 72px)", fontWeight: 700,
            letterSpacing: "-0.04em", lineHeight: 1.0,
            color: "#0a0a0a", marginBottom: 24,
          }}>
            Every call<br />answered.<br />
            <span style={{ color: "#10b981" }}>Every job booked.</span>
          </h1>

          <p style={{
            fontSize: 17, color: "#666", lineHeight: 1.7,
            maxWidth: 440, marginBottom: 40, fontWeight: 400,
          }}>
            Cleo is a 24/7 AI receptionist built for HVAC, plumbing, and electrical contractors. It picks up every call, books confirmed appointments, and syncs to your CRM.
          </p>

          <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 32 }}>
            <a href="/demo" style={{
              display: "inline-flex", alignItems: "center",
              padding: "14px 28px", borderRadius: 999,
              background: "#0a0a0a", color: "white",
              fontWeight: 700, fontSize: 15,
              letterSpacing: "-0.02em", textDecoration: "none",
            }}>
              Request a Demo →
            </a>
            <a href="#see-it" style={{
              display: "inline-flex", alignItems: "center",
              padding: "14px 24px", borderRadius: 999,
              border: "1.5px solid rgba(0,0,0,0.15)",
              color: "#333", fontWeight: 600, fontSize: 15,
              letterSpacing: "-0.01em", textDecoration: "none",
            }}>
              Hear a live call
            </a>
          </div>

          <p style={{ fontSize: 12.5, color: "#777" }}>
            No setup fee · No contract · Live in under an hour
          </p>
        </div>

        {/* Right — live call mockup */}
        <div className="r-hide" style={{ display: "flex", justifyContent: "center", alignItems: "center", position: "relative", zIndex: 1 }}>
          <div style={{
            width: "100%", maxWidth: 400,
            background: "#0d0f14",
            borderRadius: 24,
            padding: "28px 28px",
            boxShadow: "0 32px 80px rgba(0,0,0,0.18), 0 8px 24px rgba(0,0,0,0.1)",
            border: "1px solid rgba(255,255,255,0.06)",
          }}>
            {/* Header */}
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 24 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ position: "relative" }}>
                  <div style={{
                    width: 38, height: 38, borderRadius: 12,
                    background: "#10b981",
                    display: "flex", alignItems: "center", justifyContent: "center",
                  }}>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                      <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.01 1.18 2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92v2z" stroke="white" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <div style={{
                    position: "absolute", bottom: -2, right: -2,
                    width: 10, height: 10, borderRadius: "50%",
                    background: "#10b981", border: "2px solid #0d0f14",
                  }} />
                </div>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: "white", letterSpacing: "-0.02em" }}>Cleo</div>
                  <div style={{ fontSize: 11, color: "#10b981", fontWeight: 600 }}>● Live</div>
                </div>
              </div>
              <div style={{
                fontSize: 11, fontWeight: 600, color: "rgba(255,255,255,0.65)",
                background: "rgba(255,255,255,0.07)", borderRadius: 999, padding: "4px 10px",
              }}>
                Inbound Call
              </div>
            </div>

            {/* Caller */}
            <div style={{
              background: "rgba(255,255,255,0.04)", borderRadius: 14, padding: "14px 16px", marginBottom: 18,
              border: "1px solid rgba(255,255,255,0.06)",
            }}>
              <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)", fontWeight: 600, marginBottom: 4, letterSpacing: "0.04em", textTransform: "uppercase" }}>Caller</div>
              <div style={{ fontSize: 15, fontWeight: 700, color: "white", letterSpacing: "-0.02em" }}>Mike Reynolds</div>
              <div style={{ fontSize: 12, color: "rgba(255,255,255,0.45)", marginTop: 2 }}>HVAC Emergency · Austin, TX</div>
            </div>

            {/* Waveform */}
            <div style={{ display: "flex", alignItems: "center", gap: 2.5, height: 40, marginBottom: 18 }}>
              {Array.from({ length: 48 }, (_, i) => {
                const h = Math.max(4, Math.round(Math.abs(Math.sin(i * 0.42) * 16 + Math.sin(i * 0.85) * 10 + 6)));
                return (
                  <div key={i} style={{
                    flex: 1, height: `${Math.min(h, 36)}px`, borderRadius: 2,
                    background: i < 28 ? "#10b981" : "rgba(255,255,255,0.12)",
                    animationName: "wavePulse",
                    animationDuration: `${0.6 + (i % 7) * 0.1}s`,
                    animationTimingFunction: "ease-in-out",
                    animationIterationCount: "infinite",
                    animationDirection: "alternate",
                    animationDelay: `${(i * 0.04) % 0.9}s`,
                  }} />
                );
              })}
            </div>

            {/* Conversation */}
            <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 18 }}>
              {[
                { from: "caller", text: "My AC stopped working — it's 95° out." },
                { from: "cleo",   text: "I'll get a tech out today. What's your address?" },
                { from: "caller", text: "214 Maple Drive, Round Rock." },
                { from: "cleo",   text: "Booked — tech arrives 2–4 PM. You'll get a text." },
              ].map((msg, i) => (
                <div key={i} style={{ display: "flex", justifyContent: msg.from === "cleo" ? "flex-end" : "flex-start" }}>
                  <div style={{
                    padding: "8px 12px", borderRadius: 10, maxWidth: "82%",
                    background: msg.from === "cleo" ? "#10b981" : "rgba(255,255,255,0.08)",
                    fontSize: 12, fontWeight: 500, lineHeight: 1.5,
                    color: msg.from === "cleo" ? "white" : "rgba(255,255,255,0.75)",
                  }}>
                    {msg.text}
                  </div>
                </div>
              ))}
            </div>

            {/* Booking confirmation */}
            <div style={{
              background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.25)",
              borderRadius: 12, padding: "12px 16px",
              display: "flex", alignItems: "center", gap: 10,
            }}>
              <div style={{
                width: 28, height: 28, borderRadius: 8, background: "rgba(16,185,129,0.2)",
                display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
              }}>
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M2 7l3.5 3.5 6.5-7" stroke="#10b981" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#10b981", letterSpacing: "-0.01em" }}>Appointment Booked</div>
                <div style={{ fontSize: 11, color: "rgba(255,255,255,0.45)", marginTop: 1 }}>Today · 2:00–4:00 PM · CRM synced</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── PROOF STRIP ─────────────────────────────────────── */}
      <Reveal>
        <div style={{
          margin: "0 12px 12px", borderRadius: 16,
          background: "white", padding: "0 48px",
          border: "1px solid rgba(0,0,0,0.05)",
        }}>
          <div className="r-4col" style={{
            display: "grid", gridTemplateColumns: "repeat(4, 1fr)",
            maxWidth: 860, margin: "0 auto",
          }}>
            {[
              { value: "24/7", label: "Always answering" },
              { value: "< 2s", label: "Call pickup time" },
              { value: "3", label: "CRM integrations live" },
              { value: "$0", label: "Setup fee" },
            ].map((item, i) => (
              <div key={i} style={{
                padding: "26px 0",
                borderRight: i < 3 ? "1px solid rgba(0,0,0,0.07)" : "none",
                textAlign: "center",
              }}>
                <div style={{ fontSize: 26, fontWeight: 700, color: "#10b981", letterSpacing: "-0.04em", lineHeight: 1 }}>
                  {item.value}
                </div>
                <div style={{ fontSize: 12, fontWeight: 600, color: "#666", marginTop: 4, letterSpacing: "-0.01em" }}>
                  {item.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </Reveal>

      {/* ── AUDIO DEMO ──────────────────────────────────────── */}
      <AudioDemoSection />

      {/* ── TRUST STRIP ─────────────────────────────────────── */}
      <Reveal>
        <div className="r-trust" style={{
          margin: "0 12px 12px", borderRadius: 16,
          background: "#0d0f14", padding: "16px 48px",
          display: "flex", alignItems: "center", justifyContent: "center",
          gap: 0, flexWrap: "wrap",
        }}>
          {[
            {
              label: "256-bit encryption",
              icon: <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.45)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>,
            },
            {
              label: "Hosted on AWS",
              icon: <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.45)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 10h-1.26A8 8 0 109 20h9a5 5 0 000-10z"/></svg>,
            },
            {
              label: "Built on Twilio",
              icon: <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.45)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.01 1.18 2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92v2z"/></svg>,
            },
            {
              label: "99.9% uptime",
              icon: <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.45)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>,
            },
            {
              label: "No contracts",
              icon: <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.45)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="15" x2="15" y2="15"/></svg>,
            },
          ].map((item, i) => (
            <div key={item.label} className="r-trust-item" style={{
              display: "flex", alignItems: "center", gap: 8,
              padding: "8px 28px",
              borderRight: i < 4 ? "1px solid rgba(255,255,255,0.08)" : "none",
            }}>
              {item.icon}
              <span style={{ fontSize: 12.5, fontWeight: 600, color: "rgba(255,255,255,0.7)", letterSpacing: "-0.01em" }}>
                {item.label}
              </span>
            </div>
          ))}
        </div>
      </Reveal>

      {/* ── VERTICAL SWITCHER ───────────────────────────────── */}
      <VerticalSwitcher />



      {/* ── WHY CLEO ─────────────────────────────────────────── */}
      <WhyCleo />

      {/* ── INTEGRATIONS MARQUEE ─────────────────────────────── */}
      <Reveal>
        <section style={{
          margin: "0 12px 12px", borderRadius: 24,
          background: "#080a0e", padding: "36px 0", overflow: "hidden",
        }}>
          <p style={{
            textAlign: "center", fontSize: 11, fontWeight: 700,
            letterSpacing: "0.12em", textTransform: "uppercase",
            color: "rgba(255,255,255,0.4)", marginBottom: 20,
          }}>
            Works with the tools you already use
          </p>
          <div style={{ display: "flex", overflow: "hidden" }}>
            <div className="animate-marquee" style={{ display: "flex", gap: 12, whiteSpace: "nowrap", willChange: "transform" }}>
              {[
                { name: "Jobber",            domain: "jobber.com" },
                { name: "HubSpot",           domain: "hubspot.com" },
                { name: "Housecall Pro",     domain: "housecallpro.com" },
                { name: "ServiceTitan",      domain: "servicetitan.com" },
                { name: "FieldEdge",         domain: "fieldedge.com" },
                { name: "Google Calendar",   domain: "calendar.google.com" },
                { name: "Workiz",            domain: "workiz.com" },
                { name: "Service Fusion",    domain: "servicefusion.com" },
                { name: "mHelpDesk",         domain: "mhelpdesk.com" },
                { name: "Commusoft",         domain: "commusoft.com" },
                { name: "QuickBooks",        domain: "quickbooks.com" },
                { name: "Xero",              domain: "xero.com" },
                { name: "Microsoft Outlook", domain: "outlook.com" },
                { name: "Calendly",          domain: "calendly.com" },
                { name: "Jobber",            domain: "jobber.com" },
                { name: "HubSpot",           domain: "hubspot.com" },
                { name: "Housecall Pro",     domain: "housecallpro.com" },
                { name: "ServiceTitan",      domain: "servicetitan.com" },
                { name: "FieldEdge",         domain: "fieldedge.com" },
                { name: "Google Calendar",   domain: "calendar.google.com" },
                { name: "Workiz",            domain: "workiz.com" },
                { name: "Service Fusion",    domain: "servicefusion.com" },
                { name: "mHelpDesk",         domain: "mhelpdesk.com" },
                { name: "Commusoft",         domain: "commusoft.com" },
                { name: "QuickBooks",        domain: "quickbooks.com" },
                { name: "Xero",              domain: "xero.com" },
                { name: "Microsoft Outlook", domain: "outlook.com" },
                { name: "Calendly",          domain: "calendly.com" },
              ].map((crm, i) => (
                <div key={i} style={{
                  display: "flex", alignItems: "center", gap: 10,
                  padding: "10px 22px", borderRadius: 999,
                  border: "1px solid rgba(255,255,255,0.08)",
                  background: "rgba(255,255,255,0.04)",
                  flexShrink: 0,
                }}>
                  <img
                    src={`https://www.google.com/s2/favicons?domain=${crm.domain}&sz=64`}
                    alt={crm.name}
                    width={18}
                    height={18}
                    style={{ objectFit: "contain" }}
                  />
                  <span style={{ fontSize: 13, fontWeight: 700, color: "rgba(255,255,255,0.7)", letterSpacing: "-0.01em" }}>
                    {crm.name}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>
      </Reveal>



      {/* ── PRICING ──────────────────────────────────────────── */}
      <PricingSection />


      {/* ── FAQ ──────────────────────────────────────────────── */}
      <FAQSection />

      {/* ── CTA ──────────────────────────────────────────────── */}
      <section style={{
        margin: "0 12px 12px", borderRadius: 24,
        background: "#f0ede6", padding: "96px 48px",
        textAlign: "center", position: "relative", overflow: "hidden",
      }}>
        <div className="grain-overlay" style={{ position: "absolute", inset: 0, pointerEvents: "none", opacity: 0.5 }} />
        <div style={{ position: "relative", zIndex: 1, maxWidth: 560, margin: "0 auto" }}>
          <span style={{
            display: "inline-block", fontSize: 11, fontWeight: 700,
            letterSpacing: "0.12em", textTransform: "uppercase",
            color: "#059669", marginBottom: 20,
          }}>
            Get started
          </span>
          <h2 style={{
            fontSize: "clamp(34px, 4vw, 54px)", fontWeight: 700,
            letterSpacing: "-0.04em", lineHeight: 1.05,
            color: "#111", margin: "0 0 20px",
          }}>
            Stop missing calls.<br />Start booking more jobs.
          </h2>
          <p style={{
            fontSize: 17, color: "#666",
            lineHeight: 1.65, marginBottom: 36,
          }}>
            See Cleo handle a real call in a 15-minute live walkthrough. No slides, no pitch decks — just the product.
          </p>
          <a href="/demo" style={{
            display: "inline-flex", alignItems: "center",
            padding: "16px 36px", borderRadius: 999,
            background: "#111", color: "white",
            fontWeight: 700, fontSize: 16,
            letterSpacing: "-0.02em", textDecoration: "none",
          }}>
            Request a Demo →
          </a>
          <p style={{ fontSize: 12.5, color: "rgba(0,0,0,0.35)", marginTop: 16 }}>
            No setup fee · No contract · Response within a few hours
          </p>
        </div>
      </section>

      {/* ── FOOTER ───────────────────────────────────────────── */}
      <footer style={{
        margin: "0 12px 12px", borderRadius: 24,
        background: "#111", padding: "44px 48px",
      }}>
        <div className="r-footer" style={{
          maxWidth: 960, margin: "0 auto",
          display: "flex", alignItems: "center", justifyContent: "space-between",
          flexWrap: "wrap", gap: 20,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <CleoLogo />
            <div>
              <div style={{ fontWeight: 700, fontSize: 15, color: "white", letterSpacing: "-0.03em" }}>CleoVoice</div>
            </div>
          </div>
          <div style={{ display: "flex", gap: 24 }}>
            {[
              { label: "Integrations", href: "/integrations" },
              { label: "Pricing",      href: "#pricing" },
              { label: "Request a Demo", href: "/demo" },
            ].map((link) => (
              <a key={link.label} href={link.href} className="footer-link">{link.label}</a>
            ))}
          </div>
          <div style={{ fontSize: 12, color: "rgba(255,255,255,0.45)", letterSpacing: "-0.01em" }}>
            © 2026 CleoVoice. All rights reserved.
          </div>
        </div>
      </footer>
    </>
  );
}
