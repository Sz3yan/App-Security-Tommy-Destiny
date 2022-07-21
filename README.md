# NYP Y2S1 Application Security

### Background
Tommy Destiny is a powerful app for Tommy to publish content, share, and grow a business around their content. It is equipped with modern tools to easily create newsletters, update and engage with their audience. It has simple statistics to show subscription rate, amount of money generated to better understand what content is getting the most attention and who your biggest fans are and create more for them. 

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
├── README.md
├── requirements.txt
└── Tommy-Destiny
   ├── __init__.py
   ├── api
   │  └── routes.py
   ├── mitigations
   │  ├── A2_Broken_authentication.py
   │  ├── A3_Sensitive_data_exposure.py
   │  ├── A5_Broken_access_control.py
   │  ├── A7_Cross_site_scripting.py
   │  ├── API3_Excessive_data_exposure.py
   │  ├── API4_Lack_of_resource_and_rate_limiting.py
   │  ├── API6_Mass_Assignment.py
   │  └── API10_Insufficient_logging_and_monitoring.py
   ├── Procfile
   ├── static
   │  ├── css
   │  │  └── screen.css
   │  ├── js
   │  │  └── firebaseConfiguration.js
   │  └── py
   │     ├── firebaseConnection.py
   │     └── roles.py
   ├── templates
   │  ├── base.html
   │  ├── baselogin.html
   │  └── includes
   │     ├── footer.html
   │     ├── formHelper.html
   │     └── navbar.html
   └── web
      ├── admin
      │  ├── admin_routes.py
      │  ├── static
      │  │  ├── css
      │  │  │  └── admin.css
      │  │  └── py
      │  │     └── Post.py
      │  └── templates
      │     ├── admin_dashboard.html
      │     ├── admin_editor.html
      │     ├── admin_members.html
      │     ├── admin_pages.html
      │     ├── admin_post.html
      │     ├── admin_settings.html
      │     ├── admin_tags.html
      │     └── admin_viewsite.html
      └── user
         ├── static
         │  ├── css
         │  │  └── signup.css
         │  └── py
         │     └── Forms.py
         ├── templates
         │  ├── home.html
         │  ├── login.html
         │  ├── payment.html
         │  ├── post.html
         │  ├── pricing.html
         │  ├── profile.html
         │  ├── signup.html
         │  └── view_post.html
         └── user_routes.py
</pre>

**Done by: Sze Yan, Yee Ping, Stefanie, and Mizuki**