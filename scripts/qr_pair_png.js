#!/usr/bin/env node
const { makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys");
const P = require("pino");
const QRCode = require("qrcode");
const path = require("path");
const os = require("os");
const fs = require("fs");

const AUTH_DIR = path.join(os.homedir(), ".hermes", "wa_auth");
fs.mkdirSync(AUTH_DIR, { recursive: true });

(async () => {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  
  const sock = makeWASocket({
    auth: state,
    logger: P({ level: "silent" }),
    printQRInTerminal: false,
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", async ({ qr, connection }) => {
    if (qr) {
      console.log("Generating QR code...");
      const qrPath = path.join(os.homedir(), ".hermes", "wa_qr.png");
      await QRCode.toFile(qrPath, qr, { width: 500 });
      console.log("✅ QR saved to:", qrPath);
      console.log("Open this PNG and scan with WhatsApp");
      

      process.exit(0);
    }
    if (connection === "open") {
      console.log("Already authenticated");
      process.exit(0);
    }
    if (connection === "close") {
      console.log("Connection closed");
      process.exit(0);
    }
  });
})();
