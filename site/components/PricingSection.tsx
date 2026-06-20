"use client";
import { useState, useEffect } from "react";

const plans = [
  {
    name: "Starter",
    monthly: 89,
    annual: 69,
    annualTotal: 828,
    monthlySaving: 20,
    yearlySaving: 240,
    desc: "For solo operators and small crews just getting started.",
    cta: "Get started",
    highlight: false,
    limits: "1 line · 150 calls/mo",
    features: [
      "1 phone line",
      "150 calls per month",
      "Appointment booking",
      "SMS confirmation after booking",
      "All integrations included",
      "Email call summaries",
      "Custom business instructions",
      "Email support",
    ],
    missing: [
      "Live call transfer",
      "Analytics dashboard",
      "Priority support",
    ],
  },
  {
    name: "Pro",
    monthly: 199,
    annual: 159,
    annualTotal: 1908,
    monthlySaving: 40,
    yearlySaving: 480,
    desc: "For 5–15 person shops that can't afford to miss a call.",
    cta: "Get started",
    highlight: true,
    limits: "3 lines · Unlimited calls",
    features: [
      "Up to 3 phone lines",
      "Unlimited calls",
      "Appointment booking",
      "SMS confirmation after booking",
      "All integrations included",
      "Email call summaries",
      "Custom business instructions",
      "Live call transfer",
      "Returning caller recognition",
      "Analytics dashboard",
      "Priority support",
    ],
    missing: [],
  },
  {
    name: "Business",
    monthly: 449,
    annual: 359,
    annualTotal: 4308,
    monthlySaving: 90,
    yearlySaving: 1080,
    desc: "For multi-location contractors who need full control.",
    cta: "Talk to us",
    highlight: false,
    limits: "Unlimited lines",
    features: [
      "Unlimited phone lines",
      "Unlimited calls",
      "Appointment booking",
      "SMS confirmation after booking",
      "All integrations included",
      "Email call summaries",
      "Custom instructions per location",
      "Live call transfer",
      "Returning caller recognition",
      "Advanced analytics & reporting",
      "Multi-location dashboard",
      "Dedicated account manager",
      "Custom onboarding",
    ],
    missing: [],
  },
];

function Check({ dim }: { dim?: boolean }) {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style={{ flexShrink: 0 }}>
      <circle cx="8" cy="8" r="8" fill={dim ? "rgba(255,255,255,0.06)" : "rgba(16,185,129,0.15)"} />
      <path d="M5 8l2.2 2.2 3.8-4.4" stroke={dim ? "rgba(255,255,255,0.2)" : "#10b981"} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function Cross() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style={{ flexShrink: 0 }}>
      <circle cx="8" cy="8" r="8" fill="rgba(0,0,0,0.04)" />
      <path d="M5.5 10.5l5-5M10.5 10.5l-5-5" stroke="#ccc" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

function AnimatedPrice({ value, isHighlight }: { value: number; isHighlight: boolean }) {
  const [display, setDisplay] = useState(value);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    setVisible(false);
    const t = setTimeout(() => {
      setDisplay(value);
      setVisible(true);
    }, 130);
    return () => clearTimeout(t);
  }, [value]);

  return (
    <span style={{
      fontSize: 52, fontWeight: 700, letterSpacing: "-0.05em", lineHeight: 1,
      color: isHighlight ? "white" : "#111",
      display: "inline-block",
      opacity: visible ? 1 : 0,
      transform: visible ? "translateY(0)" : "translateY(6px)",
      transition: "opacity 0.13s ease, transform 0.13s ease",
    }}>
      ${display}
    </span>
  );
}

