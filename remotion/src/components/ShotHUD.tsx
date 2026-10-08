import React, { useState, useEffect, useRef } from "react";
import ReactDOM from "react-dom";
import { Shot } from "../types/shot";
import { calculateSafeKenBurns } from "../utils/camera";

interface ShotHUDProps {
  shot: Shot;
  currentSec: number;
  onUpdateShot: (updated: Shot) => void;
  onResetShot: (shotId: number) => void;
  onExportAll: () => void;
  hasOverrides: boolean;
}

export const ShotHUD: React.FC<ShotHUDProps> = ({
  shot,
  currentSec,
  onUpdateShot,
  onResetShot,
  onExportAll,
  hasOverrides,
}) => {
  const [minimized, setMinimized] = useState(false);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<"zoom" | "pan" | "presets">("zoom");
  const [position, setPosition] = useState<{ x: number; y: number }>({ x: 280, y: 64 });
  const [isDragging, setIsDragging] = useState(false);

  const dragStartRef = useRef<{ mouseX: number; mouseY: number; startX: number; startY: number }>({
    mouseX: 0,
    mouseY: 0,
    startX: 280,
    startY: 64,
  });

  const { zoom, safeCx, safeCy } = calculateSafeKenBurns(shot, currentSec);

  // Dragging interaction
  const handleMouseDown = (e: React.MouseEvent) => {
    const target = e.target as HTMLElement;
    if (target.closest("button") || target.closest("input")) {
      return;
    }
    setIsDragging(true);
    dragStartRef.current = {
      mouseX: e.clientX,
      mouseY: e.clientY,
      startX: position.x,
      startY: position.y,
    };
  };

  useEffect(() => {
    if (!isDragging) return;
    const handleMouseMove = (e: MouseEvent) => {
      const dx = e.clientX - dragStartRef.current.mouseX;
      const dy = e.clientY - dragStartRef.current.mouseY;
      setPosition({
        x: Math.max(10, Math.min(window.innerWidth - 380, dragStartRef.current.startX + dx)),
        y: Math.max(10, Math.min(window.innerHeight - 150, dragStartRef.current.startY + dy)),
      });
    };
    const handleMouseUp = () => {
      setIsDragging(false);
    };
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isDragging]);

  const handleCopy = () => {
    const code = `{ id: ${shot.id}, image: "${shot.image}", start: ${shot.start.toFixed(2)}, end: ${shot.end.toFixed(2)}, zoomStart: ${shot.zoomStart.toFixed(2)}, zoomEnd: ${shot.zoomEnd.toFixed(2)}, cx1: ${shot.cx1.toFixed(2)}, cy1: ${shot.cy1.toFixed(2)}, cx2: ${shot.cx2.toFixed(2)}, cy2: ${shot.cy2.toFixed(2)}, title: "${shot.title}" },`;
    navigator.clipboard?.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const applyPreset = (preset: string) => {
    switch (preset) {
      case "center-zoom-in":
        onUpdateShot({
          ...shot,
          zoomStart: 1.05,
          zoomEnd: 1.25,
          cx1: 0.50, cy1: 0.50,
          cx2: 0.50, cy2: 0.50,
        });
        break;
      case "center-zoom-out":
        onUpdateShot({
          ...shot,
          zoomStart: 1.25,
          zoomEnd: 1.05,
          cx1: 0.50, cy1: 0.50,
          cx2: 0.50, cy2: 0.50,
        });
        break;
      case "subtle-push":
        onUpdateShot({
          ...shot,
          zoomStart: 1.00,
          zoomEnd: 1.08,
          cx1: 0.50, cy1: 0.50,
          cx2: 0.50, cy2: 0.50,
        });
        break;
      case "pan-left-to-right":
        onUpdateShot({
          ...shot,
          zoomStart: 1.18,
          zoomEnd: 1.18,
          cx1: 0.42, cy1: 0.50,
          cx2: 0.58, cy2: 0.50,
        });
        break;
      case "focus-subject-bottom":
        onUpdateShot({
          ...shot,
          zoomStart: 1.15,
          zoomEnd: 1.28,
          cx1: 0.50, cy1: 0.60,
          cx2: 0.50, cy2: 0.62,
        });
        break;
      case "focus-title-top":
        onUpdateShot({
          ...shot,
          zoomStart: 1.12,
          zoomEnd: 1.22,
          cx1: 0.50, cy1: 0.38,
          cx2: 0.50, cy2: 0.36,
        });
        break;
      case "static-flat":
        onUpdateShot({
          ...shot,
          zoomStart: 1.00,
          zoomEnd: 1.00,
          cx1: 0.50, cy1: 0.50,
          cx2: 0.50, cy2: 0.50,
        });
        break;
    }
  };

  // Only render interactive portal in browser environments
  if (typeof document === "undefined" || !document.body) {
    return null;
  }

  if (minimized) {
    return ReactDOM.createPortal(
      <button
        onClick={() => setMinimized(false)}
        style={{
          position: "fixed",
          top: position.y,
          left: position.x,
          backgroundColor: "rgba(10, 15, 26, 0.96)",
          color: "#00e5ff",
          border: "1px solid #00e5ff",
          borderRadius: 8,
          padding: "8px 16px",
          fontFamily: "Inter, -apple-system, sans-serif",
          fontSize: 13,
          fontWeight: 700,
          cursor: "pointer",
          zIndex: 999999,
          boxShadow: "0 6px 20px rgba(0, 0, 0, 0.8)",
          pointerEvents: "auto",
        }}
      >
        🎛️ Expand Camera (Shot #{shot.id})
      </button>,
      document.body
    );
  }

  const hudContent = (
    <div
      onMouseDown={handleMouseDown}
      style={{
        position: "fixed",
        top: position.y,
        left: position.x,
        width: 380,
        backgroundColor: "rgba(10, 15, 26, 0.95)",
        padding: "16px 18px",
        borderRadius: 12,
        border: "1px solid rgba(0, 229, 255, 0.45)",
        backdropFilter: "blur(14px)",
        color: "#ffffff",
        fontFamily: "Inter, -apple-system, sans-serif",
        fontSize: 13,
        display: "flex",
        flexDirection: "column",
        gap: 12,
        boxShadow: "0 16px 40px rgba(0, 0, 0, 0.85), 0 0 20px rgba(0, 229, 255, 0.2)",
        zIndex: 999999,
        userSelect: "none",
        pointerEvents: "auto",
        cursor: isDragging ? "grabbing" : "default",
      }}
    >
      {/* Header with Drag Handle */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", cursor: "grab" }}>
        <div>
          <div style={{ color: "#00e5ff", fontWeight: 800, fontSize: 13, textTransform: "uppercase", letterSpacing: "0.5px" }}>
            ⋮⋮ 🎬 Shot #{shot.id} • {shot.title}
          </div>
          <div style={{ color: "#94a3b8", fontSize: 11, marginTop: 2 }}>
            {shot.start.toFixed(2)}s – {shot.end.toFixed(2)}s (Active: <strong style={{ color: "#38bdf8" }}>{currentSec.toFixed(2)}s</strong>)
          </div>
        </div>
        <button
          onClick={() => setMinimized(true)}
          style={{
            background: "rgba(255, 255, 255, 0.08)",
            border: "1px solid rgba(255, 255, 255, 0.15)",
            borderRadius: 6,
            color: "#94a3b8",
            cursor: "pointer",
            fontSize: 18,
            width: 26,
            height: 26,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
          title="Minimize HUD"
        >
          &minus;
        </button>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: 6, borderBottom: "1px solid rgba(255,255,255,0.12)", paddingBottom: 8 }}>
        <button
          onClick={() => setActiveTab("zoom")}
          style={{
            backgroundColor: activeTab === "zoom" ? "#0284c7" : "rgba(255,255,255,0.06)",
            color: activeTab === "zoom" ? "#fff" : "#94a3b8",
            border: activeTab === "zoom" ? "1px solid #38bdf8" : "1px solid transparent",
            borderRadius: 6,
            padding: "5px 12px",
            fontSize: 12,
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          🔍 Zoom
        </button>
        <button
          onClick={() => setActiveTab("pan")}
          style={{
            backgroundColor: activeTab === "pan" ? "#0284c7" : "rgba(255,255,255,0.06)",
            color: activeTab === "pan" ? "#fff" : "#94a3b8",
            border: activeTab === "pan" ? "1px solid #38bdf8" : "1px solid transparent",
            borderRadius: 6,
            padding: "5px 12px",
            fontSize: 12,
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          🎯 Pan & Anchor
        </button>
        <button
          onClick={() => setActiveTab("presets")}
          style={{
            backgroundColor: activeTab === "presets" ? "#0284c7" : "rgba(255,255,255,0.06)",
            color: activeTab === "presets" ? "#fff" : "#94a3b8",
            border: activeTab === "presets" ? "1px solid #38bdf8" : "1px solid transparent",
            borderRadius: 6,
            padding: "5px 12px",
            fontSize: 12,
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          ⚡ Presets
        </button>
      </div>

      {/* Tab 1: Zoom Sliders */}
      {activeTab === "zoom" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 2 }}>
              <span>Zoom Start:</span>
              <strong style={{ color: "#38bdf8" }}>{shot.zoomStart.toFixed(2)}x</strong>
            </div>
            <input
              type="range"
              min="1.00"
              max="1.50"
              step="0.01"
              value={shot.zoomStart}
              onChange={(e) => onUpdateShot({ ...shot, zoomStart: parseFloat(e.target.value) })}
              style={{ width: "100%", accentColor: "#00e5ff", cursor: "pointer" }}
            />
          </div>

          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 2 }}>
              <span>Zoom End:</span>
              <strong style={{ color: "#38bdf8" }}>{shot.zoomEnd.toFixed(2)}x</strong>
            </div>
            <input
              type="range"
              min="1.00"
              max="1.50"
              step="0.01"
              value={shot.zoomEnd}
              onChange={(e) => onUpdateShot({ ...shot, zoomEnd: parseFloat(e.target.value) })}
              style={{ width: "100%", accentColor: "#00e5ff", cursor: "pointer" }}
            />
          </div>

          <div style={{ fontSize: 11, color: "#94a3b8", backgroundColor: "rgba(255,255,255,0.05)", padding: "6px 10px", borderRadius: 6 }}>
            Current Frame Scale: <strong style={{ color: "#38bdf8" }}>{zoom.toFixed(3)}x</strong> (clamped safe from black edges)
          </div>
        </div>
      )}

      {/* Tab 2: Pan & Anchor Sliders */}
      {activeTab === "pan" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 2 }}>
              <span>Focal Center X (Start &rarr; End):</span>
              <strong style={{ color: "#38bdf8" }}>{(shot.cx1 * 100).toFixed(0)}% &rarr; {(shot.cx2 * 100).toFixed(0)}%</strong>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <input
                type="range"
                min="0.20"
                max="0.80"
                step="0.01"
                value={shot.cx1}
                onChange={(e) => onUpdateShot({ ...shot, cx1: parseFloat(e.target.value) })}
                style={{ flex: 1, accentColor: "#00e5ff", cursor: "pointer" }}
                title="Start X"
              />
              <input
                type="range"
                min="0.20"
                max="0.80"
                step="0.01"
                value={shot.cx2}
                onChange={(e) => onUpdateShot({ ...shot, cx2: parseFloat(e.target.value) })}
                style={{ flex: 1, accentColor: "#00e5ff", cursor: "pointer" }}
                title="End X"
              />
            </div>
          </div>

          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 2 }}>
              <span>Focal Center Y (Start &rarr; End):</span>
              <strong style={{ color: "#38bdf8" }}>{(shot.cy1 * 100).toFixed(0)}% &rarr; {(shot.cy2 * 100).toFixed(0)}%</strong>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <input
                type="range"
                min="0.20"
                max="0.80"
                step="0.01"
                value={shot.cy1}
                onChange={(e) => onUpdateShot({ ...shot, cy1: parseFloat(e.target.value) })}
                style={{ flex: 1, accentColor: "#00e5ff", cursor: "pointer" }}
                title="Start Y"
              />
              <input
                type="range"
                min="0.20"
                max="0.80"
                step="0.01"
                value={shot.cy2}
                onChange={(e) => onUpdateShot({ ...shot, cy2: parseFloat(e.target.value) })}
                style={{ flex: 1, accentColor: "#00e5ff", cursor: "pointer" }}
                title="End Y"
              />
            </div>
          </div>

          <div style={{ fontSize: 11, color: "#94a3b8", backgroundColor: "rgba(255,255,255,0.05)", padding: "6px 10px", borderRadius: 6 }}>
            Auto Safe-Clamped: <strong style={{ color: "#38bdf8" }}>{(safeCx * 100).toFixed(1)}%, {(safeCy * 100).toFixed(1)}%</strong>
          </div>
        </div>
      )}

      {/* Tab 3: Quick Presets */}
      {activeTab === "presets" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
          <button onClick={() => applyPreset("subtle-push")} style={presetBtnStyle}>
            🎥 Subtle Push
          </button>
          <button onClick={() => applyPreset("center-zoom-in")} style={presetBtnStyle}>
            🔍 Punch Zoom In
          </button>
          <button onClick={() => applyPreset("center-zoom-out")} style={presetBtnStyle}>
            🔍 Pull Zoom Out
          </button>
          <button onClick={() => applyPreset("pan-left-to-right")} style={presetBtnStyle}>
            ➡️ Pan Left &rarr; Right
          </button>
          <button onClick={() => applyPreset("focus-subject-bottom")} style={presetBtnStyle}>
            🎯 Focus Subject
          </button>
          <button onClick={() => applyPreset("focus-title-top")} style={presetBtnStyle}>
            📝 Focus Title
          </button>
          <button onClick={() => applyPreset("static-flat")} style={presetBtnStyle}>
            ⏹️ Static Flat (1.0x)
          </button>
          <button onClick={() => onResetShot(shot.id)} style={{ ...presetBtnStyle, color: "#f87171", borderColor: "rgba(248, 113, 113, 0.4)" }}>
            🔄 Reset Shot
          </button>
        </div>
      )}

      {/* Action Footer */}
      <div style={{ display: "flex", gap: 8, paddingTop: 4, borderTop: "1px solid rgba(255,255,255,0.12)" }}>
        <button
          onClick={handleCopy}
          style={{
            flex: 1,
            backgroundColor: copied ? "#10b981" : "#0284c7",
            color: "#ffffff",
            border: "none",
            borderRadius: 6,
            padding: "8px 10px",
            fontSize: 12,
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          {copied ? "✓ Copied!" : "📋 Copy Shot Code"}
        </button>

        <button
          onClick={onExportAll}
          style={{
            flex: 1,
            backgroundColor: "rgba(255,255,255,0.1)",
            color: "#ffffff",
            border: "1px solid rgba(255,255,255,0.2)",
            borderRadius: 6,
            padding: "8px 10px",
            fontSize: 12,
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          📥 Copy All shots.ts
        </button>
      </div>
    </div>
  );

  return ReactDOM.createPortal(hudContent, document.body);
};

const presetBtnStyle: React.CSSProperties = {
  backgroundColor: "rgba(255, 255, 255, 0.08)",
  color: "#e2e8f0",
  border: "1px solid rgba(255, 255, 255, 0.15)",
  borderRadius: 6,
  padding: "8px 10px",
  fontSize: 12,
  fontWeight: 600,
  cursor: "pointer",
  textAlign: "center",
};
