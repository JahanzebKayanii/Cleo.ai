"use client";
import { useState } from "react";

const faqs = [
  {
    q: "Does Cleo work with my existing phone number?",
    a: "Yes. You can forward your existing business number to Cleo, or use Cleo as your primary business line. Setup takes under 10 minutes.",
  },
  {
    q: "Which CRMs does Cleo integrate with?",
    a: "Jobber, HubSpot, and Housecall Pro are supported today. If you use something else, reach out — we're adding integrations continuously.",
  },
  {
    q: "What happens if Cleo doesn't know the answer?",
    a: "Cleo tells the caller that a team member will follow up, takes their name and callback number, and sends you an email summary. It never makes up answers or guesses.",
  },
  {
    q: "Can I customize what Cleo says?",
    a: "Yes. You set your business name, hours, service area, services offered, and can add custom instructions in plain English. Cleo adapts entirely to your business.",
  },
  {
    q: "What happens after hours?",
    a: "Cleo lets callers know the office is closed, takes down their name and issue, and flags it for your team the next morning. Urgent situations are always acknowledged.",
  },
  {
    q: "Is there a contract?",
    a: "No. Month-to-month on the monthly plan, annual billing on the annual plan. Cancel any time — no penalties.",
  },
];

export default function FAQSection() {
  const [open, setOpen] = useState<number | null>(null);

  const toggle = (i: number) => setOpen(open === i ? null : i);

  return (
    <section
      style={{
        margin: "0 12px 12px",
        borderRadius: 24,
        background: "#080a0e",
        padding: "80px 48px",
      }}
    >
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 48 }}>
          <span
            style={{
              display: "inline-block",
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "#34d399",
              marginBottom: 14,
            }}
          >
            FAQ
          </span>
          <h2
            style={{
              fontSize: "clamp(30px, 3.5vw, 48px)",
              fontWeight: 900,
              letterSpacing: "-0.04em",
              lineHeight: 1.06,
              color: "white",
            }}
          >
            Questions, answered.
          </h2>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
          {faqs.map((faq, i) => (
            <div
              key={i}
              style={{
                borderRadius: 14,
                border: "1px solid",
                borderColor: open === i ? "rgba(16,185,129,0.3)" : "rgba(255,255,255,0.07)",
                background: open === i ? "rgba(16,185,129,0.05)" : "rgba(255,255,255,0.02)",
                overflow: "hidden",
                transition: "border-color 0.2s, background 0.2s",
                cursor: "pointer",
              }}
              onClick={() => toggle(i)}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "18px 22px",
                  gap: 16,
                }}
              >
                <span
                  style={{
                    fontSize: 15,
                    fontWeight: 700,
                    color: open === i ? "white" : "rgba(255,255,255,0.88)",
                    letterSpacing: "-0.02em",
                    lineHeight: 1.35,
                  }}
                >
                  {faq.q}
                </span>
                <span
                  style={{
                    flexShrink: 0,
                    width: 26,
                    height: 26,
                    borderRadius: "50%",
                    background: open === i ? "#10b981" : "rgba(255,255,255,0.08)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    transition: "all 0.2s ease",
                  }}
                >
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <path
                      d={open === i ? "M2 6h8" : "M6 2v8M2 6h8"}
                      stroke={open === i ? "white" : "rgba(255,255,255,0.5)"}
                      strokeWidth="1.8"
                      strokeLinecap="round"
                    />
                  </svg>
                </span>
              </div>

              <div
                style={{
                  maxHeight: open === i ? 200 : 0,
                  overflow: "hidden",
                  transition: "max-height 0.3s ease",
                }}
              >
                <p
                  style={{
                    padding: "0 22px 18px",
                    fontSize: 14,
                    color: "rgba(255,255,255,0.72)",
                    lineHeight: 1.65,
                  }}
                >
                  {faq.a}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
