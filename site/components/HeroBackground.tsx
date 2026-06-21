"use client";
import { useEffect, useRef } from "react";

// Stable params generated once — avoids hydration drift
const NUM_BARS = 90;
const BARS = Array.from({ length: NUM_BARS }, (_, i) => ({
  f1: 0.5 + ((i * 7 + 3) % 17) / 17 * 1.5,
  f2: 0.3 + ((i * 11 + 5) % 13) / 13 * 1.0,
  p1: ((i * 23) % 628) / 100,
  p2: ((i * 37 + 11) % 628) / 100,
  s:  0.22 + ((i * 5) % 11) / 11 * 0.45,
  amp: 0.06 + ((i * 13 + 7) % 19) / 19 * 0.22,
}));

const NUM_RINGS = 5;
const RINGS = Array.from({ length: NUM_RINGS }, (_, i) => ({
  offset: i / NUM_RINGS,
}));

export default function HeroBackground() {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let t = 0;

    const resize = () => {
      const dpr = window.devicePixelRatio || 1;
      canvas.width  = canvas.offsetWidth  * dpr;
      canvas.height = canvas.offsetHeight * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();
    window.addEventListener("resize", resize);

    const draw = () => {
      const W = canvas.offsetWidth;
      const H = canvas.offsetHeight;
      ctx.clearRect(0, 0, W, H);

      const time = t * 0.006;
      const midY  = H / 2;
      const barW  = W / NUM_BARS;

      // ── Audio spectrum bars ──────────────────────────────
      for (let i = 0; i < NUM_BARS; i++) {
        const b = BARS[i];
        const v = (
          Math.sin(time * b.s * b.f1 + b.p1) * 0.55 +
          Math.sin(time * b.s * 0.6 * b.f2 + b.p2) * 0.45
        ) * 0.5 + 0.5;

        const halfH = Math.max(4, v * H * b.amp + 7);

        // Fade bars on left third so headline stays clean
        const xFrac = i / NUM_BARS;
        const fade  = xFrac < 0.42 ? Math.pow(xFrac / 0.42, 2.2) : 1;
        const alpha = (0.08 + v * 0.21) * fade;

        ctx.fillStyle = `rgba(148,138,120,${alpha.toFixed(3)})`;
        ctx.fillRect(i * barW + 1.5, midY - halfH, barW - 3, halfH * 2);
      }

      // ── Signal rings (emit from product card position) ───
      const ringX  = W * 0.755;
      const ringY  = H * 0.50;
      const maxR   = W * 0.52;

      for (let r = 0; r < NUM_RINGS; r++) {
        const phase = ((t * 0.00022) + RINGS[r].offset) % 1;
        const radius = phase * maxR;
        const alpha  = (1 - phase) * 0.055;
        if (alpha < 0.001) continue;

        ctx.beginPath();
        ctx.arc(ringX, ringY, radius, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(16,185,129,${alpha.toFixed(3)})`;
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }

      t++;
      animId = requestAnimationFrame(draw);
    };

    draw();
    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <canvas
      ref={ref}
      style={{
        position: "absolute",
        inset: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
      }}
    />
  );
}
