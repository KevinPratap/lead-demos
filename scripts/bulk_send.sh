#!/bin/bash
# Bulk WhatsApp send — sends to all leads with 30s delay
cd /home/prata/leads

echo "Sending to: Saifee Dental Clinic"
node scripts/send_whatsapp.js --lead 'Saifee Dental Clinic' --url 'https://kevinpratap.github.io/lead-demos/saifee-dental-clinic/'
sleep 30

echo "Sending to: Ganatras Dental Care"
node scripts/send_whatsapp.js --lead 'Ganatras Dental Care' --url 'https://kevinpratap.github.io/lead-demos/ganatras-dental-care/'
sleep 30

echo "Sending to: Tooth Smith Dental Clinic"
node scripts/send_whatsapp.js --lead 'Tooth Smith Dental Clinic' --url 'https://kevinpratap.github.io/lead-demos/tooth-smith-dental-clinic/'
sleep 30

echo "Sending to: Smile Plus Dental Clinic"
node scripts/send_whatsapp.js --lead 'Smile Plus Dental Clinic' --url 'https://kevinpratap.github.io/lead-demos/smile-plus-dental-clinic/'
sleep 30

echo "Sending to: Powai Medical and Dental Centre"
node scripts/send_whatsapp.js --lead 'Powai Medical and Dental Centre' --url 'https://kevinpratap.github.io/lead-demos/powai-medical-and-dental-centre/'
sleep 30

echo "Sending to: Smilee Dental Care"
node scripts/send_whatsapp.js --lead 'Smilee Dental Care' --url 'https://kevinpratap.github.io/lead-demos/smilee-dental-care/'
sleep 30

echo "Sending to: Dr. Namrata Patil Shiwalkar | Dent-O-Fit ~ Total Dental Fitness Centre"
node scripts/send_whatsapp.js --lead 'Dr. Namrata Patil Shiwalkar | Dent-O-Fit ~ Total Dental Fitness Centre' --url 'https://kevinpratap.github.io/lead-demos/dr-namrata-patil-shiwalkar-dent-o-fit-total-dental-fitness-centre/'
sleep 30

echo "Sending to: Specialist Dental Centre (SINCE 1983)"
node scripts/send_whatsapp.js --lead 'Specialist Dental Centre (SINCE 1983)' --url 'https://kevinpratap.github.io/lead-demos/specialist-dental-centre-since-1983/'
sleep 30

echo "Sending to: 32 Smile Stones"
node scripts/send_whatsapp.js --lead '32 Smile Stones' --url 'https://kevinpratap.github.io/lead-demos/32-smile-stones/'
sleep 30

echo "Sending to: CARE DENTAL CLINIC"
node scripts/send_whatsapp.js --lead 'CARE DENTAL CLINIC' --url 'https://kevinpratap.github.io/lead-demos/care-dental-clinic/'
sleep 30

echo "Sending to: Perfect Smile Dental Care Centre"
node scripts/send_whatsapp.js --lead 'Perfect Smile Dental Care Centre' --url 'https://kevinpratap.github.io/lead-demos/perfect-smile-dental-care-centre/'
sleep 30

echo "Sending to: Dental Excellence dental clinic"
node scripts/send_whatsapp.js --lead 'Dental Excellence dental clinic' --url 'https://kevinpratap.github.io/lead-demos/dental-excellence-dental-clinic/'
sleep 30

echo "Sending to: The Tooth Junction"
node scripts/send_whatsapp.js --lead 'The Tooth Junction' --url 'https://kevinpratap.github.io/lead-demos/the-tooth-junction/'
sleep 30

echo "Sending to: Dental Care Clinic"
node scripts/send_whatsapp.js --lead 'Dental Care Clinic' --url 'https://kevinpratap.github.io/lead-demos/dental-care-clinic/'
sleep 30

echo "Sending to: Glow Dent Clinic – Dr. Anjali Holambe | Dentist in Bandra | Goregaon Mumbai"
node scripts/send_whatsapp.js --lead 'Glow Dent Clinic – Dr. Anjali Holambe | Dentist in Bandra | Goregaon Mumbai' --url 'https://kevinpratap.github.io/lead-demos/glow-dent-clinic-dr-anjali-holambe-dentist-in-bandra-goregaon-mumbai/'
sleep 30

echo "Sending to: PERFECT SMILE DENTAL CARE CENTRE"
node scripts/send_whatsapp.js --lead 'PERFECT SMILE DENTAL CARE CENTRE' --url 'https://kevinpratap.github.io/lead-demos/perfect-smile-dental-care-centre/'
sleep 30

echo "All sends complete!"
