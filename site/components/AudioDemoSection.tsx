"use client";
import { useState, useRef, useEffect } from "react";

const waveBarHeights = [
  10,18,30,45,58,72,84,92,88,82,76,80,70,62,52,42,34,26,36,50,
  64,78,88,85,76,66,55,44,34,26,18,28,42,56,70,82,90,86,78,68,
  58,47,37,27,19,30,46,62,76,87,82,72,62,51,40,30,22,34,50,66,
  80,88,83,73,62,50,39,28,20,32,48,64,78,86,80,70,59,47,36,26,
  10,18,30,45,58,72,84,92,88,82,76,80,70,62,52,42,34,26,36,50,
  64,78,88,85,76,66,55,44,34,26,18,28,42,56,70,82,90,86,78,68,
];

const DEMOS = [
  {
    id: "hvac",
    trade: "HVAC",
    title: "HVAC Service Call",
    desc: "AC down in summer heat — Cleo books a same-day appointment before the homeowner hangs up.",
    src: "/audio/hvac.mp3",
    photo: "/hvac.jpg",
    accent: "#10b981",
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 2v20M2 12h20M4.93 4.93l14.14 14.14M19.07 4.93L4.93 19.07"/>
      </svg>
    ),
  },
  {
    id: "plumbing",
    trade: "Plumbing",
    title: "Plumbing Emergency",
    desc: "Active leak getting worse — Cleo captures every detail and books the next available tech fast.",
    src: "/audio/plumbing.mp3",
    photo: "/plumbing.jpg",
    accent: "#10b981",
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z"/>
      </svg>
    ),
  },
  {
    id: "electrical",
    trade: "Electrical",
    title: "Electrical Emergency",
    desc: "11 PM storm outage — Cleo stays calm, triages the issue, and gets a tech scheduled by morning.",
    src: "/audio/electrical.mp3",
    photo: "/electrical.jpg",
    accent: "#10b981",
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
      </svg>
    ),
  },
];

function makeWave(seed: number, n = 48): number[] {
  return Array.from({ length: n }, (_, i) =>
    Math.max(4, Math.round(Math.abs(Math.sin(i * 0.42 + seed) * 14 + Math.sin(i * 0.85 + seed * 1.7) * 8 + 5)))
  );
}
const WAVES = DEMOS.map((_, i) => makeWave(i * 1.4 + 0.3));

