import Nav from "@/components/Nav";

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

export default function About() {
  return (
    <>
      <Nav />

      {/* ── HERO ──────────────────────────────────────────────── */}
      <section style={{
        margin: "68px 12px 12px",
        borderRadius: 24,
        background: "#f7f6f2",
        padding: "100px 64px",
        textAlign: "center",
      }}>
        <p style={{
          fontSize: 11, fontWeight: 700, letterSpacing: "0.12em",
          textTransform: "uppercase", color: "#10b981", marginBottom: 20,
        }}>
          About CleoVoice
        </p>
        <h1 style={{
          fontSize: "clamp(38px, 5vw, 68px)", fontWeight: 700,
          letterSpacing: "-0.04em", lineHeight: 1.05, color: "#0a0a0a",
          maxWidth: 760, margin: "0 auto 28px",
        }}>
          Building AI that actually<br />earns its keep.
        </h1>
        <p style={{
          fontSize: 18, color: "#555", lineHeight: 1.75,
          maxWidth: 540, margin: "0 auto",
        }}>
          CleoVoice builds automation tools designed to eliminate repetitive work — so people can focus on the things that actually require a human.
        </p>
      </section>

      {/* ── FOUNDER ───────────────────────────────────────────── */}
      <section style={{
        margin: "0 12px 12px", borderRadius: 24,
        background: "white", padding: "80px 60px",
        border: "1px solid rgba(0,0,0,0.05)",
      }}>
        <div style={{ maxWidth: 1060, margin: "0 auto", display: "flex", alignItems: "flex-start", gap: 64, flexWrap: "wrap" }}>
          {/* Photo + identity */}
          <div style={{ flex: "0 0 auto" }}>
            <div style={{
              width: 200, height: 240, borderRadius: 20, overflow: "hidden",
              marginBottom: 20, boxShadow: "0 8px 32px rgba(0,0,0,0.12)",
            }}>
              <img
                src="/founder.jpeg"
                alt="Jahanzeb Kayani"
                style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "center top" }}
              />
            </div>
            <div style={{ fontSize: 16, fontWeight: 700, color: "#111", letterSpacing: "-0.02em" }}>Jahanzeb Kayani</div>
            <div style={{ fontSize: 13, color: "#10b981", fontWeight: 600, marginTop: 4 }}>Founder & Builder</div>
            <div style={{ fontSize: 12.5, color: "#888", marginTop: 4 }}>Tampa, Florida</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 8, marginTop: 16 }}>
              <a href="https://github.com/jahanzebkayani" target="_blank" rel="noopener noreferrer" style={{
                display: "flex", alignItems: "center", gap: 8,
                fontSize: 13, color: "#555", textDecoration: "none", fontWeight: 500,
              }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="#555">
                  <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
                </svg>
                GitHub
              </a>
              <a href="mailto:jahanzeb2005@gmail.com" style={{
                display: "flex", alignItems: "center", gap: 8,
                fontSize: 13, color: "#555", textDecoration: "none", fontWeight: 500,
              }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#555" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
                </svg>
                Email
              </a>
              <a href="https://www.linkedin.com/in/jahanzebkayanii/" target="_blank" rel="noopener noreferrer" style={{
                display: "flex", alignItems: "center", gap: 8,
                fontSize: 13, color: "#555", textDecoration: "none", fontWeight: 500,
              }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="#555">
                  <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/>
                </svg>
                LinkedIn
              </a>
            </div>
          </div>

          {/* Bio */}
          <div style={{ flex: "1 1 400px" }}>
            <h2 style={{
              fontSize: "clamp(28px, 3vw, 42px)", fontWeight: 700,
              letterSpacing: "-0.04em", lineHeight: 1.08, color: "#111",
              marginBottom: 28,
            }}>
              Built by someone who<br />cares about practical AI.
            </h2>
            <p style={{ fontSize: 16, color: "#555", lineHeight: 1.8, marginBottom: 18 }}>
              AI grabbed my attention early and never really let go. Not the hype around it, but the actual, practical question of what it can do when you point it at a real problem.
            </p>
            <p style={{ fontSize: 16, color: "#555", lineHeight: 1.8, marginBottom: 18 }}>
              Cleo is what came out of that. A voice receptionist built for home service businesses — the kind where the phone rings constantly and every missed call is a job that goes to someone else. It answers every call, books the appointment, and syncs to the CRM. No humans required.
            </p>
            <p style={{ fontSize: 16, color: "#555", lineHeight: 1.8 }}>
              I grew up seeing firsthand what a difference access to the right technology makes. Good tools are unevenly distributed, and I think AI is the best shot we&apos;ve had in a long time to fix that. That&apos;s the thing that keeps me building.
            </p>
          </div>
        </div>
      </section>

      {/* ── CTA ───────────────────────────────────────────────── */}
      <section style={{
        margin: "0 12px 12px", borderRadius: 24,
        background: "#0a0a0a", padding: "96px 60px",
        textAlign: "center",
      }}>
        <p style={{
          fontSize: 11, fontWeight: 700, letterSpacing: "0.12em",
          textTransform: "uppercase", color: "#10b981", marginBottom: 20,
        }}>
          Ready to see Cleo in action?
        </p>
        <h2 style={{
          fontSize: "clamp(30px, 3.5vw, 56px)", fontWeight: 700,
          letterSpacing: "-0.04em", lineHeight: 1.05, color: "white",
          marginBottom: 20,
        }}>
          Live in under an hour.
        </h2>
        <p style={{
          fontSize: 17, color: "rgba(255,255,255,0.45)", lineHeight: 1.7,
          maxWidth: 400, margin: "0 auto 40px",
        }}>
          No setup fee. No contract. Forward your number and Cleo answers the next call.
        </p>
        <a href="/#demo" style={{
          display: "inline-flex", alignItems: "center",
          padding: "16px 36px", borderRadius: 999,
          background: "#10b981", color: "white",
          fontWeight: 700, fontSize: 15,
          letterSpacing: "-0.02em", textDecoration: "none",
        }}>
          Request a Demo →
        </a>
      </section>

      {/* ── FOOTER ────────────────────────────────────────────── */}
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
            <div style={{ fontWeight: 700, fontSize: 15, color: "white", letterSpacing: "-0.03em" }}>
              CleoVoice
            </div>
          </div>
          <div style={{ display: "flex", gap: 24 }}>
            {[
              { label: "About",        href: "/about" },
              { label: "Integrations", href: "/integrations" },
              { label: "Pricing",      href: "/#pricing" },
              { label: "Get a Demo",   href: "/#demo" },
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
