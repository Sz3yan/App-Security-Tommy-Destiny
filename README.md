# NYP Y2S1 Application Security

# Background 
Tommy Destiny is a powerful app for Tommy to publish content, share, and grow a business around their content. It is equipped with modern tools to easily create newsletters, update and engage with their audience. It has simple statistics to show subscription rate, amount of money generated to better understand what content is getting the most attention and who your biggest fans are and create more for them. 



# Run the program
    npm install
    pip install -r requirements.txt
    python app.py


# Feature 
- Admin Homepage
- User Subscription
- View User Details of who Subscribed
- View All Content
- Create Blog Page
- Create Newsletter Page
- Set and Edit Colleague Role
- Import and Export Content

# Project Strucutre
├── README.md
├── requirements.txt
└── Tommy-Destiny
   ├── _init__.py
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
   │     └── firebaseConnection.py
   ├── templates
   │  ├── base.html
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
         │  ├── pricing.html
         │  ├── signup.html
         │  └── view_post.html
         └── user_routes.py


Done by: Sze Yan, Yee Ping, Stefanie and Mizuki