export default function PricingSection() {
  const [annual, setAnnual] = useState(true);

  return (
    <section
      id="pricing"
      style={{
        margin: "0 12px 12px",
        borderRadius: 24,
        background: "#f0ede6",
        padding: "80px 48px",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <div className="grain-overlay" style={{ position: "absolute", inset: 0, pointerEvents: "none", opacity: 0.45 }} />
      <div style={{ maxWidth: 1060, margin: "0 auto", position: "relative", zIndex: 1 }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 48 }}>
          <span style={{
            display: "inline-block", fontSize: 11, fontWeight: 700,
            letterSpacing: "0.12em", textTransform: "uppercase", color: "#059669", marginBottom: 14,
          }}>
            Pricing
          </span>
          <h2 style={{
            fontSize: "clamp(34px, 4vw, 52px)", fontWeight: 700,
            letterSpacing: "-0.04em", lineHeight: 1.05, color: "#111", marginBottom: 14,
          }}>
            Plans that grow with your business.
          </h2>
          <p style={{ fontSize: 16, color: "#666", maxWidth: 420, margin: "0 auto" }}>
            No setup fees. No per-call charges. All integrations included on every plan.
          </p>

          {/* Toggle */}
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10, marginTop: 28 }}>
            <div style={{
              display: "inline-flex", alignItems: "center",
              background: "#e8e6e2", borderRadius: 999, padding: 4, gap: 2,
            }}>
              {["Monthly", "Annual"].map((label) => {
                const isAnnual = label === "Annual";
                const isActive = annual === isAnnual;
                return (
                  <button key={label} onClick={() => setAnnual(isAnnual)} style={{
                    padding: "9px 26px", borderRadius: 999, border: "none",
                    cursor: "pointer", fontWeight: 700, fontSize: 14,
                    letterSpacing: "-0.01em", fontFamily: "inherit",
                    transition: "all 0.2s ease",
                    background: isActive ? "white" : "transparent",
                    color: isActive ? "#111" : "#888",
                    boxShadow: isActive ? "0 1px 4px rgba(0,0,0,0.1)" : "none",
                  }}>
                    {label}
                  </button>
                );
              })}
            </div>

            {/* Annual savings callout */}
            <div style={{
              display: "flex", alignItems: "center", gap: 8,
              opacity: annual ? 1 : 0,
              transform: annual ? "translateY(0)" : "translateY(-4px)",
              transition: "opacity 0.2s ease, transform 0.2s ease",
              pointerEvents: "none",
            }}>
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M7 1l1.6 3.3 3.6.5-2.6 2.5.6 3.6L7 9.3l-3.2 1.6.6-3.6L1.8 4.8l3.6-.5z" fill="#10b981" />
              </svg>
              <span style={{ fontSize: 13, fontWeight: 600, color: "#059669" }}>
                Pay annually and get 2 months free — up to $1,080 saved per year
              </span>
            </div>
          </div>
        </div>

        {/* Cards */}
        <div className="r-pricing" style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 14, alignItems: "stretch" }}>
          {plans.map((plan) => {
            const price = annual ? plan.annual : plan.monthly;
            const isHighlight = plan.highlight;

            return (
              <div key={plan.name} style={{
                borderRadius: 20,
                background: isHighlight ? "#0d0f14" : "white",
                border: isHighlight ? "1px solid rgba(16,185,129,0.2)" : "1px solid rgba(0,0,0,0.07)",
                padding: "36px 32px",
                position: "relative",
                overflow: "hidden",
                display: "flex",
                flexDirection: "column",
                boxShadow: isHighlight
                  ? "0 8px 40px rgba(0,0,0,0.2), 0 0 0 1px rgba(16,185,129,0.15)"
                  : "0 2px 12px rgba(0,0,0,0.04)",
              }}>
                {/* Glow */}
                {isHighlight && (<>
                  <div style={{
                    position: "absolute", top: -60, right: -60, width: 280, height: 280,
                    borderRadius: "50%",
                    background: "radial-gradient(circle, rgba(16,185,129,0.14) 0%, transparent 70%)",
                    pointerEvents: "none",
                    animation: "glowDrift 8s ease-in-out infinite",
                  }} />
                  <div style={{
                    position: "absolute", bottom: -40, left: -40, width: 200, height: 200,
                    borderRadius: "50%",
                    background: "radial-gradient(circle, rgba(16,185,129,0.08) 0%, transparent 70%)",
                    pointerEvents: "none",
                    animation: "glowDrift 11s ease-in-out infinite reverse",
                  }} />
                </>)}

                {/* Most popular badge */}
                {isHighlight && (
                  <div style={{
                    position: "absolute", top: 20, right: 20,
                    background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.3)",
                    borderRadius: 999, padding: "4px 12px",
                    fontSize: 11, fontWeight: 700, color: "#34d399", letterSpacing: "0.04em",
                  }}>
                    Most popular
                  </div>
                )}

                <div style={{ position: "relative", zIndex: 1, display: "flex", flexDirection: "column", flex: 1 }}>
                  {/* Plan name + desc */}
                  <div style={{ marginBottom: 20 }}>
                    <div style={{
                      fontSize: 13, fontWeight: 700, letterSpacing: "-0.01em", marginBottom: 6,
                      color: isHighlight ? "rgba(255,255,255,0.65)" : "#555",
                    }}>
                      {plan.name}
                    </div>
                    <p style={{
                      fontSize: 13, lineHeight: 1.55,
                      color: isHighlight ? "rgba(255,255,255,0.62)" : "#666",
                    }}>
                      {plan.desc}
                    </p>
                  </div>

                  {/* Price */}
                  <div style={{ marginBottom: 4 }}>
                    {/* Strikethrough monthly when annual */}
                    <div style={{
                      height: 18, marginBottom: 2,
                      opacity: annual ? 1 : 0,
                      transition: "opacity 0.2s ease",
                    }}>
                      <span style={{
                        fontSize: 13, fontWeight: 600,
                        color: isHighlight ? "rgba(255,255,255,0.42)" : "#999",
                        textDecoration: "line-through",
                      }}>
                        ${plan.monthly}/mo
                      </span>
                    </div>

                    <div style={{ display: "flex", alignItems: "baseline", gap: 3 }}>
                      <AnimatedPrice value={price} isHighlight={isHighlight} />
                      <span style={{ fontSize: 15, color: isHighlight ? "rgba(255,255,255,0.55)" : "#888" }}>/mo</span>
                    </div>
                  </div>

                  <p style={{
                    fontSize: 12.5, marginBottom: 10,
                    color: isHighlight ? "rgba(255,255,255,0.52)" : "#888",
                  }}>
                    {annual ? `Billed annually · $${plan.annualTotal}/yr` : "Billed monthly · cancel any time"}
                  </p>

                  {/* Annual savings badge per card */}
                  <div style={{
                    display: "inline-flex", alignItems: "center", gap: 5, alignSelf: "flex-start",
                    marginBottom: 16,
                    opacity: annual ? 1 : 0,
                    transform: annual ? "translateY(0)" : "translateY(-3px)",
                    transition: "opacity 0.2s ease, transform 0.2s ease",
                  }}>
                    <div style={{
                      background: isHighlight ? "rgba(16,185,129,0.15)" : "rgba(16,185,129,0.08)",
                      border: isHighlight ? "1px solid rgba(16,185,129,0.3)" : "1px solid rgba(16,185,129,0.18)",
                      borderRadius: 999, padding: "3px 10px",
                      fontSize: 11.5, fontWeight: 700, color: "#10b981",
                    }}>
                      Save ${plan.yearlySaving}/yr
                    </div>
                  </div>

                  {/* Limits pill */}
                  <div style={{
                    display: "inline-flex", alignSelf: "flex-start",
                    background: isHighlight ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.04)",
                    border: isHighlight ? "1px solid rgba(255,255,255,0.08)" : "1px solid rgba(0,0,0,0.07)",
                    borderRadius: 999, padding: "4px 12px", marginBottom: 24,
                  }}>
                    <span style={{
                      fontSize: 11.5, fontWeight: 600,
                      color: isHighlight ? "rgba(255,255,255,0.62)" : "#666",
                    }}>
                      {plan.limits}
                    </span>
                  </div>

                  {/* CTA */}
                  <a href="#demo" style={{
                    display: "flex", alignItems: "center", justifyContent: "center",
                    gap: 6, width: "100%", padding: "13px 0", borderRadius: 12,
                    background: isHighlight ? "#10b981" : "#111",
                    color: "white", fontWeight: 700, fontSize: 14,
                    letterSpacing: "-0.02em", textDecoration: "none",
                    transition: "opacity 0.15s, transform 0.15s",
                    marginBottom: 24,
                  }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.opacity = "0.85";
                      e.currentTarget.style.transform = "translateY(-1px)";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.opacity = "1";
                      e.currentTarget.style.transform = "translateY(0)";
                    }}
                  >
                    {plan.cta}
                    <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
                      <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </a>

                  {/* Divider */}
                  <div style={{
                    height: 1, marginBottom: 20,
                    background: isHighlight ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.05)",
                  }} />

                  {/* Features */}
                  <div style={{ display: "flex", flexDirection: "column", gap: 9, flex: 1 }}>
                    {plan.features.map((f) => (
                      <div key={f} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <Check />
                        <span style={{
                          fontSize: 13.5, letterSpacing: "-0.01em",
                          color: isHighlight ? "rgba(255,255,255,0.65)" : "#444",
                        }}>{f}</span>
                      </div>
                    ))}
                    {plan.missing.map((f) => (
                      <div key={f} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <Cross />
                        <span style={{ fontSize: 13.5, letterSpacing: "-0.01em", color: "#999" }}>{f}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Bottom note */}
        <p style={{ textAlign: "center", marginTop: 28, fontSize: 13, color: "#666" }}>
          Not sure which plan fits?{" "}
          <a href="#demo" style={{ color: "#10b981", fontWeight: 600, textDecoration: "none" }}>Talk to us</a>
          {" "}— we'll help you figure it out.
        </p>
      </div>
    </section>
  );
}
