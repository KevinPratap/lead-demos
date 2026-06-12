#!/usr/bin/env node
/**
 * qr_pair.js — Capture WhatsApp QR code to file for manual scanning.
 * Run this, then open /home/prata/leads/data/wa_qr.txt to see the QR.
 */
const { makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys");
const P = require("pino");
const qrcode = require("qrcode-terminal");
const fs = require("fs");
const path = require("path");

const AUTH_DIR = path.join(__dirname, "..", "data", "wa_auth");
const QR_FILE = path.join(__dirname, "..", "data", "wa_qr.txt");

async function main() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  
  const sock = makeWASocket({
    auth: state,
    logger: P({ level: "silent" }),
    printQRInTerminal: true,
    browser: ["Kevin (Hermes)", "Chrome", "1.0"],
  });

  sock.ev.on("connection.update", (update) => {
    const { connection, qr } = update;
    if (qr) {
      // Capture QR to string and write to file
      let qrOutput = "";
      const origLog = console.log;
      console.log = (s) => { qrOutput += s + "\n"; };
      qrcode.generate(qr, { small: true });
      console.log = origLog;
      
      fs.writeFileSync(QR_FILE, qrOutput);
      console.log("✅ QR code written to data/wa_qr.txt");
      console.log("📱 Open WhatsApp on your phone → Settings → Linked Devices → Scan QR");
      console.log("   Then open the file above in another terminal or copy-paste the QR.");
    }
    if (connection === "open") {
      console.log("✅ WhatsApp paired successfully! Session saved.");
      console.log("   You can now Ctrl+C this process and use send_whatsapp.js");
      // Don't exit — let user close it
    }
    if (connection === "close") {
      console.log("⚠️ Connection closed. Restarting...");
    }
  });

  sock.ev.on("creds.update", saveCreds);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
