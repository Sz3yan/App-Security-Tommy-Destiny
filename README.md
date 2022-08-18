# NYP Y2S1 Application Security

### Background
Tommy Destiny is a powerful app for Tommy to publish content, and grow a business around their content. It is equipped with modern tools to easily create, update and manage pages and posts catered for its audience.  

### Run the program
    pip install -r requirements.txt
    python app.py

### Security Mitigations for OWASP Top 10 2017 and 2019
- [A2_Broken_authentication](https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication)
- [A3_Sensitive_data_exposure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure)
- [A5_Broken_access_control](https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control)
- [A7_Cross_site_scripting](https://owasp.org/www-project-top-ten/2017/A7_2017-Cross-Site_Scripting_(XSS))
- [API3_Excessive_data_exposure](https://github.com/OWASP/API-Security/blob/master/2019/en/src/0xa3-excessive-data-exposure.md)
- [API4_Lack_of_resource_and_rate_limiting](https://github.com/OWASP/API-Security/blob/master/2019/en/src/0xa4-lack-of-resources-and-rate-limiting.md)
- [API6_Mass_Assignment](https://github.com/OWASP/API-Security/blob/master/2019/en/src/0xa6-mass-assignment.md)
- [API10_Insufficient_logging_and_monitoring](https://github.com/OWASP/API-Security/blob/master/2019/en/src/0xaa-insufficient-logging-monitoring.md)

### Project Structure
Project Structure:
<pre>
Tommy-Destiny
├── app.py
├── config.py
├── Procfile
├── README.md
├── requirements.txt
├── flask_session
├── google.json (include your own google service account key)
├── .env (include your own firebase credential)
├── LICENSE.md
├── mitigations
│  ├── A2_Broken_authentication.py
│  ├── A3_Sensitive_data_exposure.py
│  ├── A7_Cross_site_scripting.py
│  ├── API3_Excessive_data_exposure.py
│  ├── API6_Mass_Assignment.py
│  └── API10_Insufficient_logging_and_monitoring.py
├── routes
│  ├── admin
│  │  ├── admin_routes.py
│  │  ├── static
│  │  │  └── py
│  │  │     ├── Create_policy_form.py
│  │  │     ├── Page.py
│  │  │     └── Post.py
│  │  └── templates
│  │     ├── admin_dashboard.html
│  │     ├── admin_editor.html
│  │     ├── admin_editor_page.html
│  │     ├── admin_pages.html
│  │     ├── admin_post.html
│  │     └── admin_viewsite.html
│  ├── api
│  │  └── api_routes.py
│  ├── errors
│  │  ├── error_routes.py
│  │  └── templates
│  │     └── error.html
│  └── user
│     ├── static
│     │  └── py
│     │     └── Forms.py
│     ├── templates
│     │  ├── about.html
│     │  ├── allposts.html
│     │  ├── enterOTP.html
│     │  ├── home.html
│     │  ├── login.html
│     │  ├── policy.html
│     │  ├── post.html
│     │  ├── pricing.html
│     │  ├── profile.html
│     │  ├── signup.html
│     │  └── top4post.html
│     └── user_routes.py
├── static
│  ├── firebaseConnection.py
│  └── serviceAccountKey.json (include your own firebase adminsdk account key)
└── templates
   ├── adminbase.html
   ├── base.html
   ├── baselogin.html
   ├── includes
   │  ├── adminnavbar.html
   │  ├── footer.html
   │  ├── formHelper.html
   │  └── navbar.html
   └── top4base.html
</pre>

**Done by: Sze Yan, Yee Ping, Stefanie, and Mizuki**