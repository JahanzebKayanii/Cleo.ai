import Nav from "@/components/Nav";
import Reveal from "@/components/Reveal";

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

const tradeColors: Record<string, { bg: string; color: string }> = {
  HVAC:       { bg: "rgba(59,130,246,0.1)",  color: "#2563EB" },
  Plumbing:   { bg: "rgba(6,182,212,0.1)",   color: "#0891B2" },
  Electrical: { bg: "rgba(234,179,8,0.12)",  color: "#B45309" },
};

const crms = [
  {
    name: "Jobber",
    initials: "J",
    color: "#F97316",
    category: "Field Service Software",
    status: "live" as const,
    trades: ["HVAC", "Plumbing", "Electrical"],
    flows: ["Client record created", "Job request filed", "Call notes attached"],
    desc: "After every call Cleo creates a client and job request in Jobber, pre-filled with the caller's name, address, and problem description.",
  },
  {
    name: "HubSpot",
    initials: "HS",
    color: "#FF7A59",
    category: "CRM",
    status: "live" as const,
    trades: ["HVAC", "Plumbing", "Electrical"],
    flows: ["Contact created", "Deal opened in pipeline", "Full call note logged"],
    desc: "Cleo pushes a new contact, opens a deal, and attaches a full call summary note — your pipeline stays current without anyone lifting a finger.",
  },
  {
    name: "Housecall Pro",
    initials: "HP",
    color: "#00A6A8",
    category: "Field Service Software",
    status: "live" as const,
    trades: ["HVAC", "Plumbing", "Electrical"],
    flows: ["Customer created", "Job request sent", "Service notes added"],
    desc: "New customers and job requests land in Housecall Pro the moment a call ends. Your dispatch queue stays current without any manual entry.",
  },
  {
    name: "ServiceTitan",
    initials: "ST",
    color: "#0052CC",
    category: "Field Service Software",
    status: "coming" as const,
    trades: ["HVAC", "Plumbing", "Electrical"],
    flows: ["Customer sync", "Job created", "Call recording linked"],
    desc: "Full ServiceTitan integration in development. Cleo will push customers, jobs, and call notes directly into your ServiceTitan account.",
  },
  {
    name: "FieldEdge",
    initials: "FE",
    color: "#1D4ED8",
    category: "Field Service Software",
    status: "coming" as const,
    trades: ["HVAC"],
    flows: ["Customer record", "Service request", "Tech dispatch notes"],
    desc: "Purpose-built for HVAC contractors who rely on FieldEdge for dispatch and invoicing. FieldEdge support is coming soon.",
  },
  {
    name: "Service Fusion",
    initials: "SF",
    color: "#7C3AED",
    category: "Field Service Software",
    status: "coming" as const,
    trades: ["HVAC", "Plumbing", "Electrical"],
    flows: ["Customer created", "Work order opened", "Job notes synced"],
    desc: "Service Fusion integration will create customers and work orders directly from Cleo call data — no double-entry required.",
  },
  {
    name: "BuildOps",
    initials: "BO",
    color: "#374151",
    category: "Field Service Software",
    status: "coming" as const,
    trades: ["Electrical", "Plumbing"],
    flows: ["Customer record", "Project created", "Call summary filed"],
    desc: "Coming for commercial electrical and plumbing contractors — creating jobs and syncing Cleo call data into BuildOps automatically.",
  },
  {
    name: "mHelpDesk",
    initials: "mH",
    color: "#16A34A",
    category: "Field Service Software",
    status: "coming" as const,
    trades: ["HVAC", "Plumbing", "Electrical"],
    flows: ["Customer profile", "Work order created", "Service notes"],
    desc: "mHelpDesk integration will create customers and work orders from every Cleo call, keeping your service history complete and current.",
  },
];

