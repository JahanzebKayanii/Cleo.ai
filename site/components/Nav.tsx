"use client";
import { useState } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";

function CleoLogo() {
  return (
    <svg viewBox="0 0 40 40" width="32" height="32" fill="none">
      <rect width="40" height="40" rx="10" fill="#0d0f14" />
      <rect x="11" y="14" width="4.5" height="12" rx="2.25" fill="#10b981" />
      <rect x="17.75" y="9" width="4.5" height="22" rx="2.25" fill="#10b981" />
      <rect x="24.5" y="14" width="4.5" height="12" rx="2.25" fill="#10b981" />
    </svg>
  );
}

const navLinkStyle: React.CSSProperties = {
  fontSize: 14,
  fontWeight: 600,
  color: "#555",
  textDecoration: "none",
  padding: "6px 14px",
  borderRadius: 999,
  transition: "color 0.15s",
  letterSpacing: "-0.01em",
};

export default function Nav() {
  const pathname = usePathname();
  const isHome = pathname === "/";
  const p = isHome ? "" : "/";
  const [menuOpen, setMenuOpen] = useState(false);

  const close = () => setMenuOpen(false);

  return (
    <>
      <nav
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          zIndex: 50,
          background: "rgba(255,255,255,0.92)",
          backdropFilter: "blur(16px)",
          WebkitBackdropFilter: "blur(16px)",
          borderBottom: "1px solid rgba(0,0,0,0.07)",
        }}
      >
        <div
          style={{
            maxWidth: 1160,
            margin: "0 auto",
            padding: "0 24px",
            height: 64,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <Link href="/" style={{ display: "flex", alignItems: "center", gap: 10, textDecoration: "none" }}>
            <CleoLogo />
            <span style={{ fontWeight: 800, fontSize: 17, letterSpacing: "-0.03em", color: "#111" }}>
              CleoVoice
            </span>
          </Link>

          {/* Desktop links */}
          <div className="r-nav-links" style={{ display: "flex", alignItems: "center", gap: 2 }}>
            <Link
              href="/about"
              style={{ ...navLinkStyle, color: pathname === "/about" ? "#10b981" : "#555", fontWeight: pathname === "/about" ? 700 : 600 }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#111")}
              onMouseLeave={(e) => (e.currentTarget.style.color = pathname === "/about" ? "#10b981" : "#555")}
            >
              About
            </Link>
            <Link
              href="/integrations"
              style={{ ...navLinkStyle, color: pathname === "/integrations" ? "#10b981" : "#555", fontWeight: pathname === "/integrations" ? 700 : 600 }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#111")}
              onMouseLeave={(e) => (e.currentTarget.style.color = pathname === "/integrations" ? "#10b981" : "#555")}
            >
              Integrations
            </Link>
            <a
              href={`${p}#pricing`}
              style={navLinkStyle}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#111")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#555")}
            >
              Pricing
            </a>
            <Link
              href="/demo"
              style={{ ...navLinkStyle, color: pathname === "/demo" ? "#10b981" : "#555", fontWeight: pathname === "/demo" ? 700 : 600 }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#111")}
              onMouseLeave={(e) => (e.currentTarget.style.color = pathname === "/demo" ? "#10b981" : "#555")}
            >
              Demo
            </Link>
            <a
              href="https://api.cleovoice.com/dashboard/"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                fontSize: 14, fontWeight: 700, color: "white", textDecoration: "none",
                padding: "8px 22px", borderRadius: 999, background: "#111",
                letterSpacing: "-0.02em", marginLeft: 6, transition: "opacity 0.15s, transform 0.15s",
              }}
              onMouseEnter={(e) => { e.currentTarget.style.opacity = "0.85"; e.currentTarget.style.transform = "translateY(-1px)"; }}
              onMouseLeave={(e) => { e.currentTarget.style.opacity = "1"; e.currentTarget.style.transform = "translateY(0)"; }}
            >
              Login
            </a>
          </div>

          {/* Hamburger — mobile only */}
          <button
            className="r-hamburger"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle menu"
            style={{
              display: "none",
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: 8,
              borderRadius: 8,
              color: "#111",
            }}
          >
            {menuOpen ? (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6l12 12" stroke="#111" strokeWidth="2.2" strokeLinecap="round" />
              </svg>
            ) : (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M4 6h16M4 12h16M4 18h16" stroke="#111" strokeWidth="2.2" strokeLinecap="round" />
              </svg>
            )}
          </button>
        </div>
      </nav>

      {/* Mobile menu — renders only when open */}
      {menuOpen && (
        <div
          className="r-mobile-menu"
          style={{
            position: "fixed", top: 64, left: 0, right: 0, zIndex: 49,
            background: "white", borderBottom: "1px solid rgba(0,0,0,0.08)",
            padding: "12px 16px 20px",
            flexDirection: "column", gap: 2,
          }}
        >
          {[
            { label: "About", href: "/about", internal: true },
            { label: "Integrations", href: "/integrations", internal: true },
            { label: "Pricing", href: `${p}#pricing`, internal: false },
            { label: "Demo", href: "/demo", internal: true },
          ].map((item) =>
            item.internal ? (
              <Link
                key={item.label}
                href={item.href}
                onClick={close}
                style={{
                  display: "block", padding: "11px 12px", borderRadius: 10,
                  fontSize: 15, fontWeight: 600, textDecoration: "none",
                  color: pathname === item.href ? "#10b981" : "#222",
                  background: pathname === item.href ? "rgba(16,185,129,0.07)" : "transparent",
                }}
              >
                {item.label}
              </Link>
            ) : (
              <a
                key={item.label}
                href={item.href}
                onClick={close}
                style={{
                  display: "block", padding: "11px 12px", borderRadius: 10,
                  fontSize: 15, fontWeight: 600, textDecoration: "none", color: "#222",
                }}
              >
                {item.label}
              </a>
            )
          )}
          <a
            href="https://api.cleovoice.com/dashboard/"
            target="_blank"
            rel="noopener noreferrer"
            onClick={close}
            style={{
              display: "block", marginTop: 8, padding: "13px 16px", borderRadius: 12,
              background: "#111", color: "white", textAlign: "center",
              fontSize: 15, fontWeight: 700, textDecoration: "none", letterSpacing: "-0.02em",
            }}
          >
            Login →
          </a>
        </div>
      )}
    </>
  );
}
