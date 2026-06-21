"use client";
import { useState } from "react";

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "12px 16px",
  borderRadius: 12,
  border: "1.5px solid rgba(0,0,0,0.12)",
  background: "white",
  fontSize: 14,
  color: "#111",
  fontFamily: "inherit",
  fontWeight: 500,
  outline: "none",
  transition: "border-color 0.15s",
  boxSizing: "border-box",
};

const labelStyle: React.CSSProperties = {
  display: "block",
  fontSize: 13,
  fontWeight: 700,
  color: "#333",
  marginBottom: 6,
  letterSpacing: "-0.01em",
};

export default function DemoForm() {
  const [form, setForm] = useState({
    name: "",
    business: "",
    email: "",
    phone: "",
    trade: "",
    plan: "",
    note: "",
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name || !form.email || !form.business) {
      setError("Please fill in your name, business name, and email.");
      return;
    }
    setError("");
    setLoading(true);

    await new Promise((r) => setTimeout(r, 1400));

    setLoading(false);
    setSuccess(true);
  };

  return (
    <section
      id="demo"
      style={{
        margin: "0 12px 12px",
        borderRadius: 24,
        background: "#f0ede6",
        position: "relative",
        overflow: "hidden",
        padding: "80px 48px",
      }}
    >
      {/* Grain overlay */}
      <div className="grain-overlay" style={{ position: "absolute", inset: 0, pointerEvents: "none", opacity: 0.6 }} />

      <div style={{ maxWidth: 580, margin: "0 auto", position: "relative", zIndex: 1 }}>
        <div style={{ textAlign: "center", marginBottom: 44 }}>
          <span
            style={{
              display: "inline-block",
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "#059669",
              marginBottom: 14,
            }}
          >
            Get started
          </span>
          <h2
            style={{
              fontSize: "clamp(32px, 3.5vw, 50px)",
              fontWeight: 900,
              letterSpacing: "-0.04em",
              lineHeight: 1.06,
              color: "#111",
              marginBottom: 14,
            }}
          >
            See Cleo in action.
          </h2>
          <p style={{ fontSize: 16, color: "#666", lineHeight: 1.55 }}>
            Tell us about your business and we&apos;ll set up a personalized walkthrough.
          </p>
        </div>

        {success ? (
          <div
            style={{
              textAlign: "center",
              background: "white",
              borderRadius: 20,
              padding: "48px 36px",
              border: "1px solid rgba(0,0,0,0.06)",
            }}
          >
            <div
              style={{
                width: 56,
                height: 56,
                borderRadius: "50%",
                background: "#10b981",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                margin: "0 auto 20px",
              }}
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M5 12l5 5 9-10" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <h3 style={{ fontSize: 22, fontWeight: 800, color: "#111", letterSpacing: "-0.04em", marginBottom: 10 }}>
              We&apos;ll be in touch soon.
            </h3>
            <p style={{ fontSize: 15, color: "#666", lineHeight: 1.55 }}>
              Thanks, {form.name.split(" ")[0]}! We typically respond within a few hours during business hours.
            </p>
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            style={{
              background: "white",
              borderRadius: 20,
              padding: "36px 36px",
              border: "1px solid rgba(0,0,0,0.06)",
              boxShadow: "0 4px 24px rgba(0,0,0,0.06)",
            }}
          >
            <div className="r-form" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
              <div>
                <label style={labelStyle}>Name *</label>
                <input
                  style={inputStyle}
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  placeholder="Alex Johnson"
                  required
                />
              </div>
              <div>
                <label style={labelStyle}>Business name *</label>
                <input
                  style={inputStyle}
                  name="business"
                  value={form.business}
                  onChange={handleChange}
                  placeholder="Johnson HVAC"
                  required
                />
              </div>
            </div>

            <div className="r-form" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
              <div>
                <label style={labelStyle}>Email *</label>
                <input
                  style={inputStyle}
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="alex@johnsonhvac.com"
                  required
                />
              </div>
              <div>
                <label style={labelStyle}>Phone</label>
                <input
                  style={inputStyle}
                  type="tel"
                  name="phone"
                  value={form.phone}
                  onChange={handleChange}
                  placeholder="(512) 555-0100"
                />
              </div>
            </div>

            <div style={{ marginBottom: 16 }}>
              <label style={labelStyle}>Your trade</label>
              <select
                style={{ ...inputStyle, appearance: "none", backgroundImage: "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath d='M4 6l4 4 4-4' stroke='%23888' strokeWidth='1.5' strokeLinecap='round' strokeLinejoin='round' fill='none'/%3E%3C/svg%3E\")", backgroundRepeat: "no-repeat", backgroundPosition: "right 14px center", paddingRight: 40, color: form.trade ? "#111" : "#999" }}
                name="trade"
                value={form.trade}
                onChange={handleChange}
              >
                <option value="" disabled>Select your trade...</option>
                <option value="hvac">HVAC</option>
                <option value="plumbing">Plumbing</option>
                <option value="electrical">Electrical</option>
                <option value="other">Other home service</option>
              </select>
            </div>

            <div style={{ marginBottom: 24 }}>
              <label style={labelStyle}>Preferred plan</label>
              <div className="r-plan-cards" style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10, marginTop: 2 }}>
                {[
                  { value: "starter", label: "Starter", price: "$89/mo", desc: "1 line" },
                  { value: "pro", label: "Pro", price: "$199/mo", desc: "3 lines", popular: true },
                  { value: "business", label: "Business", price: "$449/mo", desc: "Unlimited" },
                ].map((p) => {
                  const selected = form.plan === p.value;
                  return (
                    <button
                      key={p.value}
                      type="button"
                      onClick={() => setForm((prev) => ({ ...prev, plan: p.value }))}
                      style={{
                        padding: "12px 10px",
                        borderRadius: 12,
                        border: selected
                          ? "2px solid #10b981"
                          : "1.5px solid rgba(0,0,0,0.1)",
                        background: selected ? "rgba(16,185,129,0.06)" : "white",
                        cursor: "pointer",
                        textAlign: "center",
                        fontFamily: "inherit",
                        transition: "all 0.15s ease",
                        position: "relative",
                      }}
                    >
                      {p.popular && (
                        <div style={{
                          position: "absolute", top: -9, left: "50%", transform: "translateX(-50%)",
                          background: "#10b981", borderRadius: 999,
                          padding: "2px 8px", fontSize: 10, fontWeight: 700, color: "white",
                          whiteSpace: "nowrap", letterSpacing: "0.04em",
                        }}>
                          POPULAR
                        </div>
                      )}
                      <div style={{ fontSize: 13, fontWeight: 700, color: selected ? "#059669" : "#111", marginBottom: 2 }}>
                        {p.label}
                      </div>
                      <div style={{ fontSize: 13, fontWeight: 700, color: selected ? "#10b981" : "#333" }}>
                        {p.price}
                      </div>
                      <div style={{ fontSize: 11, color: selected ? "#059669" : "#aaa", marginTop: 1 }}>
                        {p.desc}
                      </div>
                    </button>
                  );
                })}
              </div>
              <p style={{ fontSize: 11.5, color: "#888", marginTop: 8 }}>
                Not sure? Leave blank and we&apos;ll recommend one.
              </p>
            </div>

            <div style={{ marginBottom: 24 }}>
              <label style={labelStyle}>Anything else we should know?</label>
              <textarea
                name="note"
                value={form.note}
                onChange={handleChange}
                placeholder="e.g. We get a lot of after-hours emergency calls and currently miss most of them..."
                rows={3}
                style={{
                  ...inputStyle,
                  resize: "none",
                  lineHeight: 1.6,
                  display: "block",
                }}
              />
            </div>

            {error && (
              <p style={{ fontSize: 13, color: "#dc2626", marginBottom: 16, fontWeight: 600 }}>{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              style={{
                width: "100%",
                padding: "14px 0",
                borderRadius: 12,
                border: "none",
                background: loading ? "#9ca3af" : "#111",
                color: "white",
                fontWeight: 800,
                fontSize: 15,
                letterSpacing: "-0.02em",
                cursor: loading ? "not-allowed" : "pointer",
                fontFamily: "inherit",
                transition: "all 0.15s",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: 8,
              }}
            >
              {loading ? (
                <>
                  <span
                    style={{
                      width: 16,
                      height: 16,
                      border: "2px solid rgba(255,255,255,0.3)",
                      borderTopColor: "white",
                      borderRadius: "50%",
                      display: "inline-block",
                      animation: "spin 0.7s linear infinite",
                    }}
                  />
                  Sending...
                </>
              ) : (
                "Request a Demo →"
              )}
            </button>

            <p style={{ textAlign: "center", marginTop: 14, fontSize: 12.5, color: "#777" }}>
              We typically respond within a few hours.
            </p>
          </form>
        )}
      </div>

      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </section>
  );
}
