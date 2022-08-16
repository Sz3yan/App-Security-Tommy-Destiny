# IT2555 Final Presentation
- Briefly explain your chosen OWASP Top 10
- List your mitigations and explain how they mitigate the vulnerabilities
- Demo your web application pages/functions/features
- Demo your mitigations (if demo-able)


## Project Description
---
Tommy Destiny is a powerful app for Tommy to publish content, share, and grow a business around their content. It is equipped with modern tools to easily create posts, update and engage with their audience.



## Sze Yan

- Home Page
- About
- Allpost
- Post page
- Admin Dashboard
- Admin ViewPage
- Admin Post
- Admin Post edit
- Admin Page
- Admin Page edit

<br>

### A3 Sensitive Data Exposure
---
- Encryption at rest at server-side using AES256 Galois/Counter mode
    - to prevent complex CBC attacks such as
        - Chosen Plaintext Attack(CPA) — Attacks with a set of chosen plaintexts and to obtain respective ciphertext.
        - Chosen Ciphertext Attack(CCA) — Attacks with a set of chosen ciphertexts to obtain respective plaintexts.
        
        it is necessary to use Authenticated Encryption, hence AES GCM is used. 
        
    - AES-GCM is a combination of Counter mode (CTR) and Authentication it’s faster and more secure with a better implementation for table-driven field operations.
    - [Reference](https://isuruka.medium.com/selecting-the-best-aes-block-cipher-mode-aes-gcm-vs-aes-cbc-ee3ebae173c)
- Encryption at rest at Google Firebase using AES256 Galois/Counter mode
- Key Rotation for the key used in cryptographic operations, generated using Google Cloud Key Management System (KMS) Hardware Security Module.
    - Limiting the number of messages encrypted with the same key version helps prevent data compromised.
        - if 1 key encrypts 10 documents, in the event that a key is compromised, all 10 documents are vulnearble.
        - key v1 encrypts 5 document, key v2 encrypts another 5 document. In the event that key v1 is compromised, only 5 document are vulnerable.
    - every 30 days, the key will be rotated (new key version generated). that new key version will be use for the encryption and decryption. the KMS will use the correct key version to encrypt to decrypt the data. This can be done up to 20 times, requiring re-encryption of data at least once every 5 years.
        - key is also generated using AES 256 bit GCM
    - Google Cloud Hardware Security Module (HSM): allows you to host encryption keys and perform cryptographic operations in a cluster of FIPS 140-2 Level 3 certified HSMs.
        - HSM: dedicated cryptographic processor that manages and safeguards digital keys. the our app don’t store the key. instead, it calls to the HSM to decrypt it, and returns the plaintext.
            - They have special hardware to create entropy and generate high quality random keys (high entropy). Google Cloud HSM achieves FIPS 140-2 Level 3.
            - Build using custom hardware that is significantly harder to exploit. HSM have
                - a lower surface area of attack as compared to a standard computers with different components such as GPU, motherbord, RAM, OS.
                - Tamper-proof hardware — erase the key if the attacker remove it from the hardware.
                - Built in audit trail — log all operations being done.
    - Reference [HSM](https://www.youtube.com/watch?v=uewhaNg1BhE)
    - Reference [Google Cloud HSM](https://cloud.google.com/kms/docs/hsm)
- Firebase Hashing: scrypt to hash passwords
    - better design than BCrypt (especially in regards to memory hardness)
    - Configured with:
        - rounds: 8
        - mem_cost: 14
    - Reference [[https://medium.com/analytics-vidhya/password-hashing-pbkdf2-scrypt-bcrypt-and-argon2-e25aaf41598e](https://medium.com/analytics-vidhya/password-hashing-pbkdf2-scrypt-bcrypt-and-argon2-e25aaf41598e)]
- Secret kept safe using Google Secret Manager.
    - a secure and convenient storage system for API keys, certificates, and other sensitive data. Data is encrypted in transit with TLS and at rest with AES-256-bit encryption keys.
        - use it to store
            - Recapcha secret
            - Google KMS HSM key-id
            - Flask session key
    - Built in integration with Google Cloud Audit logs. This ensures that every transaction made with the Secret Manager will generate an audit log.
- Enabled HSTS for the Flask web application to be hosted using Flask-talisman
    - to prevent MITM attacks

### Insufficient Logging and Monitoring
---
- Google Cloud Logging
    - log all authentication attempts, denied access, and input validation errors
    - can set alerts to notify you whenever a specific message appears in your included logs, or use Cloud Monitoring to alert on logs-based metrics I define.
        - For example, if I want to know when an audit log records a particular data-access message, you can create a log-based alert that matches the message and notifies you when it appears.
- sentry io for monitoring
- Google Cloud Run monitoring