const infrastructure = [
  {
    icon: "📅",
    color: "#4285F4",
    name: "Google Calendar",
    category: "Scheduling",
    status: "live" as const,
    desc: "Cleo checks your Google Calendar for real open slots before booking — no double-booking, no guessing. Confirmed appointments are added automatically.",
    flows: ["Reads availability in real time", "Creates confirmed appointments", "Avoids double-booking"],
  },
  {
    icon: "📞",
    color: "#F22F46",
    name: "Twilio",
    category: "Voice & SMS",
    status: "live" as const,
    desc: "All inbound calls route through Twilio. After booking, Cleo fires an SMS confirmation to the customer — all via the same Twilio number.",
    flows: ["Powers all inbound calls", "Sends SMS confirmations", "Supports live call transfer"],
  },
  {
    icon: "🎙️",
    color: "#13B8A4",
    name: "Deepgram",
    category: "AI Transcription",
    status: "live" as const,
    desc: "Deepgram nova-2 transcribes every call in real time. The transcript feeds Claude, enabling Cleo to understand callers and respond naturally.",
    flows: ["Real-time speech-to-text", "Nova-2 model accuracy", "Powers Claude understanding"],
  },
  {
    icon: "🤖",
    color: "#6B4FBB",
    name: "Claude AI",
    category: "Conversation Intelligence",
    status: "live" as const,
    desc: "Claude Sonnet powers Cleo's reasoning — extracting structured data from conversations, choosing the right tool calls, and adapting to your business.",
    flows: ["Natural conversation handling", "Structured data extraction", "Tool-call decision making"],
  },
];

