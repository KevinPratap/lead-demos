#!/usr/bin/env node
/**
 * send_whatsapp.js — Send WhatsApp messages via Baileys (WebSocket, no browser).
 *
 * FIRST RUN: QR code appears in terminal. Scan with WhatsApp mobile app.
 * Session saved to ../data/wa_auth/ — survives reboots.
 *
 * USAGE:
 *   node scripts/send_whatsapp.js                    → interactive mode
 *   node scripts/send_whatsapp.js --to 919820854665 --msg "Hi from Kevin"
 *   node scripts/send_whatsapp.js --lead "Dr Merchant's Dental Clinic" --url "https://..."
 */

const {
  makeWASocket,
  useMultiFileAuthState,
  DisconnectReason,
  makeInMemoryStore,
} = require("@whiskeysockets/baileys");
const P = require("pino");
const qrcode = require("qrcode-terminal");
const fs = require("fs");
const path = require("path");
const sqlite3 = require("better-sqlite3");

// ── Config ──────────────────────────────────────────────────────────
const AUTH_DIR = path.join(__dirname, "..", "data", "wa_auth");
const DB_PATH = path.join(__dirname, "..", "data", "leads.db");
const LOG_INDEX = path.join(__dirname, "..", "data", "wa_sent.json");

// ── CLI parsing ─────────────────────────────────────────────────────
const args = {};
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i] === "--to") args.to = process.argv[++i];
  else if (process.argv[i] === "--msg") args.msg = process.argv[++i];
  else if (process.argv[i] === "--lead") args.lead = process.argv[++i];
  else if (process.argv[i] === "--url") args.demo_url = process.argv[++i];
  else if (process.argv[i] === "--list") args.list = true;
}

// ── Lead lookup ─────────────────────────────────────────────────────
function findLead(nameOrPhone) {
  try {
    const db = sqlite3(DB_PATH, { readonly: true });
    const digits = nameOrPhone.replace(/[^0-9]/g, "");
    
    // Only use phone filter if there are actual digits
    let lead;
    if (digits.length > 0) {
      lead = db.prepare(
        `SELECT place_id, name, phone, rating, reviews, category FROM leads 
         WHERE name LIKE ? OR phone LIKE ? 
         ORDER BY CASE WHEN name LIKE ? THEN 0 ELSE 1 END
         LIMIT 1`
      ).get(`%${nameOrPhone}%`, `%${digits}%`, `%${nameOrPhone}%`);
    } else {
      // Name-only search with exact priority
      lead = db.prepare(
        `SELECT place_id, name, phone, rating, reviews, category FROM leads 
         WHERE name LIKE ?
         ORDER BY CASE WHEN name = ? THEN 0 ELSE 1 END, reviews DESC
         LIMIT 1`
      ).get(`%${nameOrPhone}%`, nameOrPhone);
    }
    
    db.close();
    return lead;
  } catch {
    return null;
  }
}

