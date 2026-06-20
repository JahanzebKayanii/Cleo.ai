"use client";
import { useState } from "react";

const trades = [
  {
    id: "hvac",
    label: "HVAC",
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 2v20M2 12h20M4.93 4.93l14.14 14.14M19.07 4.93L4.93 19.07"/>
      </svg>
    ),
    headline: "Never lose an HVAC job to voicemail again.",
    desc: "Cleo handles after-hours AC failures, peak-season overflow, and repeat customers — triaging urgency and booking the right slot every time.",
    stats: [
      { value: "94%", label: "Calls booked on first contact" },
      { value: "3m 18s", label: "Avg. call duration" },
      { value: "< 2s", label: "Time to answer" },
    ],
    actions: [
      { label: "Appointment booked to Google Calendar" },
      { label: "SMS confirmation sent to customer" },
      { label: "Job created in Jobber / Housecall Pro" },
      { label: "Urgency flag set for same-day calls" },
    ],
  },
  {
    id: "plumbing",
    label: "Plumbing",
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 12c0 1.1-.9 2-2 2s-2-.9-2-2 .9-2 2-2 2 .9 2 2z"/><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
      </svg>
    ),
    headline: "Handle plumbing emergencies at any hour.",
    desc: "Leak calls can't wait until morning. Cleo triages severity, dispatches urgent jobs, and captures every detail your tech needs before they arrive on site.",
    stats: [
      { value: "89%", label: "Emergency jobs dispatched same day" },
      { value: "2m 54s", label: "Avg. call duration" },
      { value: "0", label: "Calls sent to voicemail" },
    ],
    actions: [
      { label: "Severity assessed and documented" },
      { label: "On-call tech notified for emergencies" },
      { label: "Customer name and address captured" },
      { label: "CRM record created automatically" },
    ],
  },
  {
    id: "electrical",
    label: "Electrical",
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
      </svg>
    ),
    headline: "Book electrical jobs before competitors pick up.",
    desc: "Storm outages, tripped panels, and new installs all need fast response. Cleo qualifies the job, offers real open slots, and books without back-and-forth.",
    stats: [
      { value: "91%", label: "First-call booking rate" },
      { value: "3m 41s", label: "Avg. call duration" },
      { value: "24/7", label: "Always available" },
    ],
    actions: [
      { label: "Problem type and scope documented" },
      { label: "Live calendar checked before offering slot" },
      { label: "Appointment confirmed with customer" },
      { label: "Job synced to FieldEdge / ServiceTitan" },
    ],
  },
];