export default function AudioDemoSection() {
  const [activeId, setActiveId] = useState<string | null>(null);
  const [playing, setPlaying]   = useState(false);
  const [progress, setProgress] = useState(0);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const handlePlay = (demoId: string) => {
    if (activeId === demoId && audioRef.current) {
      if (playing) { audioRef.current.pause(); setPlaying(false); }
      else         { audioRef.current.play();  setPlaying(true);  }
      return;
    }
    if (audioRef.current) { audioRef.current.pause(); audioRef.current.src = ""; }
    const demo = DEMOS.find(d => d.id === demoId);
    if (!demo) return;
    const audio = new Audio(demo.src);
    audioRef.current = audio;
    audio.addEventListener("timeupdate", () => setProgress(audio.currentTime / (audio.duration || 1)));
    audio.addEventListener("ended", () => { setPlaying(false); setActiveId(null); setProgress(0); });
    setActiveId(demoId); setProgress(0);
    audio.play().then(() => setPlaying(true)).catch(() => {});
  };

  useEffect(() => () => { audioRef.current?.pause(); }, []);

  return (
    <section className="r-section" style={{
      margin: "0 12px 12px",
      borderRadius: 24,
      background: "#080a0e",
      overflow: "hidden",
      position: "relative",
      padding: "80px 60px",
    }}>
      {/* Background waveform */}
      <div style={{
        position: "absolute", inset: 0,
        display: "flex", alignItems: "center", gap: 3,
        pointerEvents: "none", zIndex: 0,
        opacity: playing ? 0.5 : 0.15,
        transition: "opacity 0.8s ease",
      }}>
        {waveBarHeights.map((h, i) => (
          <div key={i} style={{
            flex: 1,
            height: `${h * 0.5}%`,
            borderRadius: 3,
            background: "#10b981",
            transformOrigin: "center",
            ...(playing ? {
              animationName: "wavePulse",
              animationDuration: `${0.8 + (i % 9) * 0.12}s`,
              animationTimingFunction: "ease-in-out",
              animationIterationCount: "infinite",
              animationDirection: "alternate",
              animationDelay: `${(i * 0.04) % 1.2}s`,
            } : {}),
          }} />
        ))}
      </div>

      {/* Content */}
      <div style={{ position: "relative", zIndex: 1, maxWidth: 1060, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 52 }}>
          <div style={{
            display: "inline-flex", alignItems: "center",
            border: "1px solid rgba(16,185,129,0.3)", borderRadius: 999,
            padding: "5px 16px", marginBottom: 20,
            background: "rgba(16,185,129,0.08)",
          }}>
            <span style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", color: "#34d399" }}>
              Live demos
            </span>
          </div>
          <h2 style={{
            fontSize: "clamp(28px, 3.5vw, 46px)", fontWeight: 900,
            letterSpacing: "-0.04em", lineHeight: 1.06, color: "white", marginBottom: 14,
          }}>
            Hear Cleo handle a real call.
          </h2>
          <p style={{ fontSize: 16, color: "rgba(255,255,255,0.75)", lineHeight: 1.65, maxWidth: 460, margin: "0 auto" }}>
            Three trades. Three emergencies. One AI that never misses.
          </p>
        </div>

        {/* Cards */}
        <div className="r-3col" style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14 }}>
          {DEMOS.map((demo, di) => {
            const isActive  = activeId === demo.id;
            const isPlaying = isActive && playing;
            const wave      = WAVES[di];
            const prog      = isActive ? progress : 0;

            return (
              <div key={demo.id} style={{
                position: "relative",
                borderRadius: 20, overflow: "hidden",
                border: isActive ? "1px solid rgba(16,185,129,0.4)" : "1px solid rgba(255,255,255,0.06)",
                minHeight: 440,
                transition: "all 0.22s ease",
                boxShadow: isActive ? "0 0 48px rgba(16,185,129,0.15)" : "none",
              }}>
                {/* Photo — fills the full card, bright and prominent */}
                <img src={demo.photo} alt="" style={{
                  position: "absolute", inset: 0, width: "100%", height: "100%",
                  objectFit: "cover", objectPosition: "center",
                  filter: "saturate(0.85) brightness(0.88)",
                  zIndex: 0,
                }} />

                {/* Gradient overlay — transparent top, dark bottom */}
                <div style={{
                  position: "absolute", inset: 0, zIndex: 1,
                  background: "linear-gradient(to top, rgba(0,0,0,0.94) 0%, rgba(0,0,0,0.6) 42%, rgba(0,0,0,0.08) 100%)",
                }} />

                {/* Trade label badge — top-left, over the photo */}
                <div style={{
                  position: "absolute", top: 20, left: 20, zIndex: 2,
                  background: "rgba(0,0,0,0.45)",
                  border: "1px solid rgba(255,255,255,0.18)",
                  backdropFilter: "blur(8px)",
                  borderRadius: 999,
                  padding: "5px 12px",
                  fontSize: 11, fontWeight: 700, letterSpacing: "0.08em",
                  textTransform: "uppercase" as const, color: "white",
                  display: "flex", alignItems: "center", gap: 6,
                }}>
                  <span style={{ color: "#34d399" }}>{demo.icon}</span>
                  {demo.trade}
                </div>

                {/* Bottom content — anchored to bottom over dark gradient */}
                <div style={{
                  position: "absolute", bottom: 0, left: 0, right: 0, zIndex: 2,
                  padding: "0 24px 24px",
                }}>
                  {/* Title */}
                  <div style={{ fontSize: 20, fontWeight: 800, color: "white", letterSpacing: "-0.03em", lineHeight: 1.2, marginBottom: 8 }}>
                    {demo.title}
                  </div>

                  {/* Description */}
                  <p style={{ fontSize: 13.5, color: "rgba(255,255,255,0.78)", lineHeight: 1.65, marginBottom: 18, margin: "0 0 18px" }}>
                    {demo.desc}
                  </p>

                  {/* Waveform */}
                  <div style={{ display: "flex", alignItems: "center", gap: 2, height: 28, marginBottom: 14 }}>
                    {wave.map((h, j) => (
                      <div key={j} style={{
                        flex: 1, height: `${Math.min(h, 24)}px`, borderRadius: 2,
                        background: isActive && (j / wave.length) < prog ? "#10b981" : "rgba(255,255,255,0.18)",
                        transition: "background 0.15s",
                        ...(isPlaying ? {
                          animationName: "wavePulse",
                          animationDuration: `${0.5 + (j % 8) * 0.09}s`,
                          animationTimingFunction: "ease-in-out",
                          animationIterationCount: "infinite",
                          animationDirection: "alternate",
                          animationDelay: `${(j * 0.04) % 0.8}s`,
                        } : {}),
                      }} />
                    ))}
                  </div>

                  {/* Button */}
                  <button
                    onClick={() => handlePlay(demo.id)}
                    style={{
                      width: "100%", padding: "13px 0",
                      borderRadius: 12, border: "none",
                      background: isPlaying ? "#10b981" : "rgba(255,255,255,0.95)",
                      color: isPlaying ? "#fff" : "#111",
                      fontSize: 14, fontWeight: 700,
                      cursor: "pointer",
                      display: "flex", alignItems: "center", justifyContent: "center", gap: 8,
                      transition: "all 0.18s ease",
                      fontFamily: "inherit", letterSpacing: "-0.01em",
                      boxShadow: "0 2px 16px rgba(0,0,0,0.3)",
                    }}
                  >
                    {isPlaying ? (
                      <>
                        <svg width="11" height="13" viewBox="0 0 11 13" fill="none">
                          <rect x="0" y="0" width="3.5" height="13" rx="1.5" fill="currentColor"/>
                          <rect x="7.5" y="0" width="3.5" height="13" rx="1.5" fill="currentColor"/>
                        </svg>
                        Pause
                      </>
                    ) : (
                      <>
                        <svg width="11" height="13" viewBox="0 0 11 13" fill="none">
                          <path d="M1 1l9 5.5-9 5.5V1z" fill="currentColor"/>
                        </svg>
                        {isActive ? "Resume" : "Hear Demo"}
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
