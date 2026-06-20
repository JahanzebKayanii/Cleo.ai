"use client";
import { useEffect, useRef, useState } from "react";

const stories = [
  {
    quote: "We were missing 8 to 10 calls every weekend — customers would call a competitor before Monday. First week with Cleo we booked 3 jobs we would have lost.",
    metricTarget: 3,
    metricSuffix: " jobs",
    metricLabel: "booked first week",
    name: "Mike Johnson",
    business: "Johnson HVAC",
    trade: "HVAC",
    location: "Austin, TX",
    initial: "MJ",
    color: "#0d9488",
  },
  {
    quote: "Emergency calls at 2am used to go straight to voicemail. Customers wouldn't leave a message — they'd just call the next guy. Cleo handles them now and pages me when it's a real emergency.",
    metricTarget: 0,
    metricSuffix: "",
    metricLabel: "emergency calls missed",
    name: "Carlos Rivera",
    business: "Rivera Plumbing",
    trade: "Plumbing",
    location: "Dallas, TX",
    initial: "CR",
    color: "#0284c7",
  },
  {
    quote: "I set it up on a Thursday afternoon. Friday morning I had a booking confirmation in my inbox from a call I didn't even know happened. That was it — I was sold.",
    metricTarget: null,
    metricDisplay: "< 1 hr",
    metricLabel: "to first booking",
    name: "Sarah Chen",
    business: "Elite Electrical",
    trade: "Electrical",
    location: "Houston, TX",
    initial: "SC",
    color: "#7c3aed",
  },
];

function CountUp({ target, suffix, duration = 900 }: { target: number; suffix: string; duration?: number }) {
  const [count, setCount] = useState(0);
  const startedRef = useRef(false);

  useEffect(() => {
    if (startedRef.current || target === 0) { setCount(target); return; }
    startedRef.current = true;
    const steps = 30;
    const stepTime = duration / steps;
    let i = 0;
    const timer = setInterval(() => {
      i++;
      setCount(Math.round((i / steps) * target));
      if (i >= steps) clearInterval(timer);
    }, stepTime);
    return () => clearInterval(timer);
  }, [target, duration]);

  return <>{count}{suffix}</>;
}

export default function ContractorStories() {
  const ref = useRef<HTMLElement>(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setInView(true); obs.disconnect(); } },
      { threshold: 0.15 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  return (
    <section ref={ref} style={{
      margin: "0 12px 12px", borderRadius: 24,
      background: "#f0ede6", position: "relative", overflow: "hidden",
      padding: "80px 60px",
    }}>
      <div className="grain-overlay" style={{ position: "absolute", inset: 0, pointerEvents: "none", opacity: 0.45 }} />

      <div style={{ maxWidth: 1060, margin: "0 auto", position: "relative", zIndex: 1 }}>
        <div style={{ textAlign: "center", marginBottom: 56 }}>
          <span style={{
            fontSize: 11, fontWeight: 700, letterSpacing: "0.12em",
            textTransform: "uppercase", color: "#059669", display: "inline-block", marginBottom: 14,
          }}>
            Real results
          </span>
          <h2 style={{
            fontSize: "clamp(30px, 3.5vw, 48px)", fontWeight: 700,
            letterSpacing: "-0.04em", lineHeight: 1.06, color: "#111", marginBottom: 14,
          }}>
            It pays for itself after two jobs.
          </h2>
          <p style={{ fontSize: 16, color: "#666", maxWidth: 440, margin: "0 auto" }}>
            The average HVAC service call is worth $350. Cleo pays for itself after its first six bookings.
          </p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 14 }}>
          {stories.map((s, cardIdx) => (
            <div key={s.name} style={{
              background: "white", borderRadius: 20, padding: "32px 28px",
              border: "1px solid rgba(0,0,0,0.06)",
              boxShadow: "0 2px 12px rgba(0,0,0,0.05)",
              display: "flex", flexDirection: "column", justifyContent: "space-between",
              opacity: inView ? 1 : 0,
              transform: inView ? "translateY(0)" : "translateY(20px)",
              transition: `opacity 0.55s ease ${cardIdx * 0.12}s, transform 0.55s ease ${cardIdx * 0.12}s`,
            }}>
              <div>
                {/* Stars */}
                <div style={{ display: "flex", gap: 3, marginBottom: 18 }}>
                  {Array.from({ length: 5 }).map((_, i) => (
                    <svg key={i} width="14" height="14" viewBox="0 0 14 14" fill="#10b981"
                      style={{
                        opacity: inView ? 1 : 0,
                        transform: inView ? "scale(1)" : "scale(0.5)",
                        transition: `opacity 0.3s ease ${cardIdx * 0.12 + i * 0.06}s, transform 0.3s ease ${cardIdx * 0.12 + i * 0.06}s`,
                      }}
                    >
                      <path d="M7 1l1.6 3.3 3.6.5-2.6 2.5.6 3.6L7 9.3l-3.2 1.6.6-3.6L1.8 4.8l3.6-.5z" />
                    </svg>
                  ))}
                </div>

                <p style={{
                  fontSize: 14.5, color: "#333", lineHeight: 1.72,
                  fontStyle: "italic", marginBottom: 28,
                }}>
                  &ldquo;{s.quote}&rdquo;
                </p>
              </div>

              <div>
                {/* Key metric */}
                <div style={{
                  background: "#f7f6f2", borderRadius: 12, padding: "14px 18px",
                  marginBottom: 20, display: "flex", alignItems: "center", gap: 14,
                  border: "1px solid rgba(0,0,0,0.05)",
                }}>
                  <div style={{
                    fontSize: 28, fontWeight: 700, color: "#10b981",
                    letterSpacing: "-0.04em", lineHeight: 1,
                    minWidth: 48,
                  }}>
                    {inView ? (
                      s.metricTarget !== null
                        ? <CountUp target={s.metricTarget} suffix={s.metricSuffix ?? ""} />
                        : s.metricDisplay
                    ) : "—"}
                  </div>
                  <div style={{ fontSize: 12, color: "#888", fontWeight: 600, lineHeight: 1.4 }}>
                    {s.metricLabel}
                  </div>
                </div>

                {/* Person */}
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <div style={{
                    width: 40, height: 40, borderRadius: "50%", flexShrink: 0,
                    background: s.color,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 13, fontWeight: 700, color: "white", letterSpacing: "0.02em",
                  }}>
                    {s.initial}
                  </div>
                  <div>
                    <div style={{ fontSize: 13.5, fontWeight: 700, color: "#111", letterSpacing: "-0.02em" }}>
                      {s.name}
                    </div>
                    <div style={{ fontSize: 12, color: "#888", marginTop: 1 }}>
                      {s.business} · {s.location}
                    </div>
                  </div>
                  <div style={{ marginLeft: "auto", flexShrink: 0 }}>
                    <span style={{
                      fontSize: 11, fontWeight: 700, color: "#10b981",
                      background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.18)",
                      borderRadius: 999, padding: "3px 10px",
                    }}>
                      {s.trade}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