export default function VerticalSwitcher() {
  const [active, setActive] = useState(0);
  const [fading, setFading] = useState(false);
  const [animKey, setAnimKey] = useState(0);

  const switchTo = (idx: number) => {
    if (idx === active) return;
    setFading(true);
    setTimeout(() => {
      setActive(idx);
      setAnimKey(k => k + 1);
      setFading(false);
    }, 150);
  };

  const t = trades[active];

  return (
    <section id="see-it" className="r-section" style={{
      margin: "0 12px 12px",
      borderRadius: 24,
      background: "white",
      padding: "72px 60px",
      position: "relative",
      overflow: "hidden",
      border: "1px solid rgba(0,0,0,0.05)",
    }}>
      <div style={{ position: "absolute", top: -100, right: -80, width: 500, height: 500, borderRadius: "50%", background: "radial-gradient(circle, rgba(16,185,129,0.07) 0%, transparent 70%)", filter: "blur(70px)", pointerEvents: "none" }} />

      <div style={{ maxWidth: 1060, margin: "0 auto", position: "relative", zIndex: 1 }}>
        {/* Header + tabs */}
        <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", marginBottom: 44, flexWrap: "wrap", gap: 20 }}>
          <div>
            <div style={{ display: "inline-flex", alignItems: "center", border: "1px solid rgba(0,0,0,0.12)", borderRadius: 999, padding: "5px 14px", marginBottom: 14 }}>
              <span style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", color: "#555" }}>By trade</span>
            </div>
            <h2 style={{ fontSize: "clamp(28px, 3vw, 44px)", fontWeight: 700, letterSpacing: "-0.04em", lineHeight: 1.08, color: "#111" }}>
              Built for every home services trade.
            </h2>
          </div>

          <div className="r-tabs" style={{ display: "flex", gap: 6, background: "rgba(0,0,0,0.04)", borderRadius: 14, padding: 5, border: "1px solid rgba(0,0,0,0.06)" }}>
            {trades.map((trade, i) => (
              <button key={trade.id} onClick={() => switchTo(i)} style={{
                display: "flex", alignItems: "center", gap: 8,
                padding: "9px 20px", borderRadius: 10, border: "none",
                background: active === i ? "white" : "transparent",
                color: active === i ? "#111" : "#888",
                fontWeight: 700, fontSize: 14, letterSpacing: "-0.01em",
                cursor: "pointer",
                boxShadow: active === i ? "0 1px 6px rgba(0,0,0,0.08), 0 2px 16px rgba(0,0,0,0.05)" : "none",
                transition: "all 0.18s ease", fontFamily: "inherit",
              }}>
                <span style={{ color: active === i ? "#10b981" : "#bbb", display: "flex" }}>{trade.icon}</span>
                {trade.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="r-switcher" style={{
          display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16,
          opacity: fading ? 0 : 1, transform: fading ? "translateY(4px)" : "translateY(0)",
          transition: "opacity 0.15s ease, transform 0.15s ease",
        }}>
          {/* Left — headline, desc, stats */}
          <div style={{
            background: "#0d0f14", borderRadius: 20, padding: "40px 36px",
            border: "1px solid rgba(255,255,255,0.06)",
            boxShadow: "0 8px 32px rgba(0,0,0,0.18)",
            display: "flex", flexDirection: "column", justifyContent: "space-between",
          }}>
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 24 }}>
                <div style={{ width: 32, height: 32, borderRadius: 10, background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.25)", display: "flex", alignItems: "center", justifyContent: "center", color: "#10b981" }}>
                  {t.icon}
                </div>
                <span style={{ fontSize: 12, fontWeight: 700, color: "rgba(255,255,255,0.65)", letterSpacing: "0.06em", textTransform: "uppercase" }}>{t.label}</span>
              </div>
              <h3 style={{ fontSize: 24, fontWeight: 700, color: "white", letterSpacing: "-0.03em", lineHeight: 1.25, marginBottom: 14 }}>
                {t.headline}
              </h3>
              <p style={{ fontSize: 14, color: "rgba(255,255,255,0.72)", lineHeight: 1.7 }}>
                {t.desc}
              </p>
            </div>

            {/* Stats row */}
            <div style={{ display: "flex", gap: 0, marginTop: 36, borderTop: "1px solid rgba(255,255,255,0.07)", paddingTop: 28 }}>
              {t.stats.map((stat, i) => (
                <div key={stat.label} style={{
                  flex: 1, textAlign: "center",
                  borderRight: i < t.stats.length - 1 ? "1px solid rgba(255,255,255,0.07)" : "none",
                  padding: "0 12px",
                }}>
                  <div
                    key={`${animKey}-${i}`}
                    style={{
                      fontSize: 26, fontWeight: 700, color: "#10b981",
                      letterSpacing: "-0.04em", lineHeight: 1,
                      animation: `statPop 0.4s cubic-bezier(0.22,1,0.36,1) ${i * 60}ms both`,
                    }}
                  >
                    {stat.value}
                  </div>
                  <div style={{ fontSize: 11, color: "rgba(255,255,255,0.62)", marginTop: 6, lineHeight: 1.4 }}>{stat.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Right — what Cleo does after booking */}
          <div style={{
            background: "white", borderRadius: 20, padding: "40px 36px",
            border: "1px solid rgba(0,0,0,0.06)",
            boxShadow: "0 4px 16px rgba(0,0,0,0.05)",
            display: "flex", flexDirection: "column",
          }}>
            <h3 style={{ fontSize: 20, fontWeight: 700, color: "#111", letterSpacing: "-0.03em", marginBottom: 6 }}>
              What happens after Cleo books.
            </h3>
            <p style={{ fontSize: 13.5, color: "#999", lineHeight: 1.65, marginBottom: 28 }}>
              The call ends — Cleo keeps working. Every action is automated, every system is updated.
            </p>

            <div style={{ display: "flex", flexDirection: "column", gap: 10, flex: 1 }}>
              {t.actions.map((action, i) => (
                <div
                  key={`${animKey}-action-${i}`}
                  style={{
                    display: "flex", alignItems: "center", gap: 14,
                    padding: "16px 18px", borderRadius: 14,
                    background: "#f9f9f9", border: "1px solid rgba(0,0,0,0.05)",
                    animation: `slideUp 0.35s cubic-bezier(0.22,1,0.36,1) ${i * 70}ms both`,
                  }}
                >
                  <div style={{
                    width: 28, height: 28, borderRadius: 8, flexShrink: 0,
                    background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.2)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 12, fontWeight: 700, color: "#10b981",
                  }}>
                    {i + 1}
                  </div>
                  <span style={{ fontSize: 14, fontWeight: 600, color: "#333", letterSpacing: "-0.01em" }}>{action.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