function composeWhatsAppMessage(lead, demo_url) {
  const name = lead.name;
  const rating = lead.rating || 5.0;
  const reviews = lead.reviews || 50;
  const r = (arr) => arr[Math.floor(Math.random() * arr.length)];
  // Extract actual area/neighborhood from messy Indian address, not street number
  const area = (() => {
    const addr = lead.address || "";
    const parts = addr.split(",").map(s => s.trim()).filter(Boolean);
    for (const p of parts) {
      if (!/^\d/.test(p) && p.length > 3 && !/floor|shop|flat|apt|unit|suite/i.test(p)) {
        return p;
      }
    }
    return "Mumbai";
  })();

  // Real human cadence — not a template with swapped words.
  // Every message varies STRUCTURE, not just vocabulary.
  // Some are 2 lines, some 4. Some lead with the compliment, some with intro.
  // No em dashes. No forced casual ("thats insane", "ngl"). Just natural.

  const isHigh = reviews >= 100;
  const isMid = reviews >= 30 && reviews < 100;

  // ── opening lines (sometimes combined with found, sometimes standalone) ──
  const intros = [
    `kevin here. web dev student in mumbai.`,
    `hey, kevin here. i build sites for local businesses.`,
    `kevin here, student web dev.`,
    `hey. kevin, web dev student.`,
    `kevin. im a student, i build websites on the side.`,
  ];

  // ── the discovery + compliment — this is where personality lives ──
  const foundHigh = [
    `came across ${name} on maps. ${rating} stars with ${reviews} reviews is proper impressive.`,
    `saw ${name} on google maps. ${reviews} reviews at ${rating} stars, people clearly rate you.`,
    `was looking at clinics in ${area} and ${name} stood out. ${rating} stars, ${reviews} reviews.`,
    `${name} caught my eye on maps. ${rating} stars and ${reviews} reviews is no joke.`,
  ];
  const foundMid = [
    `found ${name} on maps. ${rating} stars, ${reviews} reviews. solid.`,
    `came across ${name} while browsing ${area}. ${rating} stars, people seem to love it.`,
    `${name} — saw it on maps. ${rating} stars with ${reviews} reviews.`,
  ];
  const foundLow = [
    `saw ${name} on maps.`,
    `found ${name} in ${area}.`,
    `came across ${name} on google maps.`,
  ];

  // ── the action — sometimes merged with found, sometimes its own line ──
  const actions = [
    `noticed no website so i made one from your profile.`,
    `you dont have a site, so i built a quick one.`,
    `no website. threw a preview together from your listing.`,
    `saw there was no site so i put something together.`,
  ];

  // ── the close — sometimes present, sometimes absent (link IS the close) ──
  const closes = [
    `no catch. like it? we talk. dont? no worries.`,
    `no strings. if youre interested we can chat, if not all good.`,
    `not selling anything. just thought you should see it.`,
    `zero pressure. take a look, if you like it lets talk.`,
  ];

  const found = isHigh ? r(foundHigh) : isMid ? r(foundMid) : r(foundLow);

  // STRUCTURE VARIATION — this is the key. different shapes, not just different words.
  const structure = r([
    // A: intro + found + action + close + link (full — for high-review leads)
    () => `${r(intros)}\n${found}\n${r(actions)}\n${r(closes)}\n${demo_url}`,
    // B: intro merged with found + action + link (compact)
    () => `${r(intros)} ${found}\n${r(actions)}\n${demo_url}`,
    // C: compliment-first + intro + action + link (lead with the hook)
    () => `${found}\n${r(intros)} ${r(actions)}\n${demo_url}`,
    // D: ultra-short — for low-review leads or when keeping it minimal
    () => `${r(intros)} ${found} no website, built you a preview.\n${demo_url}`,
    // E: action-first + close + link (cut to the chase)
    () => `${r(actions)} ${found}\n${r(closes)}\n${demo_url}`,
  ]);

  return structure();
}

function logSent(phone, leadName, message, success) {
  const log = { phone, lead: leadName, message, sent_at: new Date().toISOString(), success };
  let entries = [];
  try {
    entries = JSON.parse(fs.readFileSync(LOG_INDEX, "utf-8"));
  } catch {}
  entries.push(log);
  fs.writeFileSync(LOG_INDEX, JSON.stringify(entries, null, 2));
}

