import React from "react";
import {
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const TechReel: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spring animation for main container entry
  const entrance = spring({
    frame,
    fps,
    config: {
      damping: 14,
      mass: 0.6,
      stiffness: 100,
    },
  });

  const cardScale = interpolate(entrance, [0, 1], [0.88, 1]);
  const cardOpacity = interpolate(entrance, [0, 1], [0, 1]);

  // Terminal Typing Animation Logic
  const cmd1 = "developer@global-edge:~$ npx wrangler pages deploy";
  const cmd2 = "developer@global-edge:~$ npx supabase db push";
  
  // Progressively type out text
  const t1 = Math.min(1, Math.max(0, (frame - 15) / 45));
  const chars1 = Math.floor(cmd1.length * t1);

  const t2 = Math.min(1, Math.max(0, (frame - 90) / 45));
  const chars2 = Math.floor(cmd2.length * t2);

  // Blinking cursor
  const showCursor = Math.floor(frame / 12) % 2 === 0;

  // Active Karaoke Word Highlighting
  const subtitleWords = [
    "Frontend", "ke", "liye", "istemaal", "karo", "Cloudflare", "Pages,",
    "jahan", "milti", "hai", "Unlimited", "Bandwidth", "aur", "zero", "cold", "start!"
  ];
  
  // Time window for subtitle (frame 20 to 280)
  const subProgress = Math.min(1, Math.max(0, (frame - 20) / 240));
  const activeWordIndex = Math.min(
    subtitleWords.length - 1,
    Math.floor(subProgress * subtitleWords.length)
  );

  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        background: "radial-gradient(circle at 50% 20%, #0F172A 0%, #080C14 100%)",
        color: "#F8FAFC",
        fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "70px 60px",
        boxSizing: "border-box",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Background Cyber Grid Accent */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage:
            "linear-gradient(rgba(0, 210, 255, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 210, 255, 0.04) 1px, transparent 1px)",
          backgroundSize: "80px 80px",
          pointerEvents: "none",
        }}
      />

      {/* TOP HUD BAR */}
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 10,
        }}
      >
        <div
          style={{
            background: "#FFD21E",
            color: "#0F172A",
            padding: "10px 24px",
            borderRadius: 14,
            fontWeight: 800,
            fontSize: 24,
            letterSpacing: "0.5px",
            boxShadow: "0 0 20px rgba(255, 210, 30, 0.3)",
          }}
        >
          // 01 · FRONTEND
        </div>

        <div
          style={{
            background: "rgba(15, 23, 42, 0.8)",
            border: "2px solid #00D2FF",
            color: "#00D2FF",
            padding: "10px 24px",
            borderRadius: 14,
            fontWeight: 700,
            fontSize: 24,
            boxShadow: "0 0 20px rgba(0, 210, 255, 0.2)",
          }}
        >
          ₹0 FULL-STACK ARCHITECTURE
        </div>

        <div
          style={{
            background: "rgba(30, 41, 59, 0.8)",
            border: "1px solid #64748B",
            color: "#E2E8F0",
            padding: "10px 20px",
            borderRadius: 14,
            fontWeight: 600,
            fontSize: 22,
          }}
        >
          STEP 1/3
        </div>
      </div>

      {/* MAIN ANIMATED CARD (Spring Easing) */}
      <div
        style={{
          width: "100%",
          transform: `scale(${cardScale})`,
          opacity: cardOpacity,
          display: "flex",
          flexDirection: "column",
          gap: 30,
          zIndex: 10,
        }}
      >
        {/* Title Header */}
        <div
          style={{
            background: "rgba(13, 27, 28, 0.85)",
            border: "2px solid #00E599",
            borderRadius: 28,
            padding: "40px",
            boxShadow: "0 20px 50px rgba(0, 229, 153, 0.15)",
          }}
        >
          <div
            style={{
              display: "inline-block",
              background: "#00E599",
              color: "#0B1120",
              fontWeight: 800,
              fontSize: 20,
              padding: "6px 18px",
              borderRadius: 8,
              marginBottom: 16,
            }}
          >
            FRONTEND PLATFORM
          </div>
          <div
            style={{
              fontSize: 48,
              fontWeight: 900,
              color: "#FFFFFF",
              letterSpacing: "-0.5px",
              marginBottom: 8,
            }}
          >
            CLOUDFLARE PAGES
          </div>
          <div style={{ fontSize: 26, color: "#94A3B8" }}>
            The 0ms Cold Start Architecture (100% Free Forever)
          </div>
        </div>

        {/* macOS TERMINAL (High-Tech Remotion Style) */}
        <div
          style={{
            background: "#0A0E17",
            border: "2px solid #1E293B",
            borderRadius: 24,
            overflow: "hidden",
            boxShadow: "0 25px 60px rgba(0, 0, 0, 0.6)",
          }}
        >
          {/* Mac Header */}
          <div
            style={{
              background: "#111827",
              padding: "18px 24px",
              display: "flex",
              alignItems: "center",
              borderBottom: "1px solid #1F2937",
            }}
          >
            <div style={{ display: "flex", gap: 10 }}>
              <div style={{ width: 18, height: 18, borderRadius: "50%", background: "#FF5F56" }} />
              <div style={{ width: 18, height: 18, borderRadius: "50%", background: "#FFBD2E" }} />
              <div style={{ width: 18, height: 18, borderRadius: "50%", background: "#27C93F" }} />
            </div>
            <div
              style={{
                marginLeft: 24,
                fontFamily: "Consolas, monospace",
                fontSize: 22,
                color: "#94A3B8",
              }}
            >
              bash - developer@global-edge (80x24)
            </div>
          </div>

          {/* Terminal Body */}
          <div
            style={{
              padding: "36px",
              fontFamily: "Consolas, 'Courier New', monospace",
              fontSize: 30,
              lineHeight: 1.6,
              color: "#00E599",
            }}
          >
            {/* Command 1 */}
            <div>
              {cmd1.slice(0, chars1)}
              {frame >= 15 && frame < 90 && showCursor && (
                <span style={{ color: "#00E599", marginLeft: 4 }}>█</span>
              )}
            </div>

            {/* Output 1 */}
            {frame >= 60 && (
              <div style={{ color: "#E2E8F0", marginTop: 12, fontSize: 26 }}>
                [✓] 32 Static chunks built & compressed (0ms cache)
              </div>
            )}

            {/* Command 2 */}
            {frame >= 90 && (
              <div style={{ marginTop: 24, color: "#00E599" }}>
                {cmd2.slice(0, chars2)}
                {frame >= 90 && frame < 150 && showCursor && (
                  <span style={{ color: "#00E599", marginLeft: 4 }}>█</span>
                )}
              </div>
            )}

            {/* Output 2 */}
            {frame >= 135 && (
              <div style={{ color: "#E2E8F0", marginTop: 12, fontSize: 26 }}>
                [✓] Connected to Serverless PostgreSQL (500MB Free)
              </div>
            )}

            {/* Final Live Deploy Status Box */}
            {frame >= 160 && (
              <div
                style={{
                  marginTop: 30,
                  background: "rgba(0, 229, 153, 0.08)",
                  border: "2px solid #00E599",
                  borderRadius: 16,
                  padding: "24px 30px",
                  color: "#FFFFFF",
                }}
              >
                <div style={{ color: "#00E599", fontWeight: 800, fontSize: 32 }}>
                  🚀 STATUS: LIVE ON GLOBAL EDGE
                </div>
                <div style={{ color: "#00D2FF", fontSize: 26, marginTop: 8 }}>
                  ⚡ Cold Start: 0ms  |  Regions: 330+ Cities
                </div>
                <div style={{ color: "#FFD21E", fontWeight: 800, fontSize: 28, marginTop: 8 }}>
                  💰 Total Cost: $0.00 / Lifetime
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 3 Metrics Pill Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 20,
          }}
        >
          <div
            style={{
              background: "rgba(15, 23, 42, 0.9)",
              border: "1px solid #334155",
              borderRadius: 20,
              padding: "24px",
            }}
          >
            <div style={{ color: "#94A3B8", fontSize: 20, fontWeight: 700 }}>BANDWIDTH</div>
            <div style={{ color: "#00E599", fontSize: 32, fontWeight: 900, marginTop: 6 }}>
              UNLIMITED
            </div>
            <div style={{ color: "#64748B", fontSize: 18, marginTop: 4 }}>100% Free Forever</div>
          </div>

          <div
            style={{
              background: "rgba(15, 23, 42, 0.9)",
              border: "1px solid #334155",
              borderRadius: 20,
              padding: "24px",
            }}
          >
            <div style={{ color: "#94A3B8", fontSize: 20, fontWeight: 700 }}>LATENCY</div>
            <div style={{ color: "#00D2FF", fontSize: 32, fontWeight: 900, marginTop: 6 }}>
              0ms DELAY
            </div>
            <div style={{ color: "#64748B", fontSize: 18, marginTop: 4 }}>No Spin-Down Sleep</div>
          </div>
        </div>
      </div>

      {/* DYNAMIC SUBTITLE KARAOKE BAR (Zero Overflow, Responsive Flexbox) */}
      <div
        style={{
          width: "100%",
          background: "rgba(11, 17, 32, 0.92)",
          border: "2px solid #00E599",
          borderRadius: 24,
          padding: "28px 36px",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "10px 14px",
          boxSizing: "border-box",
          boxShadow: "0 15px 40px rgba(0, 0, 0, 0.7)",
          zIndex: 10,
        }}
      >
        {subtitleWords.map((word, idx) => {
          const isActive = idx === activeWordIndex;
          return (
            <span
              key={idx}
              style={{
                fontSize: 34,
                fontWeight: 800,
                color: isActive ? "#0F172A" : "#FFFFFF",
                background: isActive ? "#FFD21E" : "transparent",
                padding: isActive ? "4px 12px" : "4px 0px",
                borderRadius: 8,
                transition: "all 0.1s ease",
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