export default function IntegrationsPage() {
  return (
    <>
      <Nav />

      {/* Hero */}
      <section
        style={{
          margin: "68px 12px 12px",
          borderRadius: 24,
          background: "#080a0e",
          padding: "80px 48px 72px",
          textAlign: "center",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Glow */}
        <div
          style={{
            position: "absolute",
            top: -80,
            left: "50%",
            transform: "translateX(-50%)",
            width: 500,
            height: 300,
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%)",
            pointerEvents: "none",
          }}
        />

        <div style={{ position: "relative", zIndex: 1, maxWidth: 680, margin: "0 auto" }}>
          <span
            style={{
              display: "inline-block",
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "#34d399",
              marginBottom: 16,
            }}
          >
            Integrations
          </span>
          <h1
            style={{
              fontSize: "clamp(42px, 6vw, 72px)",
              fontWeight: 900,
              letterSpacing: "-0.05em",
              lineHeight: 1.02,
              color: "white",
              marginBottom: 20,
            }}
          >
            Works with your stack.
          </h1>
          <p
            style={{
              fontSize: 18,
              color: "rgba(255,255,255,0.5)",
              lineHeight: 1.6,
              maxWidth: 500,
              margin: "0 auto 32px",
            }}
          >
            Cleo plugs into the CRM and field service software your business already runs. After every call, data flows to the right place — automatically.
          </p>

          {/* Live badge */}
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 16,
              background: "rgba(255,255,255,0.04)",
              border: "1px solid rgba(255,255,255,0.08)",
              borderRadius: 999,
              padding: "10px 20px",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <span style={{ width: 7, height: 7, borderRadius: "50%", background: "#10b981", display: "inline-block" }} />
              <span style={{ fontSize: 13, fontWeight: 700, color: "rgba(255,255,255,0.6)" }}>3 live now</span>
            </div>
            <div style={{ width: 1, height: 14, background: "rgba(255,255,255,0.1)" }} />
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <span style={{ width: 7, height: 7, borderRadius: "50%", background: "#9CA3AF", display: "inline-block" }} />
              <span style={{ fontSize: 13, fontWeight: 700, color: "rgba(255,255,255,0.4)" }}>5 coming soon</span>
            </div>
          </div>
        </div>
      </section>

      {/* CRM Section */}
      <section
        style={{
          margin: "0 12px 12px",
          borderRadius: 24,
          background: "#f5f4f1",
          padding: "72px 48px",
        }}
      >
        <div style={{ maxWidth: 1060, margin: "0 auto" }}>
          <Reveal>
            <div style={{ marginBottom: 48 }}>
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
                CRM & Field Service Software
              </span>
              <h2
                style={{
                  fontSize: "clamp(28px, 3.5vw, 44px)",
                  fontWeight: 900,
                  letterSpacing: "-0.04em",
                  lineHeight: 1.06,
                  color: "#111",
                  maxWidth: 520,
                }}
              >
                The 8 platforms home service businesses run on.
              </h2>
            </div>
          </Reveal>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: 14,
            }}
          >
            {crms.map((crm, i) => (
              <Reveal key={crm.name} delay={(i % 4) * 0.07}>
                <div
                  style={{
                    background: "white",
                    borderRadius: 18,
                    padding: "24px 22px",
                    border: "1px solid rgba(0,0,0,0.05)",
                    display: "flex",
                    flexDirection: "column",
                    gap: 0,
                    height: "100%",
                    boxSizing: "border-box",
                  }}
                >
                  {/* Icon + status row */}
                  <div
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      justifyContent: "space-between",
                      marginBottom: 14,
                    }}
                  >
                    <div
                      style={{
                        width: 44,
                        height: 44,
                        borderRadius: 12,
                        background: crm.color,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: "white",
                        fontWeight: 900,
                        fontSize: crm.initials.length > 1 ? 13 : 18,
                        letterSpacing: "-0.02em",
                        flexShrink: 0,
                      }}
                    >
                      {crm.initials}
                    </div>
                    <span
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: 5,
                        padding: "4px 10px",
                        borderRadius: 999,
                        fontSize: 11,
                        fontWeight: 700,
                        letterSpacing: "0.02em",
                        background: crm.status === "live" ? "rgba(16,185,129,0.1)" : "rgba(0,0,0,0.05)",
                        color: crm.status === "live" ? "#059669" : "#9CA3AF",
                        border: crm.status === "live" ? "1px solid rgba(16,185,129,0.2)" : "1px solid rgba(0,0,0,0.06)",
                      }}
                    >
                      {crm.status === "live" ? (
                        <>
                          <span style={{ width: 5, height: 5, borderRadius: "50%", background: "#10b981", display: "inline-block" }} />
                          Live
                        </>
                      ) : (
                        "Coming soon"
                      )}
                    </span>
                  </div>

                  {/* Name + category */}
                  <div style={{ marginBottom: 8 }}>
                    <div
                      style={{
                        fontSize: 16,
                        fontWeight: 800,
                        color: "#111",
                        letterSpacing: "-0.03em",
                        marginBottom: 2,
                      }}
                    >
                      {crm.name}
                    </div>
                    <div style={{ fontSize: 11.5, color: "#999", fontWeight: 600, letterSpacing: "0.02em" }}>
                      {crm.category}
                    </div>
                  </div>

                  {/* Description */}
                  <p
                    style={{
                      fontSize: 13,
                      color: "#666",
                      lineHeight: 1.6,
                      marginBottom: 14,
                      flexGrow: 1,
                    }}
                  >
                    {crm.desc}
                  </p>

                  {/* What flows */}
                  <div style={{ marginBottom: 14 }}>
                    {crm.flows.map((flow) => (
                      <div
                        key={flow}
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 7,
                          marginBottom: 5,
                        }}
                      >
                        <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                          <circle cx="6" cy="6" r="6" fill={crm.status === "live" ? "rgba(16,185,129,0.15)" : "rgba(0,0,0,0.06)"} />
                          <path
                            d="M3.5 6l1.8 1.8 3.2-3.6"
                            stroke={crm.status === "live" ? "#10b981" : "#9CA3AF"}
                            strokeWidth="1.3"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />
                        </svg>
                        <span style={{ fontSize: 12, color: "#555", fontWeight: 500 }}>{flow}</span>
                      </div>
                    ))}
                  </div>

                  {/* Trade chips */}
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 5 }}>
                    {crm.trades.map((trade) => (
                      <span
                        key={trade}
                        style={{
                          padding: "3px 9px",
                          borderRadius: 999,
                          fontSize: 11,
                          fontWeight: 700,
                          background: tradeColors[trade].bg,
                          color: tradeColors[trade].color,
                          letterSpacing: "-0.01em",
                        }}
                      >
                        {trade}
                      </span>
                    ))}
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Core Infrastructure */}
      <section
        style={{
          margin: "0 12px 12px",
          borderRadius: 24,
          background: "#080a0e",
          padding: "72px 48px",
        }}
      >
        <div style={{ maxWidth: 1060, margin: "0 auto" }}>
          <Reveal>
            <div style={{ marginBottom: 48 }}>
              <span
                style={{
                  display: "inline-block",
                  fontSize: 11,
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  textTransform: "uppercase",
                  color: "#34d399",
                  marginBottom: 12,
                }}
              >
                Core infrastructure
              </span>
              <h2
                style={{
                  fontSize: "clamp(28px, 3.5vw, 44px)",
                  fontWeight: 900,
                  letterSpacing: "-0.04em",
                  lineHeight: 1.06,
                  color: "white",
                  maxWidth: 500,
                }}
              >
                The technology stack powering every call.
              </h2>
            </div>
          </Reveal>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 14 }}>
            {infrastructure.map((item, i) => (
              <Reveal key={item.name} delay={i * 0.08}>
                <div
                  style={{
                    background: "rgba(255,255,255,0.03)",
                    border: "1px solid rgba(255,255,255,0.07)",
                    borderRadius: 18,
                    padding: "28px 24px",
                    height: "100%",
                    boxSizing: "border-box",
                    display: "flex",
                    flexDirection: "column",
                  }}
                >
                  {/* Icon + status */}
                  <div
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      justifyContent: "space-between",
                      marginBottom: 16,
                    }}
                  >
                    <div
                      style={{
                        width: 44,
                        height: 44,
                        borderRadius: 12,
                        background: `${item.color}22`,
                        border: `1px solid ${item.color}44`,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: 20,
                      }}
                    >
                      {item.icon}
                    </div>
                    <span
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: 5,
                        padding: "4px 10px",
                        borderRadius: 999,
                        fontSize: 11,
                        fontWeight: 700,
                        background: "rgba(16,185,129,0.1)",
                        color: "#34d399",
                        border: "1px solid rgba(16,185,129,0.2)",
                      }}
                    >
                      <span style={{ width: 5, height: 5, borderRadius: "50%", background: "#10b981", display: "inline-block" }} />
                      Live
                    </span>
                  </div>

                  <div style={{ marginBottom: 8 }}>
                    <div
                      style={{
                        fontSize: 16,
                        fontWeight: 800,
                        color: "white",
                        letterSpacing: "-0.03em",
                        marginBottom: 2,
                      }}
                    >
                      {item.name}
                    </div>
                    <div style={{ fontSize: 11.5, color: "rgba(255,255,255,0.3)", fontWeight: 600, letterSpacing: "0.02em" }}>
                      {item.category}
                    </div>
                  </div>

                  <p
                    style={{
                      fontSize: 13,
                      color: "rgba(255,255,255,0.45)",
                      lineHeight: 1.65,
                      marginBottom: 16,
                      flexGrow: 1,
                    }}
                  >
                    {item.desc}
                  </p>

                  {item.flows.map((flow) => (
                    <div
                      key={flow}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 7,
                        marginBottom: 5,
                      }}
                    >
                      <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <circle cx="6" cy="6" r="6" fill="rgba(16,185,129,0.15)" />
                        <path d="M3.5 6l1.8 1.8 3.2-3.6" stroke="#10b981" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      <span style={{ fontSize: 12, color: "rgba(255,255,255,0.4)", fontWeight: 500 }}>{flow}</span>
                    </div>
                  ))}
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* How data flows */}
      <section
        style={{
          margin: "0 12px 12px",
          borderRadius: 24,
          background: "#f5f4f1",
          padding: "72px 48px",
        }}
      >
        <div style={{ maxWidth: 880, margin: "0 auto" }}>
          <Reveal>
            <div style={{ textAlign: "center", marginBottom: 52 }}>
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
                Data flow
              </span>
              <h2
                style={{
                  fontSize: "clamp(28px, 3.5vw, 44px)",
                  fontWeight: 900,
                  letterSpacing: "-0.04em",
                  lineHeight: 1.06,
                  color: "#111",
                }}
              >
                From a phone call to your CRM
                <br />
                in under 5 seconds.
              </h2>
            </div>
          </Reveal>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: 0,
              position: "relative",
            }}
          >
            {[
              {
                num: "1",
                title: "Call comes in",
                body: "Customer dials your number. Cleo answers in under 2 seconds.",
                icon: "📲",
              },
              {
                num: "2",
                title: "Cleo extracts data",
                body: "Name, address, problem, and appointment slot are pulled from the conversation.",
                icon: "🧠",
              },
              {
                num: "3",
                title: "Calendar updated",
                body: "Appointment added to Google Calendar. Customer receives an SMS confirmation.",
                icon: "📅",
              },
              {
                num: "4",
                title: "CRM synced",
                body: "Contact and job created in Jobber, HubSpot, or Housecall Pro. You get an email summary.",
                icon: "🔗",
              },
            ].map((step, i) => (
              <Reveal key={i} delay={i * 0.1}>
                <div
                  style={{
                    padding: "28px 24px 28px",
                    borderRight: i < 3 ? "1px solid rgba(0,0,0,0.07)" : "none",
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      fontSize: 28,
                      marginBottom: 14,
                      display: "block",
                    }}
                  >
                    {step.icon}
                  </div>
                  <div
                    style={{
                      fontSize: 11,
                      fontWeight: 800,
                      letterSpacing: "0.06em",
                      color: "#10b981",
                      marginBottom: 8,
                      textTransform: "uppercase",
                    }}
                  >
                    Step {step.num}
                  </div>
                  <div
                    style={{
                      fontSize: 15,
                      fontWeight: 800,
                      color: "#111",
                      letterSpacing: "-0.03em",
                      marginBottom: 8,
                    }}
                  >
                    {step.title}
                  </div>
                  <p style={{ fontSize: 13, color: "#666", lineHeight: 1.6 }}>{step.body}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section
        style={{
          margin: "0 12px 12px",
          borderRadius: 24,
          background: "#f0ede6",
          position: "relative",
          overflow: "hidden",
          padding: "72px 48px",
          textAlign: "center",
        }}
      >
        <div className="grain-overlay" style={{ position: "absolute", inset: 0, pointerEvents: "none", opacity: 0.6 }} />
        <div style={{ position: "relative", zIndex: 1, maxWidth: 560, margin: "0 auto" }}>
          <h2
            style={{
              fontSize: "clamp(28px, 3.5vw, 44px)",
              fontWeight: 900,
              letterSpacing: "-0.04em",
              lineHeight: 1.06,
              color: "#111",
              marginBottom: 14,
            }}
          >
            Don&apos;t see your software?
          </h2>
          <p style={{ fontSize: 16, color: "#666", lineHeight: 1.55, marginBottom: 32 }}>
            We&apos;re adding integrations regularly. Tell us what you use and we&apos;ll prioritize it.
          </p>
          <a
            href="/#demo"
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
              padding: "14px 32px",
              borderRadius: 999,
              background: "#111",
              color: "white",
              fontWeight: 800,
              fontSize: 15,
              letterSpacing: "-0.02em",
              textDecoration: "none",
            }}
          >
            Request a Demo →
          </a>
          <p style={{ marginTop: 14, fontSize: 12.5, color: "#aaa" }}>Mention your CRM in the form and we&apos;ll take note.</p>
        </div>
      </section>

      {/* Footer */}
      <footer
        style={{
          margin: "0 12px 12px",
          borderRadius: 24,
          background: "#111",
          padding: "44px 48px",
        }}
      >
        <div
          style={{
            maxWidth: 960,
            margin: "0 auto",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: 20,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <CleoLogo />
            <div>
              <div style={{ fontWeight: 800, fontSize: 15, color: "white", letterSpacing: "-0.03em" }}>CleoVoice</div>
              <div style={{ fontSize: 12, color: "rgba(255,255,255,0.3)", marginTop: 1 }}>AI receptionist for home services</div>
            </div>
          </div>

          <div style={{ display: "flex", gap: 24 }}>
            {[
              { label: "How it works", href: "/#how" },
              { label: "Pricing", href: "/#pricing" },
              { label: "Request a Demo", href: "/#demo" },
            ].map((link) => (
              <a key={link.label} href={link.href} className="footer-link">{link.label}</a>
            ))}
          </div>

          <div style={{ fontSize: 12, color: "rgba(255,255,255,0.2)", letterSpacing: "-0.01em" }}>
            © 2026 CleoVoice. All rights reserved.
          </div>
        </div>
      </footer>
    </>
  );
}
