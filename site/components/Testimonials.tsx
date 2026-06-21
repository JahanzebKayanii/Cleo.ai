const testimonials = [
  {
    quote: "Cleo paid for a full year of Pro on day one. We had an emergency AC call at 11pm — booked, confirmed, and the tech was dispatched before I even saw the notification.",
    name: "Derek Wallace",
    business: "Wallace Climate Control",
    trade: "HVAC",
    location: "Phoenix, AZ",
    initial: "DW",
    color: "#0d9488",
  },
  {
    quote: "I was skeptical — my customers are older, I didn't think they'd talk to an AI. But Cleo sounds completely natural. Two months in and not one complaint.",
    name: "Tony Marchetti",
    business: "Marchetti Plumbing",
    trade: "Plumbing",
    location: "Chicago, IL",
    initial: "TM",
    color: "#0284c7",
  },
  {
    quote: "Setup took maybe 45 minutes. I told Cleo our rates, our service area, and how to handle emergencies. It's been flawless. Our booking rate went from about 60% to 91%.",
    name: "Angela Brooks",
    business: "Brooks Electrical Services",
    trade: "Electrical",
    location: "Atlanta, GA",
    initial: "AB",
    color: "#7c3aed",
  },
  {
    quote: "The CRM sync alone is worth the price. Every call goes straight into Jobber as a job request. My office manager used to spend an hour a day on data entry — that's gone.",
    name: "James Okafor",
    business: "Okafor Home Services",
    trade: "HVAC",
    location: "Houston, TX",
    initial: "JO",
    color: "#b45309",
  },
];

export default function Testimonials() {
  return (
    <section style={{
      margin: "0 12px 12px", borderRadius: 24,
      background: "white", padding: "80px 60px",
      border: "1px solid rgba(0,0,0,0.05)",
    }}>
      <div style={{ maxWidth: 1060, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 56 }}>
          <span style={{
            fontSize: 11, fontWeight: 700, letterSpacing: "0.12em",
            textTransform: "uppercase", color: "#059669", display: "inline-block", marginBottom: 14,
          }}>
            What contractors say
          </span>
          <h2 style={{
            fontSize: "clamp(30px, 3.5vw, 48px)", fontWeight: 700,
            letterSpacing: "-0.04em", lineHeight: 1.06, color: "#111", marginBottom: 14,
          }}>
            Trusted by contractors across the US.
          </h2>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          {testimonials.map((t) => (
            <div key={t.name} style={{
              background: "#f7f6f2", borderRadius: 20, padding: "32px 32px",
              border: "1px solid rgba(0,0,0,0.05)",
              display: "flex", flexDirection: "column", gap: 24,
            }}>
              {/* Stars */}
              <div style={{ display: "flex", gap: 3 }}>
                {Array.from({ length: 5 }).map((_, i) => (
                  <svg key={i} width="15" height="15" viewBox="0 0 14 14" fill="#10b981">
                    <path d="M7 1l1.6 3.3 3.6.5-2.6 2.5.6 3.6L7 9.3l-3.2 1.6.6-3.6L1.8 4.8l3.6-.5z" />
                  </svg>
                ))}
              </div>

              {/* Quote */}
              <p style={{
                fontSize: 15, color: "#222", lineHeight: 1.75,
                fontStyle: "italic", flex: 1,
              }}>
                &ldquo;{t.quote}&rdquo;
              </p>

              {/* Person row */}
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <div style={{
                  width: 44, height: 44, borderRadius: "50%", flexShrink: 0,
                  background: t.color,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: 14, fontWeight: 700, color: "white",
                }}>
                  {t.initial}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 14, fontWeight: 700, color: "#111", letterSpacing: "-0.02em" }}>
                    {t.name}
                  </div>
                  <div style={{ fontSize: 12.5, color: "#888", marginTop: 1 }}>
                    {t.business} · {t.location}
                  </div>
                </div>
                <span style={{
                  fontSize: 11, fontWeight: 700, color: "#10b981",
                  background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.18)",
                  borderRadius: 999, padding: "4px 12px", flexShrink: 0,
                }}>
                  {t.trade}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
