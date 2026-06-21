"use client";
import { useState, useEffect, useRef } from "react";

const DEMOS = [
  { id: "hvac",       label: "HVAC Service Call",   tag: "Residential AC repair · Austin, TX",  src: "/audio/hvac.mp3"       },
  { id: "plumbing",   label: "Plumbing Emergency",   tag: "Kitchen sink leak · getting worse",   src: "/audio/plumbing.mp3"   },
  { id: "electrical", label: "Electrical Emergency",  tag: "Power outage · storm damage",         src: "/audio/electrical.mp3" },
];

function makeWave(seed: number, n = 38): number[] {
  return Array.from({ length: n }, (_, i) =>
    Math.max(4, Math.round(
      Math.abs(Math.sin(i * 0.42 + seed) * 16 +
               Math.sin(i * 0.85 + seed * 1.7) * 9 + 6)
    ))
  );
}
const WAVES = DEMOS.map((_, i) => makeWave(i * 1.4 + 0.3));

export default function AudioDemo() {
  const [activeId, setActiveId]   = useState<string | null>(null);
  const [playing,  setPlaying]    = useState(false);
  const [progress, setProgress]   = useState(0);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const handlePlay = (demoId: string) => {
    if (activeId === demoId && audioRef.current) {
      if (playing) { audioRef.current.pause(); setPlaying(false); }
      else         { audioRef.current.play();  setPlaying(true);  }
      return;
    }
    if (audioRef.current) { audioRef.current.pause(); audioRef.current.src = ""; }

    const demo = DEMOS.find((d) => d.id === demoId);
    if (!demo) return;

    const audio = new Audio(demo.src);
    audioRef.current = audio;
    audio.addEventListener("timeupdate", () => {
      setProgress(audio.currentTime / (audio.duration || 1));
    });
    audio.addEventListener("ended", () => {
      setPlaying(false); setActiveId(null); setProgress(0);
    });
    setActiveId(demoId); setProgress(0);
    audio.play().then(() => setPlaying(true)).catch(() => {});
  };

  useEffect(() => () => { audioRef.current?.pause(); }, []);

  return (
    <div style={{ position: "relative", display: "flex", justifyContent: "center" }}>
      {/* Phone frame */}
      <div style={{
        width: 300,
        background: "#18181b",
        borderRadius: 50,
        padding: "10px 10px",
        boxShadow: "0 40px 80px rgba(0,0,0,0.22), 0 8px 24px rgba(0,0,0,0.12)",
      }}>
        {/* Screen */}
        <div style={{
          background: "#f9fafb",
          borderRadius: 42,
          overflow: "hidden",
          paddingBottom: 20,
        }}>
          {/* Status bar — no island */}
          <div style={{
            padding: "16px 22px 10px",
            display: "flex", justifyContent: "space-between", alignItems: "center",
          }}>
            <span style={{ fontSize: 13, fontWeight: 800, color: "#111" }}>9:41</span>
            <div style={{ display: "flex", alignItems: "center", gap: 5 }}>
              {/* Signal bars */}
              <div style={{ display: "flex", alignItems: "flex-end", gap: 1.5 }}>
                {[4, 6, 8, 10].map((h, i) => (
                  <div key={i} style={{ width: 3, height: h, borderRadius: 1.5, background: i < 3 ? "#111" : "#ccc" }} />
                ))}
              </div>
              {/* Wifi */}
              <svg width="15" height="11" viewBox="0 0 15 11" fill="none">
                <path d="M7.5 9a1 1 0 110 2 1 1 0 010-2z" fill="#111"/>
                <path d="M4.2 6.8a4.7 4.7 0 016.6 0" stroke="#111" strokeWidth="1.4" strokeLinecap="round" fill="none"/>
                <path d="M1.5 4.2a8.2 8.2 0 0112 0" stroke="#111" strokeWidth="1.4" strokeLinecap="round" fill="none" opacity="0.4"/>
              </svg>
              {/* Battery */}
              <svg width="22" height="11" viewBox="0 0 22 11" fill="none">
                <rect x=".5" y=".5" width="18" height="10" rx="2.5" stroke="#111" strokeOpacity=".35"/>
                <rect x="2" y="2" width="14" height="7" rx="1.5" fill="#111"/>
                <path d="M20 4v3a1.5 1.5 0 000-3z" fill="#111" opacity=".4"/>
              </svg>
            </div>
          </div>

          {/* Phone icon + heading */}
          <div style={{ textAlign: "center", padding: "10px 20px 20px" }}>
            <div style={{
              width: 54, height: 54, borderRadius: 16,
              background: "#10b981",
              display: "flex", alignItems: "center", justifyContent: "center",
              margin: "0 auto 14px",
              boxShadow: "0 4px 20px rgba(16,185,129,0.35)",
            }}>
              {/* Phone handset with signal arcs */}
              <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                <path d="M6.5 5C6.5 5 8 5 9.5 8.5C11 12 10 13 10 13L8 15C8 15 10 19 13 22L15 20C15 20 16 19 19.5 20.5C23 22 23 23.5 23 23.5V25.5C23 25.5 23 27 20 27C10 27 1 18 1 8C1 5 2.5 5 2.5 5H6.5Z" fill="white" opacity="0.92"/>
                <path d="M17 4C19.2 4.4 21.6 6.8 22 9" stroke="white" strokeWidth="1.8" strokeLinecap="round" opacity="0.7"/>
                <path d="M17 1C21.4 1.6 26.4 6.6 27 11" stroke="white" strokeWidth="1.8" strokeLinecap="round" opacity="0.4"/>
              </svg>
            </div>
            <div style={{ fontSize: 22, fontWeight: 900, color: "#111", letterSpacing: "-0.04em", lineHeight: 1, whiteSpace: "nowrap" }}>
              Hear Cleo in Action
            </div>
          </div>

          {/* Demo cards */}
          <div style={{ padding: "0 12px", display: "flex", flexDirection: "column", gap: 8 }}>
            {DEMOS.map((demo, di) => {
              const isActive  = activeId === demo.id;
              const isPlaying = isActive && playing;
              const wave      = WAVES[di];
              const prog      = isActive ? progress : 0;

              return (
                <div
                  key={demo.id}
                  onClick={() => handlePlay(demo.id)}
                  style={{
                    background: "white",
                    borderRadius: 16,
                    padding: "12px 14px",
                    border: isActive ? "1.5px solid rgba(16,185,129,0.3)" : "1.5px solid rgba(0,0,0,0.07)",
                    boxShadow: isActive ? "0 2px 12px rgba(16,185,129,0.12)" : "0 1px 4px rgba(0,0,0,0.05)",
                    transition: "all 0.18s ease",
                    cursor: "pointer",
                  }}
                >
                  {/* Label */}
                  <div style={{ marginBottom: 10 }}>
                    <div style={{ fontSize: 14.5, fontWeight: 800, color: "#111", letterSpacing: "-0.02em" }}>
                      {demo.label}
                    </div>
                    <div style={{ fontSize: 11.5, color: "#999", marginTop: 2 }}>{demo.tag}</div>
                  </div>

                  {/* Player row */}
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    {/* Play/pause circle */}
                    <div style={{
                      width: 30, height: 30, borderRadius: "50%", flexShrink: 0,
                      background: isActive ? "#10b981" : "#f0f0f0",
                      display: "flex", alignItems: "center", justifyContent: "center",
                      transition: "background 0.18s",
                      boxShadow: isActive ? "0 2px 8px rgba(16,185,129,0.35)" : "none",
                    }}>
                      {isPlaying ? (
                        <svg width="9" height="10" viewBox="0 0 9 10" fill="none">
                          <rect x="0" y="0" width="3" height="10" rx="1" fill="white"/>
                          <rect x="6" y="0" width="3" height="10" rx="1" fill="white"/>
                        </svg>
                      ) : (
                        <svg width="9" height="10" viewBox="0 0 9 10" fill="none">
                          <path d="M1 1l7 4-7 4V1z" fill={isActive ? "white" : "#555"}/>
                        </svg>
                      )}
                    </div>

                    {/* Waveform */}
                    <div style={{ display: "flex", alignItems: "center", gap: 1.5, height: 24, flex: 1 }}>
                      {wave.map((h, j) => {
                        const barFraction = j / wave.length;
                        const isPlayed   = isActive && barFraction < prog;
                        return (
                          <div
                            key={j}
                            style={{
                              flex: 1, height: `${Math.min(h, 22)}px`, borderRadius: 2,
                              background: isPlayed ? "#10b981" : isActive ? "#d1fae5" : "#e5e7eb",
                              transformOrigin: "center",
                              transition: "background 0.2s ease",
                              ...(isPlaying ? {
                                animationName: "wavePulse",
                                animationDuration: `${0.5 + (j % 8) * 0.09}s`,
                                animationTimingFunction: "ease-in-out",
                                animationIterationCount: "infinite",
                                animationDirection: "alternate",
                                animationDelay: `${(j * 0.038) % 0.8}s`,
                              } : {}),
                            }}
                          />
                        );
                      })}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <p style={{ textAlign: "center", fontSize: 10, color: "#999", marginTop: 12 }}>
            Tap a card to hear Cleo live
          </p>
        </div>
      </div>

    </div>
  );
}
