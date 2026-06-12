#!/usr/bin/env node
const { makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys");
const P = require("pino");
const QRCode = require("qrcode");
const fs = require("fs");
const path = require("path");

const AUTH_DIR = path.join(__dirname, "..", "data", "wa_auth");
const QR_PNG = path.join(__dirname, "..", "data", "wa_qr.png");

async function main() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  
  const sock = makeWASocket({
    auth: state,
    logger: P({ level: "silent" }),
    browser: ["Kevin (Hermes)", "Chrome", "1.0"],
  });

  let paired = false;

  sock.ev.on("connection.update", async (update) => {
    const { connection, qr } = update;
    
    if (qr && !paired) {
      // Write QR as PNG image
      await QRCode.toFile(QR_PNG, qr, { 
        type: "png", 
        width: 500,
        margin: 2,
        color: { dark: "#000000", light: "#ffffff" }
      });
      console.log("✅ QR saved to data/wa_qr.png");
      console.log("📱 Open the file in Windows Explorer and scan with WhatsApp");
      console.log(`   Path: /mnt/c/Users/prata/leads/data/wa_qr.png`);
      console.log("   WhatsApp → Settings → Linked Devices → Link a Device");
    }
    
    if (connection === "open") {
      if (!paired) {
        paired = true;
        console.log("✅ WhatsApp paired! You can close this now (Ctrl+C).");
        console.log("   Session saved. Ready to auto-send from send_whatsapp.js");
      }
    }
    
    if (connection === "close" && !paired) {
      console.log("QR expired. Generating new one...");
    }
  });

  sock.ev.on("creds.update", saveCreds);
  
  // Keep alive
  await new Promise(() => {});
}

main().catch(err => { console.error("Fatal:", err); process.exit(1); });
