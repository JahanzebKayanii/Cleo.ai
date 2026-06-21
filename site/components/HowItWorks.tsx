"use client";
import { useEffect, useRef, useState } from "react";

const steps = [
  {
    n: "01",
    title: "Forward your number",
    desc: "Point your existing business line to Cleo — or get a new number instantly. No hardware, no rewiring, no IT team required.",
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.01 1.18 2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92v2z"/>
      </svg>
    ),
  },
  {
    n: "02",
    title: "Cleo learns your business",
    desc: "Tell Cleo your hours, services, pricing, and how you like calls handled. It reads your calendar in real time and follows your rules exactly.",
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>
      </svg>
    ),
  },
  {
    n: "03",
    title: "Go live in under an hour",
    desc: "Cleo picks up your first real call, books the job, syncs to your CRM, and sends the customer a confirmation text — all without you lifting a finger.",
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>
      </svg>
    ),
  },
];

export default function HowItWorks() {
  const ref = useRef<HTMLElement>(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setInView(true); obs.disconnect(); } },
      { threshold: 0.2 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  return (
    <section ref={ref} className="r-section" style={{
      margin: "0 12px 12px", borderRadius: 24,
      background: "white", padding: "80px 60px",
      border: "1px solid rgba(0,0,0,0.05)",
    }}>
      <div style={{ maxWidth: 1060, margin: "0 auto" }}>
        {/* Two-column header — headline left, kicker right — breaks the chip→H2→p formula */}
        <div className="r-why-header" style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", marginBottom: 64, gap: 32 }}>
          <div style={{ flex: "0 0 auto", maxWidth: 520 }}>
            <h2 style={{
              fontSize: "clamp(30px, 3.5vw, 48px)", fontWeight: 700,
              letterSpacing: "-0.04em", lineHeight: 1.06, color: "#111",
            }}>
              Up and running<br />before lunch.
            </h2>
          </div>
          <p style={{ fontSize: 16, color: "#666", lineHeight: 1.7, maxWidth: 300, textAlign: "right", flexShrink: 0 }}>
            No developers, no lengthy onboarding. Three steps and Cleo is live on your line.
          </p>
        </div>

        <div className="r-3col" style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 0, position: "relative" }}>
          {/* Animated connector line */}
          <div className="r-connector" style={{
            position: "absolute", top: 36, left: "16.5%", right: "16.5%", height: 1,
            background: "rgba(16,185,129,0.15)", zIndex: 0,
            overflow: "hidden",
          }}>
            <div style={{
              position: "absolute", inset: 0,
              background: "linear-gradient(to right, #10b981, rgba(16,185,129,0.4))",
              transformOrigin: "left center",
              transform: inView ? "scaleX(1)" : "scaleX(0)",
              transition: "transform 1.1s cubic-bezier(0.22,1,0.36,1) 0.3s",
            }} />
          </div>

          {steps.map((step, i) => (
            <div key={step.n} className="r-step-col" style={{
              display: "flex", flexDirection: "column", alignItems: "center",
              textAlign: "center", padding: "0 40px",
              borderRight: i < 2 ? "1px solid rgba(0,0,0,0.05)" : "none",
              borderBottom: 0,
              position: "relative", zIndex: 1,
              opacity: inView ? 1 : 0,
              transform: inView ? "translateY(0)" : "translateY(16px)",
              transition: `opacity 0.5s ease ${0.15 + i * 0.15}s, transform 0.5s ease ${0.15 + i * 0.15}s`,
            }}>
              {/* Pulsing icon circle */}
              <div style={{
                width: 72, height: 72, borderRadius: "50%",
                background: "white",
                border: "1.5px solid rgba(16,185,129,0.3)",
                boxShadow: "0 4px 16px rgba(0,0,0,0.06)",
                display: "flex", alignItems: "center", justifyContent: "center",
                marginBottom: 28, flexShrink: 0,
                animation: inView ? `ringPulse 2.2s ease-out ${0.6 + i * 0.3}s infinite` : "none",
              }}>
                {step.icon}
              </div>

              <div style={{
                fontSize: 11, fontWeight: 700, letterSpacing: "0.1em",
                color: "#10b981", marginBottom: 10, textTransform: "uppercase",
              }}>
                Step {step.n}
              </div>
              <h3 style={{
                fontSize: 18, fontWeight: 700, color: "#111",
                letterSpacing: "-0.03em", marginBottom: 12, lineHeight: 1.25,
              }}>
                {step.title}
              </h3>
              <p style={{ fontSize: 14, color: "#555", lineHeight: 1.7 }}>
                {step.desc}
              </p>
            </div>
          ))}
        </div>

        {/* Bottom CTA strip */}
        <div style={{
          marginTop: 56, padding: "24px 32px", borderRadius: 16,
          background: "#f7f6f2", border: "1px solid rgba(0,0,0,0.05)",
          display: "flex", alignItems: "center", justifyContent: "space-between",
          flexWrap: "wrap", gap: 16,
          opacity: inView ? 1 : 0,
          transform: inView ? "translateY(0)" : "translateY(10px)",
          transition: "opacity 0.5s ease 0.7s, transform 0.5s ease 0.7s",
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 24, flexWrap: "wrap" }}>
            {["No hardware required", "Keep your existing number", "Cancel any time"].map((item) => (
              <div key={item} style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <circle cx="7" cy="7" r="7" fill="rgba(16,185,129,0.12)" />
                  <path d="M4 7l2 2 4-4" stroke="#10b981" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <span style={{ fontSize: 13, fontWeight: 600, color: "#444" }}>{item}</span>
              </div>
            ))}
          </div>
          <a href="#demo" style={{
            display: "inline-flex", alignItems: "center", gap: 6,
            padding: "10px 22px", borderRadius: 999,
            background: "#111", color: "white",
            fontWeight: 700, fontSize: 13.5, letterSpacing: "-0.02em",
            textDecoration: "none",
          }}>
            Get started →
          </a>
        </div>
      </div>
    </section>
  );
}
