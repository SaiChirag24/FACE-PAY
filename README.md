# FACE-PAY-
A face-recognition-based payment system that automates access and transactions using Raspberry Pi 3B+, OpenCV, and Python.




🔹 Project Overview
FacePay is an AI-powered secure access and payment system that eliminates the need for physical cards or passwords. It uses facial recognition for user identification and requires a passkey authentication via a keypad for enhanced security. Once authenticated, the system automatically deducts the payment from the user’s digital wallet.


🔹 Features

✅ Facial Recognition: Identifies users using OpenCV & Raspberry Pi Camera

✅ Passkey Authentication: Additional security layer via a keypad

✅ Automated Payments: Deducts money from a digital wallet upon successful authentication

✅ LCD Display & LED Indicators: Provides real-time user feedback

✅ Seamless Integration: Works as a smart access control and payment system

🔹 Components Used

Raspberry Pi 3B+ (Main processing unit)

Raspberry Pi Camera Module (Captures images for facial recognition)

4x4 Keypad (User input for passkey authentication)

LCD Display (Displays transaction & system status)

LED Indicators (Green = success, Red = authentication failure)


🔹 Technologies Used

Python (Core programming language)

OpenCV (Facial recognition and image processing)

NumPy (Efficient array processing for machine learning)

Raspberry Pi GPIO (Interfacing with hardware components)


🔹 How It Works
User stands in front of the Pi Camera for facial recognition.
If face matches the database, the system prompts for passkey entry on the keypad.
Upon correct passkey entry, payment is deducted from the digital wallet.
LCD screen & LEDs indicate authentication and transaction status.
