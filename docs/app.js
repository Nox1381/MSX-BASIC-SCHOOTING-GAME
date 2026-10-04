/* This file boots the emulator. The game itself is entirely in ZOMBIE.BAS. */
"use strict";

const statusLine = document.getElementById("status");
const errorPanel = document.getElementById("error");
const reboot = document.getElementById("reboot");
const screenScale = () => Math.max(0.4, Math.min(1.4, (document.getElementById("wmsx-screen").clientWidth - 8) / (544 * 1.14)));
document.getElementById("retry").addEventListener("click", () => location.reload());
reboot.addEventListener("click", () => location.reload());
let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    if (!window.WMSX?.room) return;
    WMSX.SCREEN_DEFAULT_SCALE = screenScale();
    WMSX.room.screen.setDefaults();
  }, 150);
});

function fail() {
  statusLine.textContent = "Emulator unavailable";
  errorPanel.hidden = false;
  document.getElementById("loading")?.remove();
}

function boot() {
  if (!window.WMSX || !window.wmsx) return fail();
  // Parameters must be assigned AFTER the WebMSX script has loaded.
  Object.assign(WMSX, {
    AUTO_START: false,
    ALLOW_URL_PARAMETERS: false,
    MACHINE: "MSX1A",
    PRESETS: "DISK",
    DISKA_URL: new URL("game/ZOMBIE.DSK", location.href).href,
    FAST_BOOT: 1,
    AUTO_POWER_ON_DELAY: 0,
    SCREEN_ELEMENT_ID: "wmsx-screen",
    SCREEN_DEFAULT_SCALE: screenScale(),
    SCREEN_DEFAULT_ASPECT: 1.14,
    SCREEN_FULLSCREEN_MODE: 0,
    SCREEN_FILTER_MODE: 0,
    SCREEN_CRT_SCANLINES: 0,
    SCREEN_CONTROL_BAR: 1,
    AUDIO_MONITOR_BUFFER_BASE: 2,
    ENVIRONMENT: 83,
    JOYKEYS_MODE: -1,
    TOUCH_MODE: 0,
    // Accelerate ASCII program loading; restore the real clock at the title.
    Z80_CLOCK_MODE: 8,
    SPEED: 100,
  });
  try {
    document.getElementById("loading")?.remove();
    WMSX.start();
    statusLine.textContent = "Booting Disk BASIC…";
    let attempts = 0;
    const watch = setInterval(() => {
      attempts++;
      const text = WMSX.room?.machine?.vdp?.getScreenText() || "";
      if (text.includes("PRESS SPACE OR FIRE")) {
        WMSX.room.machine.setZ80ClockMode(1);
        statusLine.textContent = "Space to start · Click screen for sound";
        reboot.disabled = false;
        clearInterval(watch);
      } else if (/error|illegal function|syntax|overflow|out of memory/i.test(text) || attempts > 240) {
        clearInterval(watch);
        fail();
      }
    }, 250);
  } catch (error) {
    console.error(error);
    fail();
  }
}

// Upstream WebMSX 6.0.8 is an external dependency; no BIOS ROM is bundled here.
const script = document.createElement("script");
script.src = "https://cdn.jsdelivr.net/gh/ppeccin/WebMSX@4f4009e86d3e0bb9be7dcd7f0a582b0cd411d660/release/stable/6.0/embedded/wmsx.js";
script.crossOrigin = "anonymous";
script.integrity = "sha384-kNkyHYQgtc2n314hU9laE0OhE+HSJ4vgEDskx8nWjJpq+STHkpMzmjhQWG0XnIlH";
script.onload = boot;
script.onerror = fail;
document.head.appendChild(script);