// ── Main ────────────────────────────────────────────────────────────
async function main() {
  if (args.list) {
    // List past sends
    try {
      const entries = JSON.parse(fs.readFileSync(LOG_INDEX, "utf-8"));
      console.log(`📋 ${entries.length} messages sent:\n`);
      entries.forEach((e, i) =>
        console.log(`${i + 1}. ${e.lead || e.phone} — ${e.sent_at} [${e.success ? "✅" : "❌"}]`)
      );
    } catch {
      console.log("No messages sent yet.");
    }
    return;
  }

  // ── Resolve lead ──────────────────────────────────────────────
  let phone = args.to;
  let message = args.msg;
  const demo_url = args.demo_url;

  if (args.lead) {
    const lead = findLead(args.lead);
    if (!lead) {
      console.error(`❌ Lead not found: "${args.lead}"`);
      process.exit(1);
    }
    if (!demo_url) {
      console.error("❌ --url <demo_url> is required when using --lead");
      process.exit(1);
    }
    phone = lead.phone.replace(/[^0-9]/g, "");
    if (phone.startsWith("91") && phone.length > 10) {
      // Already has country code
    } else if (phone.length === 10) {
      phone = "91" + phone;
    }
    message = composeWhatsAppMessage(lead, demo_url);
    console.log(`📋 Lead: ${lead.name}`);
    console.log(`📞 Phone: +${phone}`);
    console.log(`📝 Message: ${message.substring(0, 100)}...`);
  }

  if (!phone || !message) {
    console.log(`
📱 WhatsApp Auto-Sender
───────────────────────
USAGE:
  node scripts/send_whatsapp.js --lead "Clinic Name" --url "https://demo.example.com"
  node scripts/send_whatsapp.js --to 919820854665 --msg "Your message"
  node scripts/send_whatsapp.js --list                    → show sent messages

EXAMPLES:
  node scripts/send_whatsapp.js --lead "Dr Merchant's Dental Clinic" --url "https://kevin.github.io/lead-demos/dr-merchants-dental-clinic/"
    `);
    return;
  }

  // ── Connect to WhatsApp ───────────────────────────────────────
  console.log("\n🔌 Connecting to WhatsApp...");

  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const sock = makeWASocket({
    auth: state,
    logger: P({ level: "silent" }),
    printQRInTerminal: true,
    browser: ["Kevin (Hermes)", "Chrome", "1.0"],
  });

  // Print QR to terminal
  sock.ev.on("connection.update", (update) => {
    const { connection, lastDisconnect, qr } = update;
    if (qr) {
      console.log("\n📱 Scan this QR code with WhatsApp:\n");
      qrcode.generate(qr, { small: true });
    }
    if (connection === "open") {
      console.log("✅ Connected!");
    }
  });

  // Handle disconnects
  sock.ev.on("connection.update", ({ connection, lastDisconnect }) => {
    if (connection === "close") {
      const code = lastDisconnect?.error?.output?.statusCode;
      const shouldReconnect = code !== DisconnectReason.loggedOut;
      console.log(`⚠️  Connection closed. ${shouldReconnect ? "Will reconnect." : "Logged out."}`);
      if (!shouldReconnect) {
        fs.rmSync(AUTH_DIR, { recursive: true, force: true });
        console.log("💡 Auth cleared. Run again to re-scan QR.");
      }
    }
  });

  // Save credentials
  sock.ev.on("creds.update", saveCreds);

  // ── Wait for connection ───────────────────────────────────────
  await new Promise((resolve) => {
    sock.ev.on("connection.update", (update) => {
      if (update.connection === "open") resolve();
    });
  });

  // ── Send ──────────────────────────────────────────────────────
  let cleanPhone = phone.replace(/[^0-9]/g, "");
  if (cleanPhone.startsWith("0")) {
    cleanPhone = cleanPhone.substring(1);
  }
  if (cleanPhone.startsWith("91") && cleanPhone.length > 10) {
    // Already has country code
  } else if (cleanPhone.length === 10) {
    cleanPhone = "91" + cleanPhone;
  }
  const jid = `${cleanPhone}@s.whatsapp.net`;
  console.log(`📤 Sending to ${jid}...`);

  try {
    await sock.sendMessage(jid, { text: message });
    console.log("✅ Message sent!");
    logSent(phone, args.lead || phone, message, true);
  } catch (err) {
    console.error("❌ Failed to send:", err.message);
    logSent(phone, args.lead || phone, message, false);
  }

  // Wait a moment for delivery, then exit
  setTimeout(() => process.exit(0), 2000);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
