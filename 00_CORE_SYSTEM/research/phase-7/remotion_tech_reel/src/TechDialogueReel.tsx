import React from "react";
import {
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Img,
} from "remotion";
import metadata from "./dialogue_metadata.json";

export const TechDialogueReel: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // Determine active speaker turn
  const activeTurn =
    metadata.turns.find(
      (t) => currentTime >= t.start && currentTime < t.end
    ) || metadata.turns[0];

  const isArjunSpeaking = activeTurn.speaker === "ARJUN";
  const isKabirSpeaking = activeTurn.speaker === "KABIR";

  // Spring animations for speakers taking turns
  const arjunSpring = spring({
    frame: frame - Math.floor(activeTurn.start * fps),
    fps,
    config: { damping: 14, mass: 0.5 },
  });

  const kabirSpring = spring({
    frame: frame - Math.floor(activeTurn.start * fps),
    fps,
    config: { damping: 14, mass: 0.5 },
  });

  // Breathing oscillation
  const breath = Math.sin(frame * 0.1) * 3;

  // Subtitle words and karaoke progress
  const subtitleWords = activeTurn.subtitle.split(" ");
  const turnElapsed = Math.max(0, currentTime - activeTurn.start);
  const turnProgress = Math.min(1, turnElapsed / activeTurn.duration);
  const activeWordIdx = Math.min(
    subtitleWords.length - 1,
    Math.floor(turnProgress * subtitleWords.length)
  );

  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        background: "radial-gradient(circle at 50% 15%, #0F172A 0%, #070A11 100%)",
        color: "#F8FAFC",
        fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "60px 50px 80px 50px",
        boxSizing: "border-box",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Background Cyber Grid */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage:
            "linear-gradient(rgba(0, 210, 255, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 210, 255, 0.04) 1px, transparent 1px)",
          backgroundSize: "75px 75px",
          pointerEvents: "none",
        }}
      />

      {/* TOP HEADER HUD */}
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
            padding: "8px 22px",
            borderRadius: 12,
            fontWeight: 800,
            fontSize: 22,
            boxShadow: "0 0 20px rgba(255, 210, 30, 0.3)",
          }}
        >
          // DEV PODCAST · 01
        </div>

        <div
          style={{
            background: "rgba(15, 23, 42, 0.85)",
            border: "2px solid #00D2FF",
            color: "#00D2FF",
            padding: "8px 22px",
            borderRadius: 12,
            fontWeight: 700,
            fontSize: 22,
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
            padding: "8px 18px",
            borderRadius: 12,
            fontWeight: 600,
            fontSize: 20,
          }}
        >
          2026 EDITION
        </div>
      </div>

      {/* 2-SPEAKER PODCAST STAGE (Arjun on Left, Dr. Kabir on Right) */}
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-around",
          alignItems: "center",
          marginTop: 20,
          zIndex: 10,
        }}
      >
        {/* SPEAKER 1: ARJUN (JUNIOR DEV) */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            transform: isArjunSpeaking ? `scale(1.06) translateY(${breath}px)` : "scale(0.92)",
            opacity: isArjunSpeaking ? 1 : 0.45,
            transition: "all 0.25s ease",
          }}
        >
          <div
            style={{
              width: 220,
              height: 220,
              borderRadius: "50%",
              border: isArjunSpeaking ? "4px solid #00E599" : "2px solid #334155",
              boxShadow: isArjunSpeaking ? "0 0 35px rgba(0, 229, 153, 0.45)" : "none",
              overflow: "hidden",
              background: "#1E293B",
              display: "flex",
              justifyContent: "center",
              alignItems: "flex-end",
            }}
          >
            <Img
              src={staticFile(
                isArjunSpeaking
                  ? `characters/bust_${activeTurn.char_img}`
                  : "characters/bust_arjun_pointing.png"
              )}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                objectPosition: "top center",
              }}
            />
          </div>
          <div
            style={{
              marginTop: 14,
              background: isArjunSpeaking ? "#00E599" : "rgba(30, 41, 59, 0.8)",
              color: isArjunSpeaking ? "#0F172A" : "#94A3B8",
              padding: "6px 18px",
              borderRadius: 10,
              fontWeight: 800,
              fontSize: 20,
              letterSpacing: "0.5px",
            }}
          >
            {isArjunSpeaking ? "🎙️ ARJUN (JUNIOR DEV)" : "ARJUN"}
          </div>
        </div>

        {/* VS / CONVERSATION INDICATOR */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            opacity: 0.6,
          }}
        >
          <div
            style={{
              width: 44,
              height: 44,
              borderRadius: "50%",
              background: "rgba(15, 23, 42, 0.9)",
              border: "1px solid #475569",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontWeight: 900,
              fontSize: 18,
              color: "#94A3B8",
            }}
          >
            💬
          </div>
        </div>

        {/* SPEAKER 2: KABIR (SENIOR ARCHITECT) */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            transform: isKabirSpeaking ? `scale(1.06) translateY(${breath}px)` : "scale(0.92)",
            opacity: isKabirSpeaking ? 1 : 0.45,
            transition: "all 0.25s ease",
          }}
        >
          <div
            style={{
              width: 220,
              height: 220,
              borderRadius: "50%",
              border: isKabirSpeaking ? "4px solid #FFD21E" : "2px solid #334155",
              boxShadow: isKabirSpeaking ? "0 0 35px rgba(255, 210, 30, 0.45)" : "none",
              overflow: "hidden",
              background: "#1E293B",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <Img
              src={staticFile(
                isKabirSpeaking
                  ? `characters/bust_${activeTurn.char_img}`
                  : "characters/bust_dr_kabir_explaining.png"
              )}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                objectPosition: "top center",
              }}
            />
          </div>
          <div
            style={{
              marginTop: 14,
              background: isKabirSpeaking ? "#FFD21E" : "rgba(30, 41, 59, 0.8)",
              color: isKabirSpeaking ? "#0F172A" : "#94A3B8",
              padding: "6px 18px",
              borderRadius: 10,
              fontWeight: 800,
              fontSize: 20,
              letterSpacing: "0.5px",
            }}
          >
            {isKabirSpeaking ? "🎙️ DR. KABIR (ARCHITECT)" : "DR. KABIR"}
          </div>
        </div>
      </div>

      {/* DYNAMIC TECH SHOWCASE CONTAINER (Changes with Conversation Context) */}
      <div
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          gap: 24,
          zIndex: 10,
        }}
      >
        {activeTurn.id === "turn1_arjun" && (
          /* TURN 1: ARJUN'S AWS BILL PANIC */
          <div
            style={{
              background: "rgba(25, 18, 28, 0.9)",
              border: "2px solid #EF4444",
              borderRadius: 24,
              padding: "36px",
              boxShadow: "0 20px 50px rgba(239, 68, 68, 0.2)",
            }}
          >
            <div
              style={{
                display: "inline-block",
                background: "#EF4444",
                color: "#FFFFFF",
                fontWeight: 800,
                fontSize: 18,
                padding: "6px 16px",
                borderRadius: 8,
                marginBottom: 14,
              }}
            >
              CRITICAL BILLING ALERT
            </div>
            <div style={{ fontSize: 44, fontWeight: 900, color: "#FFFFFF", marginBottom: 8 }}>
              AWS SURPRISE BILL: $40.00
            </div>
            <div style={{ fontSize: 24, color: "#FCA5A5", lineHeight: 1.5 }}>
              ⚠️ Credit card auto-debited for idle RDS & EC2 instances!
            </div>
            <div
              style={{
                marginTop: 20,
                background: "rgba(0, 0, 0, 0.4)",
                borderRadius: 14,
                padding: "16px 22px",
                border: "1px solid rgba(239, 68, 68, 0.4)",
                fontSize: 22,
                color: "#FECACA",
              }}
            >
              Junior Dev Mistake: Using enterprise cloud for personal student projects.
            </div>
          </div>
        )}

        {activeTurn.id === "turn2_kabir" && (
          /* TURN 2: KABIR REVEALS THE ₹0 PRODUCTION STACK */
          <div
            style={{
              background: "#0A0E17",
              border: "2px solid #00E599",
              borderRadius: 24,
              overflow: "hidden",
              boxShadow: "0 20px 50px rgba(0, 229, 153, 0.2)",
            }}
          >
            {/* Mac Header */}
            <div
              style={{
                background: "#111827",
                padding: "14px 20px",
                display: "flex",
                alignItems: "center",
                borderBottom: "1px solid #1F2937",
              }}
            >
              <div style={{ display: "flex", gap: 8 }}>
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#FF5F56" }} />
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#FFBD2E" }} />
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#27C93F" }} />
              </div>
              <div
                style={{
                  marginLeft: 18,
                  fontFamily: "Consolas, monospace",
                  fontSize: 20,
                  color: "#94A3B8",
                }}
              >
                bash - kabir@production-edge (80x24)
              </div>
            </div>

            <div
              style={{
                padding: "28px",
                fontFamily: "Consolas, monospace",
                fontSize: 26,
                lineHeight: 1.6,
                color: "#00E599",
              }}
            >
              <div>developer@edge:~$ npx wrangler pages deploy</div>
              <div style={{ color: "#E2E8F0", fontSize: 22, marginTop: 6 }}>
                [✓] Cloudflare Pages: 0ms Edge Latency (Unlimited Free)
              </div>
              <div style={{ marginTop: 14, color: "#00E599" }}>
                developer@edge:~$ npx supabase db push
              </div>
              <div style={{ color: "#E2E8F0", fontSize: 22, marginTop: 6 }}>
                [✓] Supabase: Serverless PostgreSQL (500MB Free Forever)
              </div>
              <div
                style={{
                  marginTop: 20,
                  background: "rgba(0, 229, 153, 0.1)",
                  border: "1px solid #00E599",
                  borderRadius: 12,
                  padding: "16px 20px",
                  color: "#FFFFFF",
                }}
              >
                <div style={{ color: "#00E599", fontWeight: 800, fontSize: 26 }}>
                  🚀 2026 ARCHITECTURE: $0 / LIFETIME
                </div>
                <div style={{ color: "#00D2FF", fontSize: 20, marginTop: 4 }}>
                  Zero surprise bills + Zero cold start delay
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTurn.id === "turn3_arjun" && (
          /* TURN 3: ARJUN'S QUESTION (HOW TO KEEP AWAKE?) */
          <div
            style={{
              background: "rgba(15, 25, 45, 0.9)",
              border: "2px solid #00D2FF",
              borderRadius: 24,
              padding: "36px",
              boxShadow: "0 20px 50px rgba(0, 210, 255, 0.2)",
            }}
          >
            <div
              style={{
                display: "inline-block",
                background: "#00D2FF",
                color: "#0B1120",
                fontWeight: 800,
                fontSize: 18,
                padding: "6px 16px",
                borderRadius: 8,
                marginBottom: 14,
              }}
            >
              THE BIGGEST QUESTION
            </div>
            <div style={{ fontSize: 40, fontWeight: 900, color: "#FFFFFF", marginBottom: 8 }}>
              HOW TO KEEP FREE SERVERS ALIVE?
            </div>
            <div style={{ fontSize: 24, color: "#93C5FD", lineHeight: 1.5 }}>
              ❓ "Render ya free backends 15 minute mein so jaate hain. Recruiter ko portfolio kaise dikhayen?"
            </div>
          </div>
        )}

        {activeTurn.id === "turn4_kabir" && (
          /* TURN 4: KABIR'S 24/7 PING HACK & VIRAL CTA */
          <div
            style={{
              background: "rgba(22, 18, 38, 0.9)",
              border: "2px solid #A855F7",
              borderRadius: 24,
              padding: "36px",
              boxShadow: "0 20px 50px rgba(168, 85, 247, 0.2)",
            }}
          >
            <div
              style={{
                display: "inline-block",
                background: "#A855F7",
                color: "#FFFFFF",
                fontWeight: 800,
                fontSize: 18,
                padding: "6px 16px",
                borderRadius: 8,
                marginBottom: 14,
              }}
            >
              THE 24/7 KEEP-ALIVE HACK
            </div>
            <div style={{ fontSize: 36, fontWeight: 900, color: "#FFFFFF", marginBottom: 6 }}>
              cron-job.org + 10-Min HTTP Ping
            </div>
            <div style={{ fontSize: 22, color: "#CBD5E1", marginBottom: 20 }}>
              Server stays 100% hot & active 24/7/365 without sleeping!
            </div>

            <div
              style={{
                background: "#00E599",
                color: "#0B1120",
                padding: "16px 24px",
                borderRadius: 14,
                fontWeight: 900,
                fontSize: 28,
                textAlign: "center",
                boxShadow: "0 0 30px rgba(0, 229, 153, 0.4)",
              }}
            >
              COMMENT "STACK" FOR FULL REPO
            </div>
          </div>
        )}

        {/* 2 STATIC METRIC PILLS */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 16,
          }}
        >
          <div
            style={{
              background: "rgba(15, 23, 42, 0.8)",
              border: "1px solid #334155",
              borderRadius: 16,
              padding: "18px 24px",
            }}
          >
            <div style={{ color: "#94A3B8", fontSize: 16, fontWeight: 700 }}>MONTHLY BILL</div>
            <div style={{ color: "#00E599", fontSize: 28, fontWeight: 900, marginTop: 4 }}>
              ₹0 FOREVER
            </div>
          </div>

          <div
            style={{
              background: "rgba(15, 23, 42, 0.8)",
              border: "1px solid #334155",
              borderRadius: 16,
              padding: "18px 24px",
            }}
          >
            <div style={{ color: "#94A3B8", fontSize: 16, fontWeight: 700 }}>COLD START DELAY</div>
            <div style={{ color: "#00D2FF", fontSize: 28, fontWeight: 900, marginTop: 4 }}>
              0ms (GLOBAL)
            </div>
          </div>
        </div>
      </div>

      {/* DYNAMIC CONVERSATION SUBTITLE BOX WITH ACTIVE SPEAKER TAG */}
      <div
        style={{
          width: "100%",
          background: "rgba(11, 17, 32, 0.95)",
          border: `2px solid ${activeTurn.badge_color}`,
          borderRadius: 24,
          padding: "24px 30px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 14,
          boxSizing: "border-box",
          boxShadow: `0 15px 40px ${activeTurn.badge_color}33`,
          zIndex: 10,
        }}
      >
        {/* Active Speaker Badge */}
        <div
          style={{
            background: activeTurn.badge_color,
            color: "#0F172A",
            padding: "4px 16px",
            borderRadius: 8,
            fontWeight: 800,
            fontSize: 18,
            letterSpacing: "0.5px",
          }}
        >
          [ {activeTurn.speaker} · {activeTurn.role} ]
        </div>

        {/* Karaoke Words Flow */}
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "8px 12px",
          }}
        >
          {subtitleWords.map((word, idx) => {
            const isActive = idx === activeWordIdx;
            return (
              <span
                key={idx}
                style={{
                  fontSize: 32,
                  fontWeight: 800,
                  color: isActive ? "#0F172A" : "#FFFFFF",
                  background: isActive ? "#FFD21E" : "transparent",
                  padding: isActive ? "2px 10px" : "2px 0px",
                  borderRadius: 6,
                  transition: "all 0.1s ease",
                }}
              >
                {word}
              </span>
            );
          })}
        </div>
      </div>
    </div>
  );
};
