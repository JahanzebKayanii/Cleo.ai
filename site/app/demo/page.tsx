import Nav from "../../components/Nav";
import DemoForm from "../../components/DemoForm";

export const metadata = {
  title: "Request a Demo — CleoVoice",
  description:
    "See Cleo handle a real call. 15-minute live walkthrough — Cleo picks up, qualifies the caller, books the job, and syncs to your CRM.",
};

function CheckCircle() {
  return (
    <svg width="15" height="15" viewBox="0 0 15 15" fill="none" style={{ flexShrink: 0 }}>
      <circle cx="7.5" cy="7.5" r="7.5" fill="#10b981" />
      <path
        d="M4.5 7.5l2.2 2.2 3.8-4"
        stroke="white"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default function DemoPage() {
  return (
    <main style={{ minHeight: "100vh", background: "#f7f6f2", fontFamily: "'Space Grotesk', sans-serif" }}>
      <Nav />

      {/* Hero */}
      <section style={{ paddingTop: 64, background: "#f7f6f2" }}>
        <div
          style={{
            maxWidth: 680,
            margin: "0 auto",
            padding: "72px 24px 60px",
            textAlign: "center",
          }}
        >
          <span
            style={{
              display: "inline-block",
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "#059669",
              marginBottom: 16,
            }}
          >
            Request a Demo
          </span>

          <h1
            style={{
              fontSize: "clamp(38px, 5vw, 60px)",
              fontWeight: 700,
              letterSpacing: "-0.04em",
              lineHeight: 1.05,
              color: "#111",
              margin: "0 0 20px",
            }}
          >
            See Cleo handle<br />a real call.
          </h1>

          <p
            style={{
              fontSize: 17,
              color: "#555",
              lineHeight: 1.65,
              maxWidth: 520,
              margin: "0 auto 40px",
            }}
          >
            We&apos;ll run you through a 15-minute live walkthrough — Cleo picks up, qualifies
            the caller, books the appointment, and syncs to your CRM. No slides. Just the product.
          </p>

          {/* Trust pills */}
          <div
            className="r-trust-pills"
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 10,
              flexWrap: "wrap",
            }}
          >
            {[
              "Live call, not a recording",
              "Works with your phone number",
              "15 min — no prep needed",
            ].map((item) => (
              <div
                key={item}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 7,
                  fontSize: 13,
                  fontWeight: 600,
                  color: "#333",
                  background: "white",
                  border: "1px solid rgba(0,0,0,0.09)",
                  borderRadius: 999,
                  padding: "8px 14px",
                  boxShadow: "0 1px 4px rgba(0,0,0,0.05)",
                }}
              >
                <CheckCircle />
                {item}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Form */}
      <DemoForm />

      {/* What happens next */}
      <section
        style={{
          margin: "0 12px 12px",
          borderRadius: 24,
          background: "white",
          border: "1px solid rgba(0,0,0,0.06)",
          padding: "64px 48px",
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
                color: "#059669",
                marginBottom: 12,
              }}
            >
              What to expect
            </span>
            <h2
              style={{
                fontSize: "clamp(26px, 3vw, 36px)",
                fontWeight: 700,
                letterSpacing: "-0.04em",
                color: "#111",
                margin: 0,
              }}
            >
              Here&apos;s what happens after you submit.
            </h2>
          </div>

          <div
            className="r-3col"
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: 24,
            }}
          >
            {[
              {
                step: "01",
                title: "We reach out",
                body: "Someone from our team will email or call you within a few hours to confirm a time that works.",
              },
              {
                step: "02",
                title: "Live walkthrough",
                body: "We'll call your real business number and let Cleo handle it — intake, booking, the works. You watch in real time.",
              },
              {
                step: "03",
                title: "Get set up",
                body: "If it's a fit, we configure Cleo for your trade, connect your CRM, and you're live. Usually same day.",
              },
            ].map((s) => (
              <div key={s.step}>
                <div
                  style={{
                    fontSize: 11,
                    fontWeight: 700,
                    letterSpacing: "0.1em",
                    color: "#10b981",
                    marginBottom: 10,
                  }}
                >
                  {s.step}
                </div>
                <h3
                  style={{
                    fontSize: 17,
                    fontWeight: 700,
                    letterSpacing: "-0.03em",
                    color: "#111",
                    margin: "0 0 8px",
                  }}
                >
                  {s.title}
                </h3>
                <p style={{ fontSize: 14, color: "#666", lineHeight: 1.6, margin: 0 }}>
                  {s.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer
        style={{
          margin: "0 12px 12px",
          borderRadius: 24,
          background: "#0d0f14",
          padding: "40px 48px",
          textAlign: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 10,
            marginBottom: 14,
          }}
        >
          <svg viewBox="0 0 40 40" width="28" height="28" fill="none">
            <rect width="40" height="40" rx="10" fill="#1a1d27" />
            <rect x="11" y="14" width="4.5" height="12" rx="2.25" fill="#10b981" />
            <rect x="17.75" y="9" width="4.5" height="22" rx="2.25" fill="#10b981" />
            <rect x="24.5" y="14" width="4.5" height="12" rx="2.25" fill="#10b981" />
          </svg>
          <span
            style={{
              fontWeight: 700,
              fontSize: 15,
              color: "white",
              letterSpacing: "-0.03em",
            }}
          >
            CleoVoice
          </span>
        </div>
        <p style={{ fontSize: 13, color: "rgba(255,255,255,0.38)", margin: 0 }}>
          © 2025 CleoVoice. All rights reserved.
        </p>
      </footer>
    </main>
  );
}
