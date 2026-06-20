"use client";
import { useEffect, useRef, useState } from "react";

const BAR_HEIGHTS = [12,15,13,18,20,22,19,25,28,32,30,36,40,44,48,52,58,62,68,75,80,88,95,100];

export default function WhyCleo() {
  const ref = useRef<HTMLElement>(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setInView(true); obs.disconnect(); } },
      { threshold: 0.1 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  return (
    <section
      ref={ref}
      className="r-section"
      style={{
        margin: "0 12px 12px", borderRadius: 24,
        background: "white", padding: "80px 60px",
        border: "1px solid rgba(0,0,0,0.05)",
        position: "relative", overflow: "hidden",
      }}
    >
      <div style={{ position: "absolute", top: -60, right: -100, width: 480, height: 480, borderRadius: "50%", background: "radial-gradient(circle, rgba(16,185,129,0.06) 0%, transparent 70%)", filter: "blur(70px)", pointerEvents: "none" }} />

      <div style={{ maxWidth: 1060, margin: "0 auto", position: "relative" }}>

        {/* Left-aligned split header — breaks the centered chip→H2→p pattern */}
        <div
          className="r-why-header"
          style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", marginBottom: 52, gap: 32 }}
        >
          <div style={{ flex: "0 0 auto", maxWidth: 540 }}>
            <span style={{
              fontSize: 11, fontWeight: 700, letterSpacing: "0.12em",
              textTransform: "uppercase", color: "#059669",
              display: "block", marginBottom: 16,
            }}>
              Why Cleo
            </span>
            <h2 style={{
              fontSize: "clamp(32px, 4vw, 54px)", fontWeight: 700,
              letterSpacing: "-0.04em", lineHeight: 1.06, color: "#111",
            }}>
              The receptionist<br />that never clocks out.
            </h2>
          </div>
          <p style={{ fontSize: 16, color: "#666", lineHeight: 1.7, maxWidth: 320, textAlign: "right", flexShrink: 0 }}>
            Faster responses, more bookings, zero missed calls — without adding headcount.
          </p>
        </div>

        {/* Bento grid — clean white cards, no green gradient wrapper */}
        <div className="r-bento" style={{ display: "grid", gridTemplateColumns: "1fr 400px", gap: 12 }}>

          {/* ── Left column ── */}
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>

            {/* Bar chart card with scroll-triggered animation */}
            <div className="bento-card" style={{
              background: "white", borderRadius: 16, padding: "32px 32px",
              border: "1px solid rgba(0,0,0,0.07)",
              boxShadow: "0 2px 8px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05)",
              display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, alignItems: "flex-end",
            }}>
              <div>
                <h3 style={{ fontSize: 20, fontWeight: 700, color: "#111", letterSpacing: "-0.03em", marginBottom: 10 }}>
                  Booked. Every time.
                </h3>
                <p style={{ fontSize: 13.5, color: "#555", lineHeight: 1.7 }}>
                  Cleo checks your live calendar, finds a real open slot, and confirms the appointment in the same call — no back-and-forth.
                </p>
              </div>
              <div style={{ display: "flex", alignItems: "flex-end", gap: 4, height: 110 }}>
                {BAR_HEIGHTS.map((h, i) => (
                  <div key={i} style={{
                    flex: 1,
                    height: `${h}%`,
                    borderRadius: "3px 3px 0 0",
                    background: i >= 18 ? "#10b981" : `rgba(16,185,129,${0.15 + i * 0.035})`,
                    transformOrigin: "bottom center",
                    transform: inView ? "scaleY(1)" : "scaleY(0)",
                    transition: inView
                      ? `transform 0.55s cubic-bezier(0.22,1,0.36,1) ${0.04 + i * 0.022}s`
                      : "none",
                  }} />
                ))}
              </div>
            </div>

            {/* Full Visibility card */}
            <div className="bento-card" style={{
              background: "white", borderRadius: 16, padding: "32px 32px",
              border: "1px solid rgba(0,0,0,0.07)",
              boxShadow: "0 2px 8px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05)",
            }}>
              <div className="r-2col" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 28, alignItems: "start" }}>
                <div>
                  <h3 style={{ fontSize: 20, fontWeight: 700, color: "#111", letterSpacing: "-0.03em", marginBottom: 8 }}>
                    Full Visibility
                  </h3>
                  <p style={{ fontSize: 13.5, color: "#555", lineHeight: 1.7, marginBottom: 20 }}>
                    Every call is logged with a full transcript, AI summary, and CRM sync — so nothing falls through the cracks.
                  </p>
                  {[
                    { label: "Call transcript", desc: "Word-for-word record of every conversation" },
                    { label: "AI call summary", desc: "Issue, address, outcome — auto-generated" },
                    { label: "CRM entry created", desc: "Synced to Jobber, HubSpot, or Housecall Pro" },
                    { label: "SMS log attached", desc: "Confirmation sent and timestamped" },
                  ].map((item) => (
                    <div key={item.label} style={{ display: "flex", alignItems: "flex-start", gap: 10, marginBottom: 10 }}>
                      <div style={{
                        width: 18, height: 18, borderRadius: "50%",
                        background: "rgba(16,185,129,0.12)", border: "1px solid rgba(16,185,129,0.3)",
                        display: "flex", alignItems: "center", justifyContent: "center",
                        flexShrink: 0, marginTop: 1,
                      }}>
                        <svg width="9" height="9" viewBox="0 0 9 9" fill="none">
                          <path d="M1.5 4.5l2 2 4-4" stroke="#10b981" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      </div>
                      <div>
                        <span style={{ fontSize: 13, fontWeight: 700, color: "#222" }}>{item.label}</span>
                        <span style={{ fontSize: 12, color: "#777", marginLeft: 6 }}>{item.desc}</span>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Call log preview */}
                <div style={{ background: "#f7f8fa", borderRadius: 14, padding: "18px 18px", border: "1px solid rgba(0,0,0,0.05)" }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14, paddingBottom: 12, borderBottom: "1px solid rgba(0,0,0,0.06)" }}>
                    <div>
                      <div style={{ fontSize: 13, fontWeight: 700, color: "#111" }}>Jason Miller</div>
                      <div style={{ fontSize: 11, color: "#999", marginTop: 1 }}>HVAC · Today, 2:14 PM</div>
                    </div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#10b981", background: "rgba(16,185,129,0.1)", borderRadius: 999, padding: "3px 10px" }}>
                      Booked
                    </div>
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 14 }}>
                    {[
                      { label: "Issue",   value: "AC not cooling — unit 3 yrs old" },
                      { label: "Address", value: "4521 Oak St, Austin TX" },
                      { label: "Slot",    value: "Today 2:00–4:00 PM" },
                      { label: "CRM",     value: "Jobber — Job #4821 created" },
                      { label: "SMS",     value: "Confirmation sent ✓" },
                    ].map((row) => (
                      <div key={row.label} style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
                        <span style={{ fontSize: 11.5, color: "#888", flexShrink: 0 }}>{row.label}</span>
                        <span style={{ fontSize: 11.5, fontWeight: 600, color: "#333", textAlign: "right" }}>{row.value}</span>
                      </div>
                    ))}
                  </div>
                  <div style={{ background: "#eef9f5", borderRadius: 8, padding: "10px 12px", border: "1px solid rgba(16,185,129,0.15)" }}>
                    <div style={{ fontSize: 10, fontWeight: 700, color: "#10b981", letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: 4 }}>
                      AI Summary
                    </div>
                    <div style={{ fontSize: 11.5, color: "#555", lineHeight: 1.55 }}>
                      Homeowner reports AC stopped cooling. Unit is 3 years old, issue started this morning. Address confirmed. Booked for same-day slot.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* ── Right column ── */}
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>

            {/* Always On-Brand */}
            <div className="bento-card" style={{
              background: "white", borderRadius: 16, padding: "32px 28px", flex: 1,
              border: "1px solid rgba(0,0,0,0.07)",
              boxShadow: "0 2px 8px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05)",
            }}>
              <h3 style={{ fontSize: 20, fontWeight: 700, color: "#111", letterSpacing: "-0.03em", marginBottom: 10 }}>
                Always On-Brand
              </h3>
              <p style={{ fontSize: 13.5, color: "#555", lineHeight: 1.7, marginBottom: 24 }}>
                Cleo follows your approved scripts — no hallucinated responses, no off-brand replies.
              </p>
              <div style={{ display: "flex", flexDirection: "column", gap: 9 }}>
                {[
                  { label: "Approved Scripts", icon: <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg> },
                  { label: "Smart Routing",    icon: <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg> },
                  { label: "Live Transfer",    icon: <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.01 1.18 2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92v2z"/></svg> },
                  { label: "Call Transcripts", icon: <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg> },
                ].map((item) => (
                  <div key={item.label} style={{
                    display: "flex", alignItems: "center", justifyContent: "space-between",
                    padding: "10px 14px", borderRadius: 10,
                    background: "#f7f8fa", border: "1px solid rgba(0,0,0,0.05)",
                  }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                      <div style={{
                        width: 28, height: 28, borderRadius: 8,
                        background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.15)",
                        display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
                      }}>
                        {item.icon}
                      </div>
                      <span style={{ fontSize: 13, fontWeight: 600, color: "#333" }}>{item.label}</span>
                    </div>
                    <div style={{ width: 36, height: 20, borderRadius: 999, background: "#10b981", position: "relative", flexShrink: 0 }}>
                      <div style={{ position: "absolute", right: 3, top: 3, width: 14, height: 14, borderRadius: "50%", background: "white" }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Enterprise Reliability dark card */}
            <div style={{
              background: "#080a0e", borderRadius: 16, padding: "28px 28px",
              border: "1px solid rgba(16,185,129,0.15)",
            }}>
              <h3 style={{ fontSize: 16, fontWeight: 700, color: "white", letterSpacing: "-0.03em", marginBottom: 8 }}>
                Enterprise Reliability
              </h3>
              <p style={{ fontSize: 13, color: "rgba(255,255,255,0.7)", lineHeight: 1.65, marginBottom: 20 }}>
                Always-on infrastructure with instant failover — every call connected, every customer heard.
              </p>
              <div style={{ display: "flex", alignItems: "flex-end", gap: 3, height: 52, marginBottom: 14 }}>
                {Array.from({ length: 32 }, (_, i) => {
                  const h = 55 + Math.round(Math.sin(i * 0.7) * 20 + Math.sin(i * 1.3) * 15 + 10);
                  return (
                    <div key={i} style={{
                      flex: 1, borderRadius: "2px 2px 0 0",
                      height: `${Math.min(100, h)}%`,
                      background: "rgba(16,185,129,0.65)",
                    }} />
                  );
                })}
              </div>
              <div style={{ fontSize: 28, fontWeight: 700, color: "#10b981", letterSpacing: "-0.04em", lineHeight: 1 }}>
                99.9% Uptime
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